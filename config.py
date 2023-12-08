class Config :
    HOST='minamidb.cfsuebajeebd.ap-northeast-2.rds.amazonaws.com'
    DATABASE = 'memo'
    DB_USER = 'memo_user'
    DB_PASSWORD = '3728'

    PASSWORD_SALT = 'Minami1*hi123'


    ### JWT 관련 변수 셋팅
    JWT_SECRET_KEY = 'Minami1##bye~~'
    JWT_ACCESS_TOKEN_EXPIRES = False
    PROPAGATE_EXCEPTIONS = True