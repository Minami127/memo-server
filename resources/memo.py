from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from mysql.connector import Error

from flask_jwt_extended import get_jwt_identity

from mysql_connection import get_connection

class MemoListResource(Resource) :

    @jwt_required()
    def post(self) :

        data = request.get_json()
        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''insert into memo
                    (userId, title, date, content)
                    values 
                    ( %s, %s, %s, %s);'''
            record = ( user_id, data['title'],
                        data['date'], data['content'] )
            
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)}, 500
                
        return {'result' : 'success'} , 200




    @jwt_required()
    def get(self) :

        user_id = get_jwt_identity()

        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()

            query = '''select id, title, date, content, createdAt, updateAt
                    from memo
                    where userId = %s
                    order by date desc
                    limit 0,25;''' 

            record = (user_id, )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, record)

            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                result_list[i]['createdAt'] = row['createdAt'].isoformat()
                result_list[i]['updateAt'] = row['updateAt'].isoformat()
                result_list[i]['date'] = row['date'].isoformat()
                i = i + 1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)            
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 500
                
        return {"result" : "success" ,
                "items" : result_list , 
                "count" : len(result_list)}, 200


class MemoResource(Resource) :

    @jwt_required()
    def put(self, memo_id) :

        data = request.get_json()
        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''update memo
                    set 
                    title = %s,
                    date = %s,
                    content = %s 
                    where id = %s and userId = %s;'''
            record = (data['title'], data['date'],
                    data['content'], memo_id, user_id)            
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()
        
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)} , 500

        return {'result' : 'success'} , 200



    @jwt_required()
    def delete(self, memo_id) :

        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''delete from memo
                    where id = %s and userId = %s;'''
            record = (memo_id, user_id)
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()
        
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)} , 500


        return {'result' : 'success'}, 200


