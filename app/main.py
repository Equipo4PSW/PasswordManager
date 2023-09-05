import typer
import pyperclip
import random
from typing import List, Optional
from typing_extensions import Annotated
from backend import Db
from backend.passwords import password_generator
from backend.passwords.encryption import generate_key

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
        password: str,
        tags: List[str],
        verify: bool = typer.Option(False, "--no-verification", "--v", help="Si se incluye se salta la doble verificacion de la contraseña")
    ):
    '''
    Comando para agregar una password. Debemos otorgarle una password y los tags asociados a esta
    '''

    # Check if had master pass
    if not db.verifyHandler():
        return

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
    Muestra el buscador con las tags ingresadas
    """

    # Check if had master pass
    if not db.verifyHandler():
        return

    # print(tags)
    db.getPasswords(tags)


@cli.command()
def search():
    """
    Comando usado para abrir el buscador de contraseñas y poder copiar en el portapapeles la seleccionada
    """

    # Check if had master pass
    if not db.verifyHandler():
        return

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
    
    # Check if had master pass
    if not db.verifyHandler():
        return

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
    """

    # Check if had master pass
    if not db.verifyHandler():
        return

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
        a: bool = typer.Option(True, "a", "--minusculas", help="Indica si la contraseña generada tiene minusculas."),
        A: bool = typer.Option(True, "A", "--mayusculas", help="Indica si la contraseña generada tiene mayusculas."),
        n: bool = typer.Option(True, "n", "--numeros", help="Indica si la contraseña generada tiene numeros."),
        sym: str = typer.Option("", "sym", "--simbolos", help="Indica que simbolos puede tener la contraseña."),
        t: bool = typer.Option(False, "--segura", help="Indica si el generador debe generar una contraseña segura (16 largo, alfanumerica con mayusculas sin simbolos)"),
        min: int=8, 
        max: int=16, 
    ):
    """
    Comando para poder generar una password segura, viene con distintas opciones para componerla como:
    """

    while(1):
        # Generate secure password
        if t:
            password = db.passwordGenerator(16, True, True, True)
        else:
            if not sym:
                sym = ""

            size = random.randint(min, max)
            password = db.passwordGenerator(size, a, A, n, sym)

        # Ask for another password
        print(f"La contraseña generada fue: {password}")

        opt = str(input("Desea cambiarla por otra contraseña (y/n): "))
        if opt in DENY_OPTIONS:
            break

    # Copy new password in the clipboard
    pyperclip.copy(password)
    print("Contraseña pegada en el portapapeles")

@cli.command()
def config():
    """
    Comando para configurar la clave maestra para el programa, revisa si esta definida, si lo esta no hace nada, si no
    pregunta por una password, hace que la repitas y define algunas palabras de seguridad extra para poder recuperarla en caso de.
    """
    
    # Generate key for the passwords
    db.generateKey()
    
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
    Imprime en pantalla cuanto tiempo queda con la contraseña maestra activa y es usado para renovar el tiempo con la contraseña activa"
    """

    # Check if had master pass
    if not db.verifyHandler():
        return

    db.checkTime(on_screen=True)
