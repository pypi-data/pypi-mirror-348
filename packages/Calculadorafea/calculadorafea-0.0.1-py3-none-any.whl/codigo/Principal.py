# Programa para hacer una calculadora asistida
# pedir nombre de usuario
# que opoeracion quiere hacer
# datos
# salutacion
from misfunciones import funcionsaludar, funcioncal
Nombre = input(f'Usario deme su nombre porfavor: ')
print(' ')
print(funcionsaludar.saludar(Nombre))
print(' ')
# datos
Otra_operacion = input('¿Desea realizar operación? (Si o No): ')
Otra_operacion = Otra_operacion.strip().capitalize()
print(' ')
while Otra_operacion == "Si":
    operación = input(f'{Nombre} Ingrese el tipo de operación aqui: ').upper()
    print(' ')
    # operaciones
    print(funcioncal.operar(operación))
    print(" ")
    Otra_operacion = input('¿Desea realizar operación? (Si o No): ')
    Otra_operacion = Otra_operacion.strip().capitalize()
    print(" ")
    if Otra_operacion == "No":
        break
