import typer
from typing import List, Optional

app = typer.Typer()

# Que las contraseñas sean una clase, ver si es rentable convertir todas las que tengamos en la db para poder buscarlas mas rapido
# o una a una, eso esta por verse.
# Que el usuario al generar una password la pueda guardar inmediatamente agregando los tags.

# En el JSON dejar un tiempo de actividad, se inicia en 0 y ir cambiandolo, o podriamos dejar la fecha actual, 
# y si la siguiente vez supera una cantidad de tiempo definida, pide la master password de nuevo.

@app.command()
def add(
        password: str = typer.Option(..., help="La contraseña deseada"), 
        tags: List[str] = typer.Option(..., help="Lista con los tags relacionados a la contraseña")
    ):
    '''
    Comando para agregar una password. Debemos otorgarle una password y los tags asociados a esta\n
    Lo que debemos hacer es:
        - Que escriba la password por segunda vez para estar seguro.
        - Que los tags sean validos.
        - Comprobar que no se repitan los tags (fzf) y si se parece mucho preguntar. y permitir cambiarlos
        - Tomar la password y cifrarla.
        - Guardarla en "db"
    '''
    print(password, tags)

@app.command()
def get(tags: List[str]):
    """
    Comando para obtener una password segun sus tags.
    Lo que debemos hacer es:
        - Si no tiene tags permitirle que busque y mostrarle las password que coinciden
        - Si tiene tags mostrarle las password que coinciden.
        - Tiene que haber una opcion para que agregue mas tags a su busqueda.
        - Cuando elija una, mostrarsela en pantalla, ojala que se la pegue en el portapapeles.
    """
    print(tags)

@app.command()
def update(tags: List[str]):
    """
    Comando para poder actualizar una password existente.
    Lo que debemos hacer es:
        - Si no tiene tags permitirle que busque y mostrarle las password que coinciden
        - Si tiene tags mostrarle las password que coinciden.
        - Tiene que haber una opcion para que agregue mas tags a su busqueda.
        - Cuando elija una, ejecutar un proceso similar al que tiene en add.
        - Guardar los cambios en db.
    """
    print(tags)

@app.command()
def delete(tags: List[str]):
    """
    Comando para poder borrar una password existente.
    Lo que debemos hacer es:
        - Si no tiene tags permitirle que busque y mostrarle las password que coinciden
        - Si tiene tags mostrarle las password que coinciden.
        - Tiene que haber una opcion para que agregue mas tags a su busqueda.
        - Cuando elija una, preguntar si de verdad quiere borrarla.
        - Guardar los cambios en db.
    """
    print(tags)

@app.command()
def generate(
        a: Optional[bool], 
        A: Optional[bool], 
        n: Optional[bool], 
        s: Optional[bool], 
        t: Optional[bool], 
        sym: Optional[str], 
        tags: Optional[List[str]]=None, 
        min: int=8, 
        max: int=16, 
    ):
    """
    Comando para poder generar una password segura, viene con distintas opciones para componerla como:
        - a: letras minusculas
        - A: letras mayusculas
        - n: numeros
        - sym: string con simbolos validos para la password
    Se puede definir un minimo y maximo, en caso de que no se haga, se define un rango entre 8-16.
    En caso de que se ejecute solo o con la flag --s crea una contraseña de 16 de largo alfanumerica con mayusculas y ciertos symbolos,
    estos simbolos pueden ser sobrescritos si --sym no esta vacio.
    Si viene con tags definidos, se pasa por el proceso de comprobacion de tags y se agrega automaticamente como una password a la db,
    pero si -t esta definida, no pregunta ni se agrega la nueva password a la db
    
    Lo que debemos hacer:
        - Ver en cual de todos los casos caemos y ejecutar una funcion que se encargue de crear la password.
        - En caso de que las tags no esten definidas, preguntar para agregarla a la db, si -t no esta definida.
        - Mostrar la password
        - En caso de que venga con tags, preguntar si esta bien, si lo esta, procesar como add si no pedir otra.
    """
    print(a, A, n, sym)

@app.command()
def config():
    """
    Comando para configurar la clave maestra para el programa, revisa si esta definida, si lo esta no hace nada, si no
    pregunta por una password, hace que la repitas y define algunas palabras de seguridad extra para poder recuperarla en caso de.
    """
    print("hola")

@app.command()
def change_master():
    """
    Comando para cambiar la clave maestra, ahi vemos si lo hacemos con las palabras de seguridad o con algun otro metodo.
    """
    print("hola 2")

@app.command()
def help():
    """
    Muestra todas las explicaciones de las funciones y sus flags.
    """
    print("hola 3")

if __name__ == "__main__":
    app()
