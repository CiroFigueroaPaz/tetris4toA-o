import time
import pygame
import random
import copy
from pathlib import Path

# =================================
# 1. INICIALIZAR PYGAME
# =================================

pygame.init()
pygame.font.init()


CARPETA_JUEGO = Path(__file__).resolve().parent
rutaFuente = CARPETA_JUEGO / "PressStart2P.ttf"
fuente = pygame.font.Font(str(rutaFuente), 20)

game_over = False
nivel = 0
nivelConfig = nivel
cantidaddeFilasEliminadas = 0
puntaje = 0
puntajeaMostrar = puntaje
colorFlash = 255,255,255
# Variables de Animación
animacion_eliminacion = False
filas_completas = []
tiempo_animacion = 0
DURACION_ANIMACION = 420
pausado = False

# Configuración de la ventana
ANCHO = 650
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
GRIS = (30, 30, 30)
OTROGRIS = (128, 128, 128)
GRISFONDO = (164, 164, 164)
GRISCLARO = (210, 210, 210)

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
    fuente_texto = pygame.font.Font("PressStart2P.ttf", 15)
    texto = fuente_texto.render(
        f"Puntos: {puntajeaMostrar}",
        True,
        BLANCO
    )

    pantalla.blit(texto, (400, 280))

def dibujar_gameOver():
    fuente_game_over = pygame.font.Font("PressStart2P.ttf", 30)

    texto = fuente_game_over.render(
        f"Game Over",
        True,
        (255, 0, 0)
    )
    rectangulo = texto.get_rect(center=(ANCHO // 2, ALTO  // 2))
    pantalla.blit(texto, rectangulo)

def dibujar_puntajeFinal():
    fuente_texto = pygame.font.Font("PressStart2P.ttf", 20)

    texto = fuente_texto.render(
        f"Puntaje Final: {puntaje}",
        True,
        (255, 255, 255)
    )
    rectangulo = texto.get_rect(center=(ANCHO // 2, (ALTO  // 2) + 50))
    pantalla.blit(texto, rectangulo)


def dibujar_texto(texto, x, y, tamaño):
    fuente_texto = pygame.font.Font("PressStart2P.ttf", tamaño)
    texto = fuente_texto.render(
        f"{texto}",
        True,
        BLANCO
    )

    pantalla.blit(texto, (x, y))

def dibujar_nivel():
    fuente_texto = pygame.font.Font("PressStart2P.ttf", 15)
    texto = fuente_texto.render(
        f"Nivel: {nivel}",
        True,
        BLANCO
    )

    pantalla.blit(texto, (400, 217))

# Cambiar Puntaje

def cambiar_puntaje(filas):
    global puntaje
    if nivel == 0:
        if filas == 1:
            puntaje = puntaje + (40 * (nivel + 1))
        elif filas == 2:
            puntaje = puntaje + (100 * (nivel + 1))
        elif filas == 3:
            puntaje = puntaje + (300 * (nivel + 1))
        elif filas == 4:
            puntaje = puntaje + (1200 * (nivel + 1))
    else:
        if filas == 1:
            puntaje = puntaje + (40 * (nivel))
        elif filas == 2:
            puntaje = puntaje + (100 * (nivel))
        elif filas == 3:
            puntaje = puntaje + (300 * (nivel))
        elif filas == 4:
            puntaje = puntaje + (1200 * (nivel))
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

# Corregir la configuracion de niveles

# Detectar filas completas
def detectar_filas_completas():
    filas = []

    for i, fila in enumerate(tablero):
        if all(casilla is not None for casilla in fila):
            filas.append(i)

    return filas

# Eliminar filas

def eliminar_filas():
    global tablero, cantidaddeFilasEliminadas

    filas_originales = len(tablero)

    tablero = [
        fila for fila in tablero
        if not all(casilla is not None for casilla in fila)
    ]

    filas_eliminadas = filas_originales - len(tablero)

    while len(tablero) < FILAS:
        tablero.insert(0, [None for _ in range(COLUMNAS)])
    cantidaddeFilasEliminadas += 1
    print("Cantidad de Filas Eliminadas:" + str(cantidaddeFilasEliminadas))
    return filas_eliminadas

# Dibujar tablero

def dibujar_tablero():
    # 0. Dibujar Fondo

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (120, 45, COLUMNAS * TAM_CELDA, FILAS * TAM_CELDA)
    )

    # 1. Dibujar los bloques fijos
    for fila in range(FILAS):
        for columna in range(COLUMNAS):

            x = columna * TAM_CELDA + 120
            y = fila * TAM_CELDA + 45

            color = tablero[fila][columna]

            if color is not None:

                pygame.draw.rect(
                    pantalla,
                    color,
                    (x, y, TAM_CELDA, TAM_CELDA)
                )

    # 2. Dibujar la cuadrícula al final
    for fila in range(FILAS):
        for columna in range(COLUMNAS):

            x = columna * TAM_CELDA + 120
            y = fila * TAM_CELDA + 45

            pygame.draw.rect(
                pantalla,
                GRIS,
                (x, y, TAM_CELDA, TAM_CELDA),
                1
            )

# Dibujar Animación

def dibujar_animacion_eliminacion():

    if animacion_eliminacion:

        for fila in filas_completas:
            for columna in range(COLUMNAS):

                x = columna * TAM_CELDA + 120
                y = fila * TAM_CELDA + 45

                pygame.draw.rect(
                    pantalla,
                    colorFlash,
                    (x, y, TAM_CELDA, TAM_CELDA)
                )

# Dibujar pieza

def dibujar_pieza(pieza):

    forma = pieza["forma"]
    color = pieza["color"]

    for fila in range(len(forma)):

        for columna in range(len(forma[fila])):

            if forma[fila][columna] == 1:

                x = (pieza["x"] + columna) * TAM_CELDA + 120
                y = (pieza["y"] + fila) * TAM_CELDA + 45

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


# Cambiar config del nivel
def cambiar_nivel():
    global VELOCIDAD_CAIDA
    if nivel <= 1:
        return nivel
    else:
        VELOCIDAD_CAIDA -= 50
        print(VELOCIDAD_CAIDA)


# Bucle

ejecutando = True

while ejecutando:
    if puntaje >= 99999:
        puntajeaMostrar = 99999
    else:
        puntajeaMostrar = puntaje


    # Detectar Controles
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
            if not animacion_eliminacion and not game_over:
                pausado = not pausado

                if not pausado:
                    ultimo_movimiento = pygame.time.get_ticks()
        elif evento.type == pygame.KEYDOWN and not animacion_eliminacion and not game_over and not pausado:
            
            
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

        # SoftDrop
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
            
            #rotar la pieza
            elif evento.key == pygame.K_UP:

                rotar_pieza(pieza_actual)

            # Hard Drop
            elif evento.key == pygame.K_SPACE:

                while movimiento_valido(
                    pieza_actual,
                    pieza_actual["x"],
                    pieza_actual["y"] + 1
                ):
                    pieza_actual["y"] += 1
                    puntaje += 2

                # Colocar la pieza
                fijar_pieza(pieza_actual)

                # Detectar filas completas
                filas_completas = detectar_filas_completas()

                if filas_completas:
                    animacion_eliminacion = True
                    tiempo_animacion = pygame.time.get_ticks()

                else:
                    nueva_pieza()

                # Reiniciar el contador de caída
                ultimo_movimiento = pygame.time.get_ticks()
 
    # Obtener el tiempo actual
    tiempo_actual = pygame.time.get_ticks()

    # Comprobar si pasó el tiempo necesario
    if not animacion_eliminacion and not game_over and not pausado:

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


    if nivel < 1: 
        if cantidaddeFilasEliminadas >= 5:
            nivel += 1
            cantidaddeFilasEliminadas = 0
 
            cambiar_nivel()
    else:
        if cantidaddeFilasEliminadas >= 5 * nivel:
            nivel += 1
            cantidaddeFilasEliminadas = 0
 
            cambiar_nivel()


    # Limpiar pantalla
    pantalla.fill(GRISFONDO)

    # Dibujar pieza actual

    pygame.draw.rect(pantalla, OTROGRIS, (113, 41, (COLUMNAS * TAM_CELDA) + 12, (FILAS * TAM_CELDA) + 12))   
    pygame.draw.rect(pantalla, GRISCLARO, (115, 40, (COLUMNAS * TAM_CELDA) + 10, (FILAS * TAM_CELDA) + 10))
    dibujar_tablero()
    if not game_over:
        dibujar_pieza(pieza_actual)
    dibujar_animacion_eliminacion()

    pygame.draw.rect(pantalla, GRISCLARO, (385, 260, 220, 60))
    pygame.draw.rect(pantalla, NEGRO, (390, 265, 210, 50))
    dibujar_puntaje()

    pygame.draw.rect(pantalla, GRISCLARO, (385, 195, 170, 60))
    pygame.draw.rect(pantalla, NEGRO, (390, 200, 160, 50))

    dibujar_nivel()

    pygame.draw.rect(pantalla, GRISCLARO, (385, 45, 170, 145))
    pygame.draw.rect(pantalla, NEGRO, (390, 50, 160, 135))
    dibujar_texto("Siguiente\n  Pieza", 400, 150, 15)
    dibujar_pieza_siguiente()

    pygame.draw.rect(pantalla, GRISCLARO, (10, 570, 380, 110))
    pygame.draw.rect(pantalla, NEGRO, (15, 575, 370, 100))
    dibujar_texto("\n Mover pieza: Izq y Dcha \n Soft Drop: Abajo \n Hard Drop: Espacio \n Rotar: Arriba \n Pausar: P", 10, 570, 15)

    
    if pausado:

        # Crear una superficie transparente
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(150)
        overlay.fill(NEGRO)

        pantalla.blit(overlay, (0, 0))

        pygame.draw.rect(pantalla, GRISCLARO, (170, 270, 170, 60))
        pygame.draw.rect(pantalla, NEGRO, (175, 275, 160, 50))
        
        # Mostrar el texto PAUSA
        texto_pausa = fuente.render("PAUSA", True, BLANCO)

        rect_texto = texto_pausa.get_rect(center=(250, 300))

        pantalla.blit(texto_pausa, rect_texto)

    if game_over:
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(150)
        overlay.fill(NEGRO)

        pantalla.blit(overlay, (0, 0))
        dibujar_gameOver()
        dibujar_puntajeFinal()
        dibujar_texto("    Presiona Enter \n para cerrar el juego", 150, 500, 15)
        print("Se Termino el juego")
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            break
            

    
    # Actualizar pantalla
    pygame.display.update()

    # FPS
    reloj.tick(60)


# cerrar pygame

pygame.quit()
