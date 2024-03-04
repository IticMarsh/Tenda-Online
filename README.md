# CRUD en Python amb FastAPI i PostgreSQL

Aquest projecte implementa un CRUD (Crear, Llegir, Actualitzar i Esborrar) utilitzant FastAPI com a framework web i PostgreSQL com a base de dades.

## Funcionalitats:

- **Ruta /product GET**: Retorna una llista JSON amb tota la informació dels productes de la taula `products`.
- **Ruta /product/{id} GET**: Retorna un objecte JSON amb la informació del producte la ID del qual coincideix amb la ID proporcionada com a paràmetre.
- **Ruta /product/ POST**: Permet afegir un nou producte a la base de dades i retorna un objecte JSON amb el missatge "S'ha afegit correctament".
- **Ruta /product/{id} PUT**: Permet modificar un producte a la base de dades definit per la ID proporcionada com a paràmetre. Retorna un objecte JSON amb el missatge "S'ha modificat correctament".
- **Ruta /product/{id} DELETE**: Permet eliminar un producte de la base de dades i retorna un objecte JSON amb el missatge "S'ha borrat correctament".
- **Ruta /productAll/ GET**: Retorna una llista JSON amb la següent informació: nom de la categoria, nom de la subcategoria, nom del producte, marca del producte i el preu.

- **Càrrega massiva de productes**:
  - **Ruta /loadProducts POST**: Serveix per fer una càrrega massiva de categories, subcategories i productes a la base de dades a través d'un fitxer CSV.
