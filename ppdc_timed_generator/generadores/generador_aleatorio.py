import datetime as dt
import random
from collections.abc import Callable
from typing import Any

from ppdc_timed_generator.generador import Generador


class GeneradorAleatorio(Generador):
    def generar_clientes(
        self,
        minutos: int,
        constructor: Callable[[int, dt.datetime], Any],
        update: bool = True,
    ):
        """[Profe Seba] Muy clara la intención, pero la implementación de esta variación tiene un pequeño detalle
        que la vuelve incorrecta.
        Recuerden que existe el criterio de 20% de la población durante el día.
        En el peor caso, con el aleatorio que tienen podrían crearse 0 clientes en todos los momentos,
        y por lo tanto no cumplir con la regla del 20%.


        === Posible corrección ===
        Hay varias formas de solucionar esto:
        - Que al menos se generé el 50% de lo que debería, y el otro 50% pueda existir o no.
        - Que en las últimas horas de funcionamiento no se utilice el random, sino algo fijo que
        permita remontar en la cantidad de personas generadas.
        """
        if update:
            self.current_datetime += dt.timedelta(minutes=minutos)

        cpm = self.poblacion * 0.2 / self.minutos_de_funcionamiento()
        max_clientes = int(minutos * cpm)
        size = random.randint(0, max_clientes)

        clientes = []
        for _ in range(size):
            val = self.rdm.randint(0, 2_000_000)
            cliente = constructor(val, self.current_datetime)
            clientes.append(cliente)

        return clientes
