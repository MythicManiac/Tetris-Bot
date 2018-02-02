import numpy as np
import gym


def test_env():
    env = gym.make("Snake-v0")
    ob_space = env.observation_space
    act_space = env.action_space
    ob = env.reset()
    msg = 'Reset observation: {!r} not in space'.format(ob)
    assert ob_space.contains(ob), msg
    a = act_space.sample()
    observation, reward, done, _info = env.step(a)
    msg = 'Step observation: {!r} not in space'.format(observation)
    assert ob_space.contains(observation), msg
    assert np.isscalar(reward), "{} is not a scalar for {}".format(reward, env)
    assert isinstance(done, bool), "Expected {} to be a boolean".format(done)

    for mode in env.metadata.get('render.modes', []):
        env.render(mode=mode)
    env.close()

    # Make sure we can render the environment after close.
    for mode in env.metadata.get('render.modes', []):
        env.render(mode=mode)
    env.close()


def test_random_rollout():
    env = gym.make("Snake-v0")
    agent = lambda ob: env.action_space.sample()  # noqa: E731
    ob = env.reset()
    for _ in range(20):
        assert env.observation_space.contains(ob)
        a = agent(ob)
        assert env.action_space.contains(a)
        (ob, _reward, done, _info) = env.step(a)
        env.render(mode="human")
        if done:
            break
