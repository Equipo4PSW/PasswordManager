import typer
import pyperclip
from typing import List, Optional
from typing_extensions import Annotated
from backend import Db

cli = typer.Typer()
db = Db()

ACCEPT_OPTIONS = ["si", "s", "S", "Si", "SI", "y", "yes", "Y", "YES"]
DENY_OPTIONS = ["no", "n", "N", "No", "NO"]

# Que las contraseñas sean una clase, ver si es rentable convertir todas las que tengamos en la db para poder buscarlas mas rapido
# o una a una, eso esta por verse.
# Que el usuario al generar una password la pueda guardar inmediatamente agregando los tags.

# En el JSON dejar un tiempo de actividad, se inicia en 0 y ir cambiandolo, o podriamos dejar la fecha actual, 
# y si la siguiente vez supera una cantidad de tiempo definida, pide la master password de nuevo.

@cli.command()
def add(
        # password: str = typer.Option(help="La contraseña deseada"), 
        # tags: List[str] = typer.Option(help="Lista con los tags relacionados a la contraseña"),

        password: str,
        tags: List[str],
        verify: bool = typer.Option(False, "--no-verification", "--v", help="Si se incluye se salta la doble verificacion de la contraseña")
    ):
    '''
    Comando para agregar una password. Debemos otorgarle una password y los tags asociados a esta
    '''

    # Repeat password
    if not verify:
        aux = str(input("Repita la contraseña: "))
        if aux != password:
            print("Las contraseñas no son iguales, vuelva a intentarlo")
            return

    db.addDb(password, tags)

    # TODO: Esto deberia estar en las funciones de DB para confirmar bien
    print("Se ha guardado correctamente")

@cli.command()
def get(tags: Annotated[Optional[List[str]], typer.Argument()] = None):
    """
    Comando para obtener una password segun sus tags.
    Lo que debemos hacer es:
        - Si no tiene tags permitirle que busque y mostrarle las password que coinciden
        - Si tiene tags mostrarle las password que coinciden.
        - Tiene que haber una opcion para que agregue mas tags a su busqueda.
        - Cuando elija una, mostrarsela en pantalla, ojala que se la pegue en el portapapeles.
    """
    # print(tags)
    db.getPasswords(tags)


@cli.command()
def search():
    """
    Comando usado para abrir el buscador de contraseñas y poder copiar en el portapapeles la seleccionada
    """

    obj = db.searchPassword('')
    if obj != []:
        pyperclip.copy(obj["password"])
        print("Contraseña pegada en el portapapeles")

@cli.command()
def update(
        tags: Annotated[Optional[List[str]], typer.Argument()] = None,
        password: str = typer.Option('', "--clave", "--password", help="Nueva contraseña utilizada para actualizar"),
        verify: bool = typer.Option(False, "--no-verification", "--v", help="Si se incluye se salta la doble verificacion de la contraseña")
    ):
    """
    Comando para poder actualizar una password existente.
    """

    # Gets a string of tags separated by commas.
    _tags = ",".join(tags)
    
    # Verify if there is a password
    if password == "":
        password = str(input("Ingrese una contraseña: "))

    # Repeat password
    if not verify:
        aux = str(input("Repita la contraseña: "))
        if aux != password:
            print("Las contraseñas no son iguales, vuelva a intentarlo")
            return

    #Get password dict
    obj = db.searchPassword(_tags)
    print(obj)

    db.updateDb(obj, password)

@cli.command()
def delete(
        tags: List[str],
        verify: bool = typer.Option(False, "--no-verification", "--v", help="Si se incluye se salta la doble verificacion para borrar la contraseña")
    ):
    """
    Comando para poder borrar una password existente.
    Lo que debemos hacer es:
        - Si no tiene tags permitirle que busque y mostrarle las password que coinciden
        - Si tiene tags mostrarle las password que coinciden.
        - Tiene que haber una opcion para que agregue mas tags a su busqueda.
        - Cuando elija una, preguntar si de verdad quiere borrarla.
        - Guardar los cambios en db.
    """
    # Gets a string of tags separated by commas.
    _tags = ",".join(tags)

    #Get password dict
    obj = db.searchPassword(_tags)

    if not verify:
        aux = str(input("Estas seguro de borrar la contraseña (si/no): "))
        if aux in ACCEPT_OPTIONS:
            # Delete the password
            db.deleteDb(obj['id'])



@cli.command()
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

@cli.command()
def config():
    """
    Comando para configurar la clave maestra para el programa, revisa si esta definida, si lo esta no hace nada, si no
    pregunta por una password, hace que la repitas y define algunas palabras de seguridad extra para poder recuperarla en caso de.
    """
    
    # Enter password
    password = str(input("Ingrese su contraseña maestra: "))

    # Repeat password
    aux = str(input("Repita la contraseña: "))
    if aux != password:
        print("Las contraseñas no son iguales, vuelva a intentarlo")
        return

    db.addMasterDb(password)

@cli.command()
def remaining():
    """
    Printea cuanto tiempo queda con la contraseña maestra activa
    """

    db.checkTime()








