from db import clientPS
import pandas as pd

def consulta():
    try:
        conn = clientPS.client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM product")
        data = cur.fetchone()
    except Exception as e:
        print(f"error de conexió: {e}")
        return None
    finally:
        conn.close()
    return data


def insert(prod):
    try:
        conn = clientPS.client()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO public.product(product_id, name, description, company, price, units, subcategory_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            RETURNING product_id
            """, 
            (prod.id, prod.name, prod.description, prod.company, prod.price, prod.units, prod.subcategory_id)
        )
        inserted_id = cur.fetchone()[0]  
        conn.commit()
       
    except Exception as e:
        print(f"Error de conexión: {e}")

        return None
    finally:
        
            conn.close()

    return inserted_id

def update_product(product_id, prod):
    try:
        conn = clientPS.client()
        cur = conn.cursor()
        cur.execute("""
            UPDATE product 
            SET 
                name = %s, 
                description = %s, 
                company = %s, 
                price = %s, 
                units = %s, 
                subcategory_id = %s, 
                updated_at = CURRENT_TIMESTAMP 
            WHERE product_id = %s
            """, 
            (prod.name, prod.description, prod.company, prod.price, prod.units, prod.subcategory_id, product_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"error de conexión: {e}")
        return False

def delete_product(product_id):
    try:
        conn = clientPS.client()
        cur = conn.cursor()
        cur.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"error de conexión: {e}")
        return False

def get_product_by_id(id:int):
    try:
        conn = clientPS.client()
        cur = conn.cursor()
        cur.execute(f"select * from product where product_id = {id}")
        data = cur.fetchone()

    except Exception as e:
                print(f"error de conexión: {e}")

    finally:
         conn.close()

    return data


def get_all_products():
    try:
        conn = clientPS.client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM product")
        data = cur.fetchall()
        
        
    except Exception as e:
        print(f"error de conexió: {e}")
        return None
    finally:
        
        conn.close()

    return data

        
# PART 2 LLEGIR I TRACTAR CSV

def load (file):
     #llegir fitxer
     dadesCSV = pd.read_csv(file.file, header=0)
     for index, row in dadesCSV.iterrows():
          #per cada fila passem a un diccionari
          fila=row.to_dict()
          #per cada entitat agafem els seus valors
          getCategory(fila["id_categoria"], fila["nom_categoria"])
          getSubCategory(fila["id_subcategoria"], fila["nom_subcategoria"])


def getCategory(id, name):
     print( f"id: {id} i la categoria: {name}")


def getSubCategory(id, name):
     print( f"id: {id} i la subcategoria: {name}")