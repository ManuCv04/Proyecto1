from __future__ import annotations

from collections import deque
from datetime import datetime
import json
from pathlib import Path
from typing import Deque


class SistemaGestionTurnos:

    def __init__(self, nombre_servicio: str):

        self.nombre_servicio = nombre_servicio

        self._cola_alta: Deque[dict] = deque()
        self._cola_media: Deque[dict] = deque()
        self._cola_baja: Deque[dict] = deque()

        self._historial_atendidos = []

        self._contador = 0

        self.paciente_actual = None

        self.tiempo_restante = 0

        self.simulacion_activa = False

    def tomar_turno(
        self,
        nombre: str,
        prioridad: str,
        categoria: str,
    ):

        self._contador += 1

        numero = f"T-{self._contador:03d}"

        paciente = {

            "turno": numero,

            "nombre": nombre,

            "prioridad": prioridad,

            "categoria": categoria,

            "hora_toma":
                datetime.now().strftime("%H:%M:%S"),

        }

        if prioridad == "alta":

            self._cola_alta.append(paciente)

        elif prioridad == "media":

            self._cola_media.append(paciente)

        else:

            self._cola_baja.append(paciente)

        return numero

    def iniciar_simulacion(self):

        self.simulacion_activa = True

        if self.paciente_actual is None:

            self.iniciar_atencion()

    def detener_simulacion(self):

        self.simulacion_activa = False

    def iniciar_atencion(self):

        paciente = None

        # PRIORIDAD REAL

        if self._cola_alta:

            paciente = self._cola_alta.popleft()

        elif self._cola_media:

            paciente = self._cola_media.popleft()

        elif self._cola_baja:

            paciente = self._cola_baja.popleft()

        if paciente is None:
            return

        self.paciente_actual = paciente

        # TIEMPO SEGÚN PRIORIDAD

        if paciente["prioridad"] == "alta":

            self.tiempo_restante = 15

        elif paciente["prioridad"] == "media":

            self.tiempo_restante = 10

        else:

            self.tiempo_restante = 5

    def actualizar_simulacion(self):

        if not self.simulacion_activa:
            return

        if self.paciente_actual is None:

            self.iniciar_atencion()
            return

        self.tiempo_restante -= 1

        if self.tiempo_restante <= 0:

            self.paciente_actual[
                "hora_atencion"
            ] = datetime.now().strftime("%H:%M:%S")

            self._historial_atendidos.append(
                self.paciente_actual
            )

            self.paciente_actual = None

            self.iniciar_atencion()

    def ver_cola(self):

        return (

            list(self._cola_alta)

            + list(self._cola_media)

            + list(self._cola_baja)

        )

    def historial(self, n=10):

        return list(
            reversed(
                self._historial_atendidos[-n:]
            )
        )

    def guardar_estado(self, archivo):

        ruta = Path(archivo)

        data = {

            "nombre_servicio":
                self.nombre_servicio,

            "contador":
                self._contador,

            "cola_alta":
                list(self._cola_alta),

            "cola_media":
                list(self._cola_media),

            "cola_baja":
                list(self._cola_baja),

            "historial":
                self._historial_atendidos,

        }

        with ruta.open(
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2,
            )

    @classmethod
    def cargar_estado(cls, archivo):

        ruta = Path(archivo)

        with ruta.open(
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        sistema = cls(
            data["nombre_servicio"]
        )

        sistema._contador = data["contador"]

        sistema._cola_alta = deque(
            data["cola_alta"]
        )

        sistema._cola_media = deque(
            data["cola_media"]
        )

        sistema._cola_baja = deque(
            data["cola_baja"]
        )

        sistema._historial_atendidos = data["historial"]

        return sistema