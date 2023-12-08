from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error


class followResource(Resource) :


    def put(self) :
        data = request.get_json()

        user_id = get_jwt_identity()

        try:
            connection = get_connection()

            query = '''insert into (followerId,followeeId) values (%s,%s)'''

            record = (user_id, data['followerId'], data['followeeId'])

            cursor = connection.cursor()
            cursor.execute(user_id,record)
            connection.commit()

            cursor.close()
            connection.close()



        except Error as e:
            print(e)
            
            return
    
        return

    