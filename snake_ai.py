import gym
import sys
import os

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


def main():
    env = gym.make("SnakeHeadless-v0")

    checkpoint_path = os.path.abspath(os.path.join("checkpoints", "snake-deep-noloop.ckpt"))
    if not os.path.isdir(os.path.dirname(checkpoint_path)):
        os.makedirs(os.path.dirname(checkpoint_path))

    agent = SnakeNetwork(
        feature_count=env.observation_space.shape[2],
        level_width=env.observation_space.shape[0],
        level_height=env.observation_space.shape[1],
        action_count=env.action_space.n,
        checkpoint_path=checkpoint_path
    )
    loaded = agent.load()
    extra_episodes = 0
    if loaded:
        extra_episodes += 32000

    episode = 0
    total_steps = 0
    while True:
        episode += 1
        episode_total_reward = 0
        observation = env.reset()
        epsilon = 1.0 / (0.01 * (extra_episodes + (total_steps / 1000)))
        agent.epsilon = epsilon

        for i in range(1000):
            action, Q_base = agent.choose_action(observation)
            (new_observation, reward, done, info) = env.step(action)

            agent.learn(
                old_state=observation,
                action=action,
                reward=reward,
                new_state=new_observation,
                Q_base=Q_base
            )
            observation = new_observation
            episode_total_reward += reward
            total_steps += 1
            if done:
                break

        print("#" * 20)
        print("Episode: %s" % (episode + 1))
        print("Episode reward: %d" % episode_total_reward)
        print("Episode steps: %s" % (i + 1))
        print("Total steps: %s" % total_steps)
        print("Epsilon: %.4f" % round(agent.epsilon, 4))

        if (episode + 1) % 500 == 0:
            agent.save()

        if episode_total_reward > 70 and episode + 1 >= 5000:
            agent.save()
            break


if __name__ == "__main__":
    sys.stdout = Unbuffer(sys.stdout)
    register()
    main()
