import gym
import sys
import os
import random

from multiprocessing import Process, Queue

from snake.env import register
from deep_snake_brain import SnakeNetwork


class Unbuffer(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


class GymWorkerDatum(object):

    def __init__(self, identifier, total_steps, total_episodes,
                 old_observation, new_observation, last_reward,
                 last_action, last_Q_base, messages):
        self.identifier = identifier
        self.total_steps = total_steps
        self.total_episodes = total_episodes
        self.old_observation = old_observation
        self.new_observation = new_observation
        self.last_reward = last_reward
        self.last_action = last_action
        self.last_Q_base = last_Q_base
        self.messages = messages


class GymWorker(object):

    def __init__(self, identifier):
        self.env = gym.make("SnakeHeadless-v0")
        self.env.seed(random.randint(0, 9999999))
        self.identifier = identifier
        self.total_steps = 0
        self.episode = 0
        self.episode_reward = 0
        self.episode_steps = 0
        self.observation = self.env.reset()
        self.out_buffer = []

    def encode(self):
        data = GymWorkerDatum(
            old_observation=self.old_observation,
            new_observation=self.new_observation,
            last_reward=self.reward,
            last_action=self.action,
            last_Q_base=self.Q_base,
            total_steps=self.total_steps,
            total_episodes=self.episode,
            identifier=self.identifier,
            messages=self.out_buffer
        )
        self.out_buffer = []
        return data

    def reset(self):
        self.out_buffer = [
            "#" * 20,
            "Worker %s - Episode: %s" % (self.identifier, self.episode),
            "Worker %s - Episode reward: %s" % (self.identifier, self.episode_reward),
            "Worker %s - Episode steps elapsed: %s" % (self.identifier, self.episode_steps),
        ]

        self.observation = self.env.reset()
        self.episode += 1
        self.episode_steps = 0
        self.episode_reward = 0

    def store_action(self, action, Q_base):
        self.action = action
        self.Q_base = Q_base

    def step(self):
        self.old_observation = self.observation
        (self.new_observation, self.reward, self.done, info) = self.env.step(self.action)

        self.episode_steps += 1
        self.total_steps += 1
        self.episode_reward += self.reward

        if self.done:
            self.reset()
        else:
            self.observation = self.new_observation


def gym_process_main(recv_queue, send_queue, identifier):
    register()
    worker = GymWorker(identifier)
    should_run = recv_queue.get(timeout=20)
    while should_run:
        send_queue.put(worker.observation)
        (action, Q_base) = recv_queue.get(timeout=20)
        worker.store_action(action, Q_base)
        worker.step()
        send_queue.put(worker.encode(), timeout=20)
        should_run = recv_queue.get(timeout=20)


class Worker(object):

    def __init__(self, target, identifier):
        self.queue_out = Queue()
        self.queue_in = Queue()
        self.target = target
        self.identifier = identifier
        self.process = Process(
            target=self.target,
            args=(self.queue_out, self.queue_in, self.identifier)
        )
        self.process.daemon = True

    def start(self):
        self.process.start()

    def get(self):
        return self.queue_in.get()

    def put(self, val):
        return self.queue_out.put(val)

    def join(self):
        return self.process.join()


def main():
    worker_count = 2
    workers = []
    for i in range(worker_count):
        workers.append(Worker(target=gym_process_main, identifier=i))

    checkpoint_path = os.path.abspath(os.path.join("checkpoints", "snake-deep-noloop.ckpt"))
    if not os.path.isdir(os.path.dirname(checkpoint_path)):
        os.makedirs(os.path.dirname(checkpoint_path))

    env = gym.make("SnakeHeadless-v0")
    agent = SnakeNetwork(
        feature_count=env.observation_space.shape[2],
        level_width=env.observation_space.shape[0],
        level_height=env.observation_space.shape[1],
        action_count=env.action_space.n,
        checkpoint_path=checkpoint_path
    )
    loaded = agent.load()

    total_steps = 0
    total_episodes = 0
    last_total_episodes = 0
    extra_episodes = 0

    if loaded:
        extra_episodes = 32000

    for worker in workers:
        worker.start()

    while total_episodes < 30000:
        epsilon = 1.0 / (0.01 * (extra_episodes + (total_steps / 1000)))
        agent.epsilon = min(epsilon, 0.1)

        for worker in workers:
            worker.put(True)  # Signal that we should keep running
            observation = worker.get()
            worker.put(agent.choose_action(observation))

        total_steps = 0
        total_episodes = 0
        messages = []
        for worker in workers:
            data = worker.get()

            agent.learn(
                old_state=data.old_observation,
                new_state=data.new_observation,
                action=data.last_action,
                reward=data.last_reward,
                Q_base=data.last_Q_base,
            )
            total_steps += data.total_steps
            total_episodes += data.total_episodes

            if data.messages and not messages:
                messages = data.messages

        if total_episodes != last_total_episodes:
            for message in messages:
                print(message)
            print("-" * 20)
            print("Total steps: %s" % total_steps)
            print("Total episodes: %s" % total_episodes)

            if total_episodes % 500 == 0:
                agent.save()

        last_total_episodes = total_episodes

    for worker in workers:
        worker.put(False)  # Signal that we should stop

    for worker in workers:
        worker.join()


if __name__ == "__main__":
    sys.stdout = Unbuffer(sys.stdout)
    register()
    main()
