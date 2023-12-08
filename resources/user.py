from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

from email_validator import EmailNotValidError, validate_email

from utils import hash_password


class UserRegisterResource(Resource) :

    def post(self):

        data = request.get_json()

        try:
            validate_email(data['email'])
        except EmailNotValidError as e:
            print(e)
            return{'error' : str(e)}, 400
        
        if len(data['password']) < 4 or len(data['password']) > 14 :
            return {'error' : '비밀번호 길이를 확인하세요'}, 400
        
        password = hash_password(data['password'])

        print(password)

        try :
            connection = get_connection()

            query = '''insert into user
                         (email,password,nickname)
                          values 
                         (%s,%s,%s);'''
            record = (data['email'],
                      data['password'],
                      data['nickname'])
            
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            user_id = cursor.lastrowid

            cursor.close()
            connection.close()


        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return{"error" : str(e)}, 500
        
        access_token = create_access_token(user_id)
            

        return{'result' : 'success',
               'access_token' : access_token}, 200