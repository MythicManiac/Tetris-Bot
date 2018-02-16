import gym

from snake.env import register
from snek_brain import SnakeNetwork


def main():
    env = gym.make("Snake-v0")
    agent = SnakeNetwork(
        feature_count=env.observation_space.shape[2],
        level_width=env.observation_space.shape[0],
        level_height=env.observation_space.shape[1],
        action_count=env.action_space.n,
    )

    total_steps = 0

    for episode in range(300):
        episode_total_reward = 0
        observation = env.reset()
        while True:
            action = agent.choose_action(observation)
            (new_observation, reward, done, info) = env.step(action)

            agent.store_transition(observation, action, reward, new_observation)

            episode_total_reward += reward
            if total_steps > 1000:
                agent.learn()

            if done:
                print("#" * 20)
                print("Episode: %s" % episode)
                print("Episode reward: %.2f" % round(episode_total_reward, 2))
                # print("Epsilon: %.2f" % round(agent.epsilon, 2))
                break

            observation = new_observation
            total_steps += 1


if __name__ == "__main__":
    register()
    main()
