"""Aplicacion Flask para el sistema de gestion de turnos."""

from __future__ import annotations

import os
from flask import Flask

from app.controllers.turnos_controller import turnos_bp
from app.models.sistema_gestion_turnos import SistemaGestionTurnos


def create_app(nombre_servicio: str = "Banco XYZ") -> Flask:
    """Crea y configura la aplicacion Flask."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-turnos")
    app.extensions["sistema_turnos"] = SistemaGestionTurnos(nombre_servicio)
    app.register_blueprint(turnos_bp)
    return app
