import psycopg2

conn = psycopg2.connect(user="demo_user2",
                        password="123456",
                        host="localhost",
                        port="5432",
                        database="agv_database2")