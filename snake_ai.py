import gym
import sys
import os

from snake.env import register
from snek_brain import SnakeNetwork


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
    env = gym.make("Snake-v0")

    checkpoint_path = os.path.abspath(os.path.join("checkpoints", "snake.ckpt"))
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
        extra_episodes += 500

    for episode in range(500):
        episode_total_reward = 0
        observation = env.reset()
        agent.epsilon = 1.0 / (0.1 * (extra_episodes + episode) + 2)

        for i in range(500):
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
            if done:
                break

        print("#" * 20)
        print("Episode: %s" % (episode + 1))
        print("Episode reward: %.2f" % round(episode_total_reward, 2))
        print("Steps elapsed: %s" % (i + 1))
        print("Epsilon: %.2f" % round(agent.epsilon, 2))

        if (episode + 1) % 50 == 0:
            agent.save()


if __name__ == "__main__":
    sys.stdout = Unbuffer(sys.stdout)
    register()
    main()
