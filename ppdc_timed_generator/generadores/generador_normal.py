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
