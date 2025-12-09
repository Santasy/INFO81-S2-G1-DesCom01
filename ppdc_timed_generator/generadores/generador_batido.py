import datetime as dt
from collections.abc import Callable
from typing import Any
from math import ceil

from ppdc_timed_generator.generador import Generador


class GeneradorBatido(Generador):
    """Generador que produce clientes en ráfagas en intervalos regulares.

    En lugar de generar clientes uniformemente o constantemente cada minuto,
    este generador produce todos los clientes en intervalos fijos de tiempo (por ejemplo, cada 15 minutos).
    Fuera de estos intervalos, no se generan clientes.

    [REVISION] La idea estaba clara, pero la utilización de módulo no fue del todo correcta.
    Para crear "impulsos" de generación de clientes, se puede seguir este método:
    1. Guardar el tiempo actual, antes de avanzar los [minutos] especificados.
    2. Contar cuántos minutos faltan para el siguiente "impulso" de creación.
        - Sólo si justo empezamos una batida, crearemos personas.
    3. Si a [minutos] le descontamos lo que faltaba para el siguiente impulso,
        entonces nos bastaba la división del tiempo restante con INTERVALO_BATIDA
        para saber la cantidad de "impulsos" que deben ocurrir.

    Les recomiendo revisen los casos de borde, quizá hay algo que falta corregir.
    - ¿Avanzar 0 minutos?
    - ¿Avanzar 1 minuto?
    - ¿Avanzar INTERVALO_BATIDA?
    - ¿Avanzar INTERVALO_BATIDA + 1?
    - ¿Avanzar INTERVALO_BATIDA - 1?
    - ¿Pasar del horario de funcionamiento?
    """

    INTERVALO_BATIDA = 15  # minutos

    def generar_clientes(
        self,
        minutos: int,
        constructor: Callable[[int, dt.datetime], Any],
        update: bool = True,
    ) -> list[Any]:
        dt_inicio = self.current_datetime
        if update:
            self.current_datetime += dt.timedelta(minutes=minutos)

        # Número total de ráfagas en el día
        minutos_funcionamiento = self.minutos_de_funcionamiento()
        num_batidas = ceil(minutos_funcionamiento / self.INTERVALO_BATIDA)
        clientes_por_batida = int(self.poblacion * 0.2 / num_batidas)

        clientes = []

        # Calcular en qué minuto del día estamos
        minuto_inicio = dt_inicio.hour * 60 + dt_inicio.minute

        # Calcular cuántos minutos faltan para el primer impulso
        minutos_en_batida = minuto_inicio % self.INTERVALO_BATIDA
        if minutos_en_batida == 0:
            # Justo en este momento debe ocurrir un impulso
            minutos_hasta_primer_impulso = 0
        else:
            # Faltan minutos para llegar al siguiente impulso
            minutos_hasta_primer_impulso = (
                self.INTERVALO_BATIDA - minutos_en_batida
            )

        # Calcular cuántos minutos quedan después del primer impulso
        if minutos <= minutos_hasta_primer_impulso:
            # No alcanzamos ningún impulso
            num_batidas_ocurridas = 0
        else:
            minutos_restantes = minutos - minutos_hasta_primer_impulso
            # Contar impulsos: el primero + los intervalos completos restantes
            num_batidas_ocurridas = 1 + (
                minutos_restantes // self.INTERVALO_BATIDA
            )

        # Generar clientes por cada batida que ocurrió
        for _ in range(num_batidas_ocurridas):
            for _ in range(clientes_por_batida):
                val = self.rdm.randint(0, 2_000_000)
                cliente = constructor(val, self.current_datetime)
                clientes.append(cliente)

        return clientes
