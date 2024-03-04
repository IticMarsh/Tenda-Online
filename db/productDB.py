from db import clientPS
import pandas as pd

def consulta():
    try:
        conn = clientPS.client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM product")
        data = cur.fetchall()
    except Exception as e:
        print(f"Failed to connect: {e}")
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
        print(f"Failed to connect: {e}")

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
        print(f"Failed to connect: {e}")
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
        print(f"Failed to connect: {e}")
        return False

def get_product_by_id(id:int):
    try:
        conn = clientPS.client()
        cur = conn.cursor()
        cur.execute(f"select * from product where product_id = {id}")
        data = cur.fetchone()

    except Exception as e:
                print(f"Failed to connect: {e}")

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
        print(f"Failed to connect: {e}")
        return None
    finally:
        
        conn.close()

    return data

        
# PART 2 LLEGIR I TRACTAR CSV

#Funció principal
def load(file):
    try:
        conn = clientPS.client()
        dadesCSV = pd.read_csv(file.file, header=0)

        with conn.cursor() as cur:
            for index, row in dadesCSV.iterrows():
                fila = row.to_dict()
                category_id = get_or_create_category(conn, fila["id_categoria"], fila["nom_categoria"])
                subcategory_id = get_or_create_subcategory(conn, fila["id_subcategoria"], fila["nom_subcategoria"], fila["id_categoria"])
                product_id = get_or_update_product(conn, fila["id_producto"], fila["nom_producto"], fila["descripcion_producto"], fila["companyia"], fila["precio"], fila["unidades"], subcategory_id)

        conn.commit()
        return {"message": "CSV imported succesfully"}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()
#funcions per categories i subcategories
def get_or_create_category(conn, id, name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM category WHERE category_id = %s", (id,))
    existing_category = cur.fetchone()
    if existing_category:
        cur.execute("UPDATE category SET name = %s, updated_at = CURRENT_TIMESTAMP WHERE category_id = %s", (name, id))
    else:
        cur.execute("INSERT INTO category(category_id, name, created_at, updated_at) VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", (id, name))
    return id


def get_or_create_subcategory(conn, id, name, category_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM subcategory WHERE subcategory_id = %s", (id,))
    existing_subcategory = cur.fetchone()
    if existing_subcategory:
        cur.execute("UPDATE subcategory SET name = %s, category_id = %s, updated_at = CURRENT_TIMESTAMP WHERE subcategory_id = %s", (name, category_id, id))
    else:
        cur.execute("INSERT INTO subcategory(subcategory_id, name, category_id, created_at, updated_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", (id, name, category_id))
    return id

def get_or_update_product(conn, id, name, description, company, price, units, subcategory_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM product WHERE product_id = %s", (id,))
    existing_product = cur.fetchone()
    if existing_product:
        cur.execute("UPDATE product SET name = %s, description = %s, company = %s, price = %s, units = %s, subcategory_id = %s, updated_at = CURRENT_TIMESTAMP WHERE product_id = %s", (name, description, company, price, units, subcategory_id, id))
    else:
        cur.execute("INSERT INTO product(product_id, name, description, company, price, units, subcategory_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", (id, name, description, company, price, units, subcategory_id))
    return id
