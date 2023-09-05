def repeatPassword(password: str, prefix:str="") -> bool:
    # Ask for password
    aux = str(input(f"Repita la contraseña {prefix}: "))

    # Compare passwords
    if aux != password:
        print("Las contraseñas no son iguales, vuelva a intentarlo")
        return False

    return True
