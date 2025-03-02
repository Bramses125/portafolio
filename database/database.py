import psycopg2

def connect():
    return psycopg2.connect(
        host="localhost",
        database="perfumes_api_rest",
        user="postgres",
        password="1234"
    )
   