from os import environ

class BaseConfig(object):
    """Base configuration."""

    DEBUG = None
    DB_HOST = "bd_name"
    DB_USER = "db_user"
    DB_PASS = "db_pass"
    DB_NAME = "db_name"
    DB_DIALECT = "mysql"
    DB_DRIVER = "pymysql"
    DB_PORT = "3306"
    SQLALCHEMY_DATABASE_URI="{0}+{1}://{2}:{3}@{4}:{5}/{6}".format(DB_DIALECT, DB_DRIVER, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = "secret"

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    ENV = "development"
    DEBUG = environ.get("DEBUG", True)
    DB_HOST = environ.get("DB_HOST")
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = "{0}+{1}://{2}:{3}@{4}:{5}/{6}".format(BaseConfig.DB_DIALECT, BaseConfig.DB_DRIVER, DB_USER, DB_PASS, DB_HOST, BaseConfig.DB_PORT, DB_NAME)


class TestingConfig(BaseConfig):
    """Testing configuration."""

    ENV = "testing"
    TESTING = True
    DEBUG = environ.get("DEBUG", True)
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")
    SQLALCHEMY_DATABASE_URI = "{0}+{1}://{2}:{3}@{4}:{5}/{6}".format(BaseConfig.DB_DIALECT, BaseConfig.DB_DRIVER, DB_USER, DB_PASS, DB_HOST, BaseConfig.DB_PORT, DB_NAME)


class ProductionConfig(BaseConfig):
    """Production configuration."""

    ENV = "production"
    DEBUG = environ.get("DEBUG", False)
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "grupo33")
    DB_PASS = environ.get("DB_PASS", "N2I2ZmNlNTc4ZTM4")
    DB_NAME = environ.get("DB_NAME", "grupo33")
    SQLALCHEMY_DATABASE_URI = "{0}+{1}://{2}:{3}@{4}:{5}/{6}".format(BaseConfig.DB_DIALECT, BaseConfig.DB_DRIVER, DB_USER, DB_PASS, DB_HOST, BaseConfig.DB_PORT, DB_NAME)


config = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)
