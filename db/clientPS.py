import psycopg
def client():

    conexio =    """
                dbname=postgres
                user=user_postgres
                password=pass_postgres
                host=localhost
                port=5432
                """
    
    try: 
        # return psycopg.connect(conexio)
       conn = psycopg.connect(conexio)
       return conn
   
    except Exception as e:
     print(f"error conexio {e}")




