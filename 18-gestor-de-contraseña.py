import sqlite3
import secrets
import string

#conexión a la base de datos
conn = sqlite3.connect('passwords.db')
c = conn.cursor()

#crear una tabla si no existe
c.execute('''CREATE TABLE IF NOT EXISTS passwords
            (id INTEGER PRIMARY KEY, website TEXT, username TEXT, password TEXT)''')

#función para crear una contraseña segura
def generate_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

#función para guardar una contraseña en la base de datos
def save_password(website, username, password):
    c.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)", (website, username, password))
    conn.commit()

#función para buscar una contraseña por sitio web y usuario
def get_password(website, username):
    c.execute("SELECT password FROM passwords WHERE website=? AND username=?", (website, username))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return None
    
#ejemplo de uso
website = input("Ingrese el sitio web: ")
username = input("Ingrese el nombre de usuario: ")

#busca si ya existe una contraseña para este sitio y usuario
existing_password = get_password(website, username)

if existing_password:
    print("La contraseña ya existe en la base de datos:", existing_password)
else:
    #generar una nueva contraseña
    new_password = generate_password()
    print("Se ha generado una nueva contraseña segura para el sitio web:", new_password)

    #guardar en la base de datos
    save_password(website, username, new_password)
    print("La contraseña se ha guardado con éxito en la base de datos")

#cerrar la conexión a la base de datos
conn.close()
