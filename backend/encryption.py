from cryptography.fernet import Fernet

PATH = "./"

def generate_key():
    key = Fernet.generate_key()
    with open('{}.env.key'.format(PATH), 'wb') as env_file:
        env_file.write(key)
    return

def read_key():
    with open('{}.env.key'.format(PATH), 'rb') as env_file:
        key = env_file.read()
    return key

def encrypter(password):
    key = read_key()
    cifrado = Fernet(key)
    encriptado = cifrado.encrypt(str.encode(password))
    return encriptado

def decryptor(encriptado):
    key = read_key()
    cifrado = Fernet(key)
    desencriptado_bytes = cifrado.decrypt(encriptado)
    desencriptado = desencriptado_bytes.decode()
    return desencriptado

def compare(password,encriptado):
    key = read_key()
    desencriptado = decryptor(encriptado)
    return password == desencriptado
    
    
#Example
'''
key = generate_key()

password = "olaola123"

encrypted = encrypter(password)

print(encrypted)

decrypted = decryptor(encrypted)
print(decrypted)

print(compare(password,encrypted))
'''