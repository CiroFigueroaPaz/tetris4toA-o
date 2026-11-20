import time
import pygame
import random
import copy

# =================================
# 1. INICIALIZAR PYGAME
# =================================

pygame.init()
pygame.font.init()

fuente = pygame.font.Font("PressStart2P.ttf", 20)

game_over = False
nivel = 0
puntaje = 0
colorFlash = 255,255,255
# Variables de Animación
animacion_eliminacion = False
filas_completas = []
tiempo_animacion = 0
DURACION_ANIMACION = 420

# Configuración de la ventana
ANCHO = 600
ALTO = 700

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TETRIS - CIRO FIGUEROA")

reloj = pygame.time.Clock()
VEL_CAIDA_CONST = 800
VELOCIDAD_CAIDA = VEL_CAIDA_CONST  # Milisegundos
ultimo_movimiento = pygame.time.get_ticks()
# Colores

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (10, 10, 10)

COLORES = [
    (0, 240, 240),   #Pieza en I
    (240, 240, 0),   #Pieza en cuadrado
    (160, 0, 240),   #Pieza en T
    (0, 240, 0),     #Pieza en S
    (200, 0, 50),     #Pieza en Z
    (0, 50, 200),     #Pieza en J
    (240, 160, 0)    #Pieza en L
]

# Tablero

FILAS = 20
COLUMNAS = 10
TAM_CELDA = 25

tablero = [[None for _ in range(COLUMNAS)]
           for _ in range(FILAS)]
# Formas de las piezas

PIEZAS = [

    # Pieza I
    [[1, 1, 1, 1]],

    # Pieza O
    [[1, 1],
     [1, 1]],

    # Pieza T
    [[0, 1, 0],
     [1, 1, 1]],

    # Pieza S
    [[0, 1, 1],
     [1, 1, 0]],

    # Pieza Z
    [[1, 1, 0],
     [0, 1, 1]],

    # Pieza J
    [[1, 0, 0],
     [1, 1, 1]],

    # Pieza L
    [[0, 0, 1],
     [1, 1, 1]]
]

# Crear una pieza aleqatoria

def crear_pieza():

    indice = copy.deepcopy(random.randint(0, 6))

    pieza = PIEZAS[indice]

    color = COLORES[indice]

    return {
        "forma": pieza,
        "color": color,
        "x": 3,
        "y": 0
    }

# Verificar si se puede mover

def movimiento_valido(pieza, nuevo_x, nuevo_y):

    forma = pieza["forma"]

    for fila in range(len(forma)):

        for columna in range(len(forma[fila])):

            if forma[fila][columna] == 1:

                x = nuevo_x + columna
                y = nuevo_y + fila

                # Comprobar los límites laterales
                if x < 0 or x >= COLUMNAS:
                    return False

                # Comprobar el fondo
                if y >= FILAS:
                    return False

                # Comprobar colisiones con otras piezas
                if y >= 0 and tablero[y][x] is not None:
                    return False

    return True

pieza_siguiente = crear_pieza()
def nueva_pieza():
    global pieza_actual, game_over, pieza_siguiente


    pieza_actual = pieza_siguiente    
    pieza_siguiente = crear_pieza()
    if not movimiento_valido(
        pieza_actual,
        pieza_actual["x"],
        pieza_actual["y"]
    ):
        game_over = True

# Dibujar Puntaje
def dibujar_puntaje():

    texto = fuente.render(
        f"Puntaje: {puntaje}",
        True,
        BLANCO
    )

    pantalla.blit(texto, (10, 10))

