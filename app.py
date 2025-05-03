
import tornado.ioloop
import tornado.web
import tornado.escape
from db import get_connection

class LoginHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()
    
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        username = data.get("username")
        password = data.get("password")

        if username == "admin" and password == "admin":
            self.write({"success": True, "token": "admin-token"})
        else:
            self.set_status(401)
            self.write({"error": "Invalid credentials"})


# GET and POST /results API
class ResultsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  
        self.set_header("Access-Control-Allow-Headers", "Content-Type, X-Requested-With")  
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")  

    def options(self):
        self.set_status(204)  
        self.finish()

    def get(self):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM results ORDER by roll_number")  
                results = cursor.fetchall()
                self.write({"results": results}) 
        finally:
            connection.close()

    def post(self):
        connection = get_connection()
        data = tornado.escape.json_decode(self.request.body)  
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO results (name, roll_number, department, subject, marks)
                VALUES (%s, %s, %s, %s, %s)
                """  
                cursor.execute(sql, (
                    data["name"],
                    data["roll_number"],
                    data["department"],
                    data["subject"],
                    data["marks"]
                ))  
                connection.commit() 
                self.write({"message": "Result added successfully"})  
        finally:
            connection.close()


class UpdateHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  
        self.set_header("Access-Control-Allow-Headers", "Content-Type, X-Requested-With") 
        self.set_header("Access-Control-Allow-Methods", "GET, PUT, OPTIONS")  

    def options(self, roll_number):
        self.set_status(204)  
        self.finish()

    def get(self, roll_number):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM results WHERE roll_number = %s"  
                cursor.execute(sql, (roll_number,))  
                result = cursor.fetchone()  
                if result:
                    self.write(result)  
                else:
                    self.set_status(404)   
                    self.write({"error": "Result not found"})
        finally:
            connection.close()

    def put(self, roll_number):
        connection = get_connection()
        data = tornado.escape.json_decode(self.request.body)  
        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE results
                SET name = %s, roll_number = %s, department = %s, subject = %s, marks = %s
                WHERE roll_number = %s
                """  
                cursor.execute(sql, (
                    data["name"],
                    data["roll_number"],
                    data["department"],
                    data["subject"],
                    data["marks"],
                    roll_number
                ))
                connection.commit()  
                self.write({"message": "Result updated successfully"})  
        finally:
            connection.close()

class DeleteResultsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "DELETE, OPTIONS")

    def options(self, roll_number):
        self.set_status(204)
        self.finish()

    def delete(self, roll_number):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "Delete from results where roll_number = %s"
                cursor.execute(sql, (roll_number,))
                connection.commit()
                self.write({"message": "Result deleted successfully"})
        finally:
            connection.close()        

def make_app():
    return tornado.web.Application([
        (r"/results", ResultsHandler),  
        (r"/results/roll/([a-zA-Z0-9]+)", UpdateHandler),  
        (r"/login", LoginHandler),
        (r"/results/delete/([a-zA-Z0-9]+)", DeleteResultsHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)  
    print("Server is running on http://localhost:8000")  
    tornado.ioloop.IOLoop.current().start()  

