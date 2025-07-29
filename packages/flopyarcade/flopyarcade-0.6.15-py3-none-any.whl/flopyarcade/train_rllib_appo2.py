# import os
# import sys
# import logging
# import warnings
# from argparse import ArgumentParser
# from os import makedirs
# from os.path import abspath, dirname, exists, join

# # Setup
# logging.disable(logging.WARNING)
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# warnings.filterwarnings('ignore', category=DeprecationWarning)

# # Ensure local imports work
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# # Import Ray and RLlib
# import ray
# from ray.tune.registry import register_env
# from ray import air, tune, train
# from ray.rllib.algorithms.appo import APPOConfig

# # Import Gymnasium
# import gymnasium as gym

# # Import your environment
# try:
#     from flopyarcade.flopyarcade import FloPyEnv
# except ImportError:
#     from flopyarcade import FloPyEnv

# # Utility: str to bool
# def str_to_bool(value):
#     if isinstance(value, bool):
#         return value
#     if value.lower() in {'false', 'f', '0', 'no', 'n'}:
#         return False
#     elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
#         return True
#     raise ValueError(f'{value} is not a valid boolean value')

# # Argument parsing
# parser = ArgumentParser(description='FloPyArcade optimization using deep Q networks')
# parser.add_argument('--envtype', default='1s-d', type=str, help='string defining environment')
# parser.add_argument('--suffix', default='', type=str, help='string defining environment')
# parser.add_argument('--cpus', default=1, type=int, help='number of cpus to use')
# parser.add_argument('--gpus', default=0, type=int, help='number of gpus to use')
# parser.add_argument('--playbenchmark', default=False, type=str_to_bool, help='display runs')
# parser.add_argument('--external', default=True, type=str_to_bool, help='temporary helper')
# args = parser.parse_args()

# ENVTYPE = args.envtype

# # RLlib Model and Training Config
# config_model = {
#     "fcnet_hiddens": [512, 1024, 512],
#     "fcnet_activation": "relu",
#     "post_fcnet_hiddens": [],
#     "post_fcnet_activation": "relu",
#     "free_log_std": False,
#     "no_final_linear": False,
#     "vf_share_layers": True,
#     "dim": 84,
#     "grayscale": False,
#     "zero_mean": True
# }

# config_stopCriteria = {
#     "training_iteration": int(1e12),
#     "timesteps_total": int(1e12),
#     "episode_reward_mean": 990,
# }

# def env_creator(env_config):
#     # Ensure env_config is passed correctly
#     env_config = dict(env_config) if env_config else {}
#     env_config['ENVTYPE'] = ENVTYPE
#     env = FloPyEnv(env_config=env_config)
#     from gymnasium.wrappers import EnvCompatibility
#     env = EnvCompatibility(env)
#     return env

# def env_creator_MountainCarContinuous(env_config):
#     return gym.make('MountainCarContinuous-v0')

# def test(agent, env):
#     """Test trained agent for a single episode. Return the episode reward"""
#     from matplotlib.pyplot import switch_backend
#     switch_backend('TkAgg')
#     env.RENDER = True
#     reward_total = 0.
#     obs, _ = env.reset()
#     done = False
#     truncated = False
#     while not (done or truncated):
#         action = agent.compute_single_action(obs)
#         obs, reward, done, truncated, info = env.step(action)
#         reward_total += reward
#     return reward_total

# if __name__ == "__main__":
#     # Ray initialization
#     import ray
#     ray.init(include_dashboard=False)

#     # Register environments
#     register_env("my_env", env_creator)
#     # Other env registrations...

#     # RLlib APPOConfig (Ray 2.x+)
#     config = APPOConfig()
#     config = config.training(lr=tune.grid_search([0.0002]))
#     config = config.framework('tf')
#     #... other config settings ...
#     config = config.environment(env="my_env")  # Correct environment setting

#     tuner = tune.Tuner(
#         "APPO",
#         run_config=air.RunConfig(
#             stop={"episode_reward_mean": 100},
#             local_dir="D:\\ray_results_temp",  # Correct path
#             checkpoint_config=train.CheckpointConfig(
#                 checkpoint_frequency=5,
#                 checkpoint_at_end=True,
#             ),
#             name="APPO",
#         ),
#         param_space=config.to_dict(),
#     )
#     tuner.fit()


import ray
from ray.tune.registry import register_env
from gymnasium.wrappers import EnvCompatibility

def env_creator(env_config):
    from flopyarcade.flopyarcade import FloPyEnv
    env = FloPyEnv(env_config=env_config)
    from gymnasium.wrappers import EnvCompatibility
    env = EnvCompatibility(env)  # Only if your env is not Gymnasium API
    return env

ray.init(include_dashboard=False)
register_env("my_env", env_creator)