def dibujar_gameOver():
    fuente_game_over = pygame.font.Font("PressStart2P.ttf", 30)

    texto = fuente_game_over.render(
        f"Game Over",
        True,
        (255, 0, 0)
    )
    rectangulo = texto.get_rect(center=(ANCHO // 2.5, ALTO  // 2.2))
    pantalla.blit(texto, rectangulo)

def dibujar_texto(texto, x, y, tamaño):
    fuente_texto = pygame.font.Font("PressStart2P.ttf", tamaño)
    texto = fuente_texto.render(
        f"{texto}",
        True,
        BLANCO
    )

    pantalla.blit(texto, (x, y))

# Cambiar Puntaje

def cambiar_puntaje(filas):
    global puntaje
    if filas == 1:
        puntaje = puntaje + (40 * (nivel + 1))
    elif filas == 2:
        puntaje = puntaje + (100 * (nivel + 1))
    elif filas == 3:
        puntaje = puntaje + (300 * (nivel + 1))
    elif filas == 4:
        puntaje = puntaje + (1200 * (nivel + 1))
    print(puntaje)

#Fijar la pieza en el tablero
def fijar_pieza(pieza):

    forma = pieza["forma"]
    color = pieza["color"]

    for fila in range(len(forma)):

        for columna in range(len(forma[fila])):

            if forma[fila][columna] == 1:

                x = pieza["x"] + columna
                y = pieza["y"] + fila

                if 0 <= y < FILAS and 0 <= x < COLUMNAS:
                    tablero[y][x] = color

# Rotar pieza

def rotar_pieza(pieza):

    # Guardar la forma original
    forma_original = pieza["forma"]

    # Crear una copia rotada
    forma_rotada = [
        list(fila)
        for fila in zip(*forma_original[::-1])
    ]

    # Guardar temporalmente la nueva forma
    pieza["forma"] = forma_rotada

    # Comprobar si la rotación es válida
    if not movimiento_valido(
        pieza,
        pieza["x"],
        pieza["y"]
    ):

        # Si no es válida, recuperar la forma original
        pieza["forma"] = forma_original

# Detectar filas completas
def detectar_filas_completas():
    filas = []

    for i, fila in enumerate(tablero):
        if all(casilla is not None for casilla in fila):
            filas.append(i)

    return filas

# Eliminar filas

def eliminar_filas():
    global tablero

    filas_originales = len(tablero)

    tablero = [
        fila for fila in tablero
        if not all(casilla is not None for casilla in fila)
    ]

    filas_eliminadas = filas_originales - len(tablero)

    while len(tablero) < FILAS:
        tablero.insert(0, [None for _ in range(COLUMNAS)])

    return filas_eliminadas

# Dibujar tablero

def dibujar_tablero():

    # 1. Dibujar los bloques fijos
    for fila in range(FILAS):
        for columna in range(COLUMNAS):

            x = columna * TAM_CELDA + 125
            y = fila * TAM_CELDA + 50

            color = tablero[fila][columna]

            if color is not None:

                pygame.draw.rect(
                    pantalla,
                    color,
                    (x, y, TAM_CELDA, TAM_CELDA)
                )

    # 2. Dibujar el parpadeo blanco
    if animacion_eliminacion:

        for fila in filas_completas:
            for columna in range(COLUMNAS):

                x = columna * TAM_CELDA + 125
                y = fila * TAM_CELDA + 50

                pygame.draw.rect(
                    pantalla,
                    colorFlash,
                    (x, y, TAM_CELDA, TAM_CELDA)
                )

    # 3. Dibujar la cuadrícula al final
    for fila in range(FILAS):
        for columna in range(COLUMNAS):

            x = columna * TAM_CELDA + 125
            y = fila * TAM_CELDA + 50

            pygame.draw.rect(
                pantalla,
                GRIS,
                (x, y, TAM_CELDA, TAM_CELDA),
                1
            )


# Dibujar pieza

def dibujar_pieza(pieza):

    forma = pieza["forma"]
    color = pieza["color"]

    for fila in range(len(forma)):

        for columna in range(len(forma[fila])):

            if forma[fila][columna] == 1:

                x = (pieza["x"] + columna) * TAM_CELDA + 125
                y = (pieza["y"] + fila) * TAM_CELDA + 50

                pygame.draw.rect(
                    pantalla,
                    color,
                    (x, y, TAM_CELDA, TAM_CELDA)
                )

                pygame.draw.rect(
                    pantalla,
                    BLANCO,
                    (x, y, TAM_CELDA, TAM_CELDA),
                    1
                )



                pygame.draw.rect(
                    pantalla,
                    BLANCO,
                    (x, y, TAM_CELDA, TAM_CELDA),
                    1
                )

# Dibujar siguiente pieza

def dibujar_pieza_siguiente():
    forma = pieza_siguiente["forma"]
    color = pieza_siguiente["color"]

    tamaño = TAM_CELDA

    inicio_x = 425
    inicio_y = 80

    for fila in range(len(forma)):
        for columna in range(len(forma[fila])):

            if forma[fila][columna] == 1:

                x = inicio_x + columna * tamaño
                y = inicio_y + fila * tamaño

                pygame.draw.rect(
                    pantalla,
                    color,
                    (x, y, tamaño, tamaño)
                )

                pygame.draw.rect(
                    pantalla,
                    BLANCO,
                    (x, y, tamaño, tamaño),
                    1
                )

# Crear primera pieza

nueva_pieza()




# Bucle

ejecutando = True

while ejecutando:

    

    # Comprobar si pasó el tiempo necesario
    
    # Detectar eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        # Detectar teclas
        elif evento.type == pygame.KEYDOWN and not animacion_eliminacion and not game_over:
            
            # Mover a la izquierda
            if evento.key == pygame.K_LEFT:
                VELOCIDAD_CAIDA = 1500
                nuevo_x = pieza_actual["x"] - 1

                if movimiento_valido(
                    pieza_actual,
                   nuevo_x,
                    pieza_actual["y"]
                ):
                    pieza_actual["x"] = nuevo_x

        # Mover a la derecha
            elif evento.key == pygame.K_RIGHT:
                VELOCIDAD_CAIDA = 1500
                nuevo_x = pieza_actual["x"] + 1

                if movimiento_valido(
                    pieza_actual,
                    nuevo_x,
                    pieza_actual["y"]
                ):
                    pieza_actual["x"] = nuevo_x

        # Mover hacia abajo
            elif evento.key == pygame.K_DOWN:
                VELOCIDAD_CAIDA = VEL_CAIDA_CONST
                puntaje = puntaje + 1
                nuevo_y = pieza_actual["y"] + 1

                if movimiento_valido(
                    pieza_actual,
                    pieza_actual["x"],
                    nuevo_y
                ):

                    pieza_actual["y"] = nuevo_y
                    ultimo_movimiento = pygame.time.get_ticks()

                else:
                    if animacion_eliminacion == False:
                        VELOCIDAD_CAIDA = VEL_CAIDA_CONST
                    fijar_pieza(pieza_actual)
                    filas_completas = detectar_filas_completas()
                    if filas_completas:
                        animacion_eliminacion = True
                        tiempo_animacion = pygame.time.get_ticks()
                    else:
                        nueva_pieza()
                # Reiniciar el contador de caída
            

            elif evento.key == pygame.K_UP:

                rotar_pieza(pieza_actual)
 
    # Obtener el tiempo actual
    tiempo_actual = pygame.time.get_ticks()

    # Comprobar si pasó el tiempo necesario
    if not animacion_eliminacion and not game_over:

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - ultimo_movimiento >= VELOCIDAD_CAIDA:

            if movimiento_valido(
                pieza_actual,
                pieza_actual["x"],
                pieza_actual["y"] + 1
            ):
                pieza_actual["y"] += 1

            else:
                fijar_pieza(pieza_actual)

                filas_completas = detectar_filas_completas()

                if filas_completas:
                    animacion_eliminacion = True
                    tiempo_animacion = pygame.time.get_ticks()

                else:
                    nueva_pieza()

            ultimo_movimiento = pygame.time.get_ticks()

    if animacion_eliminacion:

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_animacion <= 100:
            colorFlash = 255,255,255
        elif tiempo_actual - tiempo_animacion <= 200:
            colorFlash = 0,0,0
        elif tiempo_actual - tiempo_animacion <= 300:
            colorFlash = 255,255,255
        else:
            colorFlash = 0,0,0
        if tiempo_actual - tiempo_animacion >= DURACION_ANIMACION:

            filas_eliminadas = eliminar_filas()
            cambiar_puntaje(filas_eliminadas)

            animacion_eliminacion = False
            filas_completas = []

            nueva_pieza()

            ultimo_movimiento = pygame.time.get_ticks()

    # Limpiar pantalla
    pantalla.fill(NEGRO)

    # Dibujar pieza actual
    if not game_over:
        dibujar_pieza(pieza_actual)

    dibujar_tablero()

    dibujar_puntaje()

    dibujar_texto("Siguiente\n  Pieza", 400, 150, 15)
    dibujar_pieza_siguiente()

    if game_over:
        dibujar_gameOver()
        print("Se Termino el juego")
        break
    
    # Actualizar pantalla
    pygame.display.update()

    # FPS
    reloj.tick(60)


# cerrar pygame

pygame.quit()
