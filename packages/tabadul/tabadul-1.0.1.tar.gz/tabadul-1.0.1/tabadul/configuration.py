class Configuration(object):
    """
    This class allows SDK configuration without requiring instantiation.
    Properties and methods can be accessed statically.
    """

    # Enum for API server endpoints
    class Server(object):
        BASE_URL = 'base_url'

    # Enum for SDK environments
    class Environment(object):
        """
        Specifies the environment in which the SDK is intended to operate.
        """
        PRODUCTION = 'production'

    # Configuration for each environment
    environments = {
        Environment.PRODUCTION: {
            Server.BASE_URL: 'https://qapigw.tabadul.sa',
        },
    }

    # The active environment for the SDK
    environment = Environment.PRODUCTION

    # API credentials for authentication
    tabadul_client_id = None
    tabadul_client_secret = None

    @classmethod
    def get_base_uri(cls, server=Server.BASE_URL):
        """
        Constructs and returns the base URI for the specified environment and server.
        This is used as the foundation for all API requests.
        """
        return cls.environments[cls.environment][server]