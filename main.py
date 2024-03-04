from typing import List
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from db import productDB
from model.product import Product
from model.csv import CSVData
from schema.producte import product_schema, products_schema
from typing import Annotated

app = FastAPI()

@app.get("/")  # Retorna un hello world
def read_root():
    return {"Hello": "World"}

@app.get("/product/")  # Llegeix tots els productes i retorna les dades en format JSON
def read_products():
    return product_schema(productDB.consulta())

@app.get("/product/{product_id}")  # Llegeix un producte específic per la seva ID i retorna les seves dades en format JSON
def read_product(product_id: int):
    data = productDB.get_product_by_id(product_id)
    if not data:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_schema(data)

@app.post("/product/")  # Afegeix un nou producte a la base de dades
def create_product(prod: Product):
    success = productDB.insert(prod)
    if success:
        return {"message": "Product added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to add product to database")

@app.put("/product/{product_id}")  # Actualitza les dades d'un producte existent
def update_product(product_id: int, prod: Product):
    success = productDB.update_product(product_id, prod)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully"}

@app.delete("/product/{product_id}")  # Esborra un producte de la base de dades
def delete_product(product_id: int):
    success = productDB.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@app.get("/productAll/")  # Llegeix tots els productes i les seves dades relacionades i retorna la informació en format JSON
def read_products_all():
    return products_schema(productDB.get_all_products())

@app.post("/loadProducts/")  # Carrega massiva de productes, categories i subcategories des d'un fitxer CSV
async def create_upload_file(file: UploadFile):
    productDB.load(file)
    return {"filename": file.filename, "message": "cargado con éxito"}

