import tornado.web
from db import get_connection
import json

class ResultsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
        self.set_header("Access-Control-Allow-Headers", "*")

    def options(self):
        self.set_status(204)
        self.finish()
    
    async def get(self):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * From Results")
            results = cursor.fetchall()
        conn.close()
        self.write(json.dumps(results))

    async def post(self):
        data = json.loads(self.request.body)
        name = data["name"]
        roll_number = data["roll_number"]
        department = data["department"]
        subject = data["subject"]
        marks = data["marks"]

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM Results WHERE roll_number = %s",(roll_number,)
            )
            existing = cursor.fetchone()
            if existing:
                self.set_status(400)
                self.write(json.dumps({"message": "Roll number already exists"}))
                conn.close()
                return

            cursor.execute(
                "INSERT INTO Results (name, roll_number, department, subject, marks) VALUES (%s, %s, %s, %s, %s)",
                (name, roll_number, department, subject, marks)
            )
            conn.commit()
        conn.close()
        self.write(json.dumps({message: "Result added succesfully"}))

class DeleteResultsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "OPTIONS, DELETE")
        self.set_header("Access-Control-Allow-Headers", "*")

    def options(self, id):
        self.set_status(204)
        self.finish()
    
    async def delete(self, id):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Results WHERE roll_number = %s", (id,))
            conn.commit()
        conn.close()
        self.write(json.dumps({message: "Result deleted successfully"}))