class ConfigurationException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class MissingEnvVariable(ConfigurationException):

    def __init__(self, env_var: str):
        msg = f'Invalid Configuration! The required environment variable {env_var} is missing.'
        super().__init__(msg)
