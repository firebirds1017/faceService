import os

baseDir = os.path.abspath(os.path.dirname(__file__))


class Config:

    @staticmethod
    def init_app():
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = "mongodb://faceDetectAdmin:admin@localhost:27017/face"


class ProductionConfig(Config):
    MONGO_URI = "mongodb://faceDetectAdmin:admin@localhost:27017/face"


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig

}

# ############################
# Const code
# ############################

CONST_COMPARE_FACE_SUCCESS = '00000'
CONST_COMPARE_UNKNOWN_FACE_NO_FACE_FOUND = "10001"
CONST_COMPARE_UNKNOWN_FACE_FACE_TOO_MANY = "10002"
CONST_COMPARE_KNOWN_FACE_NO_FACE_FOUND = "10003"
CONST_COMPARE_KNOWN_FACE_FACE_TOO_MANY = "10004"
CONST_ERROR = "20001"
CONST_COMPARE_FACE_INSERT_ERROR = "30001"
CONST_COMPARE_FACE_DELETE_ERROR = "30002"
CONST_COMPARE_USER_NOT_FOUND = "60001"
