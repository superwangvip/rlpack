import gym
import numpy as np


class ClassicControl(object):
    def __init__(self, env_name):

        assert env_name in {"Acrobot-v1", "CartPole-v1", "CartPole-v0", "MountainCar-v0"}
        self.env = gym.make(env_name)
        self._dim_obs = self.env.observation_space.shape
        self._dim_act = self.env.action_space.n
        self._traj_len = 0
        self._traj_rew = 0

    def reset(self):
        s = self.env.reset()
        return s

    def step(self, action):
        s, r, d, info = self.env.step(action)

        self._traj_len += 1
        self._traj_rew += r

        rew = -1.0 if d is True else 0.1

        if d is True:
            info["episode"] = {"r": self._traj_rew, "l": self._traj_len}
            s = self.env.reset()
            self._traj_len = 0
            self._traj_rew = 0

        return s, rew, d, info

    def sample_action(self):
        return np.random.randint(self.dim_action)

    def seed(self, rnd):
        self.env.seed(rnd)

    @property
    def dim_observation(self):
        return self._dim_obs

    @property
    def dim_action(self):
        return self._dim_act


def make_classic_control(env_name):
    env = ClassicControl(env_name)
    return env


if __name__ == "__main__":
    env = ClassicControl("CartPole-v0")
    s = env.reset()

    all_r = 0
    for i in range(1000):
        a = env.sample_action()
        print(a)
        next_s, r, d, info = env.step(a)
        all_r += r

        print(f"iter {i} a: {a} \t s: {s.shape} max: {np.max(next_s)} min: {np.min(next_s)} {type(next_s)} \t r: {r}, all_r: {all_r} d: {d} info:{info}  ")

        if d is True:
            input()
