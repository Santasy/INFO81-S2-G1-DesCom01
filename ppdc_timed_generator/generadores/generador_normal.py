import datetime as dt
import random
from collections.abc import Callable
from typing import Any
from ppdc_timed_generator.generador import Generador


class GeneradorNormal(Generador):
    def generar_clientes(
        self,
        minutos: int,
        constructor: Callable[[int, dt.datetime], Any],
        update: bool = True,
    ):
        """[Profe Seba] La implementación de esta variación no es del todo correcta.
        Era esperable que, para una distribución normal (que es un concepto complicado),
        lo que cambiara fuera la cantidad (size) de personas generadas en el intervalo.

        La implementación actual utiliza la distribución normal para principalmente crear valores cercanos al 1_000_000,
        lo que, según la forma que tengan para elegir los detinos, podría significar en que los pasajeros
        generarán datos similares. No es algo necesariamente útil para nuestro caso; quizá para esto nos interesaría
        más cambiar la función de generación.


        === Posible corrección ===
        Para corregir esto, era mejor tener una única lista, generada en la construcción de esta clase,
        que tuviera guardada la cantidad de personas para cada instante interesante, utilizando las cantidades
        conseguidas con la distribución normal.

        Ej: Los valores deberían quedar acumulados más cerca del medio:

        self.cantidades = [  0,  50, 100,  400,  600,    400,    100,     50,      0,      0]
        # Para las horas:  7AM, 8AM, 9AM, 10AM, 11AM, 12 hrs, 13 hrs, 14 hrs, 15 hrs, 16 hrs

        Ejemplo de creacion: Si son las 09:00, y se quiere llegar a las 10:30 hrs:
            9AM + 10AM * (30 de 60 minutos) = 100 + 400 * 0.5 = 300
        """
        if update:
            self.current_datetime += dt.timedelta(minutes=minutos)

        # promedio esperable por minuto, igual que uniformemente.
        cpm = self.poblacion * 0.2 / self.minutos_de_funcionamiento()
        size = int(minutos * cpm)

        clientes = []
        # desviacion estandar usada para variar.
        media = 1_000_000
        sigma = 200_000

        for _ in range(size):
            val = int(random.gauss(media, sigma))
            # limitar a un rango valido
            val = min(max(val, 0), 2_000_000)
            cliente = constructor(val, self.current_datetime)
            clientes.append(cliente)

        return clientes
