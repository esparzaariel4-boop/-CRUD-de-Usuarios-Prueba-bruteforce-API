import itertools
import time

username = "admin"
password_real = "ad12"

alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

intentos = 0
inicio = time.time()
encontrada = None

for longitud in range(1, len(password_real) + 1):
    for combinacion in itertools.product(alfabeto, repeat=longitud):
        intento = "".join(combinacion)
        intentos += 1

        print("Intento:", intento)

        if intento == password_real:
            final = time.time()
            encontrada = intento
            break

    if encontrada:
        break

print("\n==============================")
print("Ataque de Fuerza Bruta")
print("==============================")
print("Usuario:", username)
print("Contraseña:", encontrada)
print("Intentos realizados:", intentos)
print("Tiempo:", round(final - inicio, 4), "segundos")