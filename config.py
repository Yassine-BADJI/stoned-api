import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # SECRET_KEY = os.getenv('SECRET_KEY')
    SECRET_KEY = 'thisissecretkeytest'
    SENDGRID_KEY = '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'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'stoned_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://wdbjcwvtwqrepa' \
                              ':cee8af49d68c54942189e2d9688e7fa5f2d2b6d00f9dd0e8d4bd90febacf4b24@ec2-54-228-250-82.eu' \
                              '-west-1.compute.amazonaws.com:5432/d5d3577l6fd3ac'


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
sg_key = Config.SENDGRID_KEY
