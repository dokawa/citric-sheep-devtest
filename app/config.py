class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///elevator.db"
    DEBUG = True


class TestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    DEBUG = True
