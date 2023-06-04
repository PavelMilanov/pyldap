from environs import Env

env = Env()
env.read_env()

__version__ = env('VERSION')