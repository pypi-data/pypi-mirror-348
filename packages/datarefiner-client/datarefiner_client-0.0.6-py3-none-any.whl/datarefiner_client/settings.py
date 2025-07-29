from environs import Env

env = Env()
env.read_env()

API_TOKEN: str = env.str("API_TOKEN", None)
API_BASE_URL: str = env.str("API_BASE_URL", "https://app.datarefiner.com")
API_USER_EMAIL: str = env.str("API_USER_EMAIL", None)
API_USER_PASSWORD: str = env.str("API_USER_PASSWORD", None)
