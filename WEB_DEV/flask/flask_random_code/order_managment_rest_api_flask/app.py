from flask import Flask, request, abort
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from datetime import datetime
from marshmallow import Schema, fields

from check_user import auth, identity
from config import sql_db

import psycopg2


params = sql_db
date_today = datetime.today().strftime('%Y-%m-%d')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key'

api = Api(app)

jwt = JWT(app, auth, identity)


class OrderSchema(Schema):
    id = fields.Int()
    company = fields.Str()
    client = fields.Str()
    phone_number = fields.Str()
    order_name = fields.Str()
    order_term = fields.Str()
    status = fields.Str()
    comments = fields.Str()
    update_date = fields.Str()
        

class get_all_data(Resource):
    def get(self):
        con = psycopg2.connect(**params)
        cur = con.cursor()
        cur.execute(
            """SELECT id, company, client, phone_number, order_name,
            order_term, status, comments, update_date
            FROM orders
            ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
        query = cur.fetchall()
        con.close()

        data = {query[num][0]:
            {"company": query[num][1],
            "client": query[num][2],
            "phone_number": query[num][3],
            "order_name": query[num][4],
            "order_term": query[num][5],
            "status": query[num][6],
            "comments": query[num][7],
            "update_date": query[num][8]} 
            for num in range(0, len(query))}
        
        return data
    

class get_one_item(Resource):
        def get(self, id):
            id_ = id
        
            con = psycopg2.connect(**params)
            cur = con.cursor()
            cur.execute(
                f"""SELECT id, company, client, phone_number, order_name,
                order_term, status, comments, update_date
                FROM orders WHERE id = {id_}
                ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
            query = cur.fetchall()
            con.close()

            data = {query[num][0]:
                {"company": query[num][1],
                "client": query[num][2],
                "phone_number": query[num][3],
                "order_name": query[num][4],
                "order_term": query[num][5],
                "status": query[num][6],
                "comments": query[num][7],
                "update_date": query[num][8]} 
                for num in range(0, len(query))}
            
            if id_ in data.keys():
                return data
            else:
                abort(404, f"ID:{id_} not Found")

class add_data(Resource):
    
    @jwt_required()
    def post(self):
        # replace data to "" if arguments is 'None'.
        # with out 'or ""' request will add 'None'.
        company = request.args.get('company') or ""
        client = request.args.get('client') or ""
        phone_number = request.args.get('phone_number') or ""
        order_name = request.args.get('order_name') or ""
        order_term = request.args.get('order_term') or ""
        status = request.args.get('status') or ""
        comments = request.args.get('comments') or ""
        update_date = f'{date_today}'
        
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute('''INSERT INTO orders (company, client, phone_number, order_name,
            order_term, status, comments, update_date) VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)''',
            (company, client, phone_number, order_name,
            order_term, status, comments, update_date,))
        conn.commit()
        conn.close()
        
        return {"New record":f"{company}, {client}, {phone_number}, {order_name}, {order_term}, {status}, {comments}, {update_date}"}
    
    
class update_data(Resource):
    
    @jwt_required()
    def put(self, id):
        data = get_all_data.get(self)
        id_ = id
        
        if id_ in data.keys():
            # replace data to data from SQL if arguments is 'None'.
            # with out 'or data[id]['company']' request will update data to 'None'.
            company = request.args.get('company') or data[id]['company']
            client = request.args.get('client') or data[id]['client']
            phone_number = request.args.get('phone_number') or data[id]['phone_number']
            order_name = request.args.get('order_name') or data[id]['order_name']
            order_term = request.args.get('order_term') or data[id]['order_term']
            status = request.args.get('status') or data[id]['status']
            comments = request.args.get('comments') or data[id]['comments']
            update_date = f'{date_today}'
            
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute('''UPDATE orders SET company = %s, client = %s, phone_number = %s, order_name = %s, 
                        order_term = %s, status = %s, comments = %s, update_date = %s WHERE id = %s''',
                (company, client, phone_number, order_name,
                order_term, status, comments, update_date, id_,))
            conn.commit()
            conn.close()
        
            return {"Updated record":f"{company}, {client}, {phone_number}, {order_name}, {order_term}, {status}, {comments}, {update_date}"}
        
        else:
            abort(404, f"ID:{id_} not Found")
        
        
class delete_data(Resource):
    
    @jwt_required()
    def delete(self, id):
        data = get_all_data.get(self)
        id_ = id
        
        if id_ in data.keys():
            con = psycopg2.connect(**params)
            cur = con.cursor()
            cur.execute(f"DELETE FROM orders WHERE id = {id_}")
            con.commit()
            con.close()
            
            return {"message": f"row with id {id_} was deleted"}
        
        else:
            abort(404, f"ID:{id_} not Found")
    
    
# API endpoints
api.add_resource(get_all_data, "/all_data")
api.add_resource(get_one_item, "/<int:id>")
api.add_resource(add_data, "/add")
api.add_resource(update_data, "/update/<int:id>")
api.add_resource(delete_data, "/delete/<int:id>")


if __name__ == '__main__':
    app.run(debug=True, port=5000)