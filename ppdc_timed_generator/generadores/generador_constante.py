import datetime as dt
from collections.abc import Callable
from typing import Any

from ppdc_timed_generator.generador import Generador


class GeneradorConstante(Generador):
    """Generador que produce un número fijo de clientes por minuto.
    
    La cantidad de clientes por minuto se calcula como un porcentaje fijo
    de la población total dividido por los minutos de operación del día.
    Este generador es determinista y produce exactamente la misma cantidad
    de clientes por minuto cada vez que se llama.
    """

    def generar_clientes(
        self,
        minutos: int,
        constructor: Callable[[int, dt.datetime], Any],
        update: bool = True,
    ) -> list[Any]:
        if update:
            self.current_datetime += dt.timedelta(minutes=minutos)

        # Queremos generar exactamente 20% de la población en todo el día,
        # así que dividimos por los minutos de operación para tener una tasa constante
        clientes_por_dia = self.poblacion * 0.2
        clientes_por_minuto = clientes_por_dia / self.minutos_de_funcionamiento()
        
        # La cantidad total será proporcional a los minutos transcurridos
        size = int(minutos * clientes_por_minuto)
        
        clientes = []
        for _ in range(size):
            # Usamos random solo para generar IDs únicos, no para la cantidad
            val = self.rdm.randint(0, 2_000_000)
            cliente = constructor(val, self.current_datetime)
            clientes.append(cliente)
        
        return clientes