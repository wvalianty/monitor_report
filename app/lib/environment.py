import os


def get_dingding_url(env_var):
    env_list = os.environ
    return env_list.get(env_var)