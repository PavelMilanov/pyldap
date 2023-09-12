from environs import Env


env = Env()
env.read_env()


__all__ = ['RedisConnector']
