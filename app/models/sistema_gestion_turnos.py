"""Modelo de dominio para gestionar turnos en una institucion."""

from __future__ import annotations

from collections import deque
from datetime import datetime
import json
from pathlib import Path
from typing import Deque


class SistemaGestionTurnos:
    """
    Sistema de turnos con cola normal y cola prioritaria.

    La cola prioritaria siempre se atiende antes que la normal.
    """

    def __init__(self, nombre_servicio: str):
        if not nombre_servicio or not nombre_servicio.strip():
            raise ValueError("El nombre del servicio no puede estar vacio.")

        self.nombre_servicio = nombre_servicio.strip()
        self._cola_normal: Deque[dict] = deque()
        self._cola_prioritaria: Deque[dict] = deque()
        self._historial_atendidos: list[dict] = []
        self._contador_normal = 0
        self._contador_prioritario = 0

    def tomar_turno(self, nombre: str, prioritario: bool = False) -> str:
        """
        Asigna un numero de turno al cliente.

        Retorna el numero asignado (ej: 'T-001' o 'P-001' para prioritario).
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del cliente no puede estar vacio.")

        nombre_limpio = nombre.strip()
        if prioritario:
            self._contador_prioritario += 1
            numero = f"P-{self._contador_prioritario:03d}"
        else:
            self._contador_normal += 1
            numero = f"T-{self._contador_normal:03d}"

        turno = {
            "turno": numero,
            "nombre": nombre_limpio,
            "prioritario": prioritario,
            "hora_toma": datetime.now().isoformat(timespec="seconds"),
        }

        if prioritario:
            self._cola_prioritaria.append(turno)
        else:
            self._cola_normal.append(turno)

        return numero

    def atender_siguiente(self) -> dict | None:
        """
        Atiende al siguiente cliente (prioritario primero).

        Retorna datos del cliente atendido, o None si no hay turnos.
        """
        if self._cola_prioritaria:
            atendido = self._cola_prioritaria.popleft()
        elif self._cola_normal:
            atendido = self._cola_normal.popleft()
        else:
            return None

        atendido["hora_atencion"] = datetime.now().isoformat(timespec="seconds")
        self._historial_atendidos.append(atendido)
        return atendido

    def ver_cola(self) -> list:
        """Retorna la lista de turnos pendientes."""
        return list(self._cola_prioritaria) + list(self._cola_normal)

    def historial(self, n: int = 10) -> list:
        """Retorna los ultimos n atendidos (desde la pila de historial)."""
        if n <= 0:
            return []
        return list(reversed(self._historial_atendidos[-n:]))

    def guardar_estado(self, archivo: str) -> None:
        """Persiste el estado completo en JSON."""
        ruta = Path(archivo)
        if ruta.parent and not ruta.parent.exists():
            ruta.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "nombre_servicio": self.nombre_servicio,
            "contador_normal": self._contador_normal,
            "contador_prioritario": self._contador_prioritario,
            "cola_normal": list(self._cola_normal),
            "cola_prioritaria": list(self._cola_prioritaria),
            "historial_atendidos": self._historial_atendidos,
        }

        with ruta.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def cargar_estado(cls, archivo: str) -> "SistemaGestionTurnos":
        """Restaura el estado desde JSON."""
        ruta = Path(archivo)
        if not ruta.exists():
            raise FileNotFoundError(f"No existe el archivo: {archivo}")

        with ruta.open("r", encoding="utf-8") as f:
            data = json.load(f)

        instancia = cls(data["nombre_servicio"])
        instancia._contador_normal = int(data.get("contador_normal", 0))
        instancia._contador_prioritario = int(data.get("contador_prioritario", 0))
        instancia._cola_normal = deque(data.get("cola_normal", []))
        instancia._cola_prioritaria = deque(data.get("cola_prioritaria", []))
        instancia._historial_atendidos = data.get("historial_atendidos", [])
        return instancia
