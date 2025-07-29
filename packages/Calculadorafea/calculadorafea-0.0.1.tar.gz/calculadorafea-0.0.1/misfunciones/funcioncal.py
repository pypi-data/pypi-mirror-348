"se encarga de la parte operativa"


def operar(o):
    "provoca la operacion"
    h = str(o).capitalize()

    print(f'operación recibida = {h}')
    print(' ')
    numero1 = int(input(f'ingrese un numero: '))
    numero2 = int(input(f'ingrese otro numero: '))
    print(' ')
    print('Este es el resultado espero haberte ayudado:')
    print(' ')
    if o == 'DIVISION':
        if numero2 == 0:
            return 'Lamentablemente no puedo ayudarte, la division por cero no es valida. Intenta con otra cosa.'
        else:
            return (numero1 / numero2)
    elif o == 'MULTIPLICACION':
        return (numero1 * numero2)
    elif o == 'RESTA':
        return (numero1 - numero2)
    elif o == 'SUMA':
        return (numero1 + numero2)
    else:
        return 'Lamentablemente si te equivocas escribiendo la operación no puedo darte un resultado, intentalo de nuevo.'
    print(' ')
