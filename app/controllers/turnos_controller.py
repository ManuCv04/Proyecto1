"""Controlador Flask para sistema hospitalario."""

from __future__ import annotations

from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

turnos_bp = Blueprint("turnos", __name__)


def _sistema():

    return current_app.extensions["sistema_turnos"]


def _archivo_estado():

    return str(
        Path(current_app.root_path).parent
        / "data"
        / "estado_turnos.json"
    )


@turnos_bp.get("/")
def inicio():

    sistema = _sistema()

    return render_template(

        "index.html",

        nombre_servicio=sistema.nombre_servicio,

        cola=sistema.ver_cola(),

        historial=sistema.historial(),

        paciente_actual=sistema.paciente_actual,

        tiempo_restante=sistema.tiempo_restante,

        simulacion_activa=sistema.simulacion_activa,
    )


@turnos_bp.post("/turnos")
def tomar_turno():

    nombre = request.form.get(
        "nombre",
        ""
    ).strip()

    prioridad = request.form.get(
        "prioridad",
        ""
    ).strip()

    categoria = request.form.get(
        "categoria",
        ""
    ).strip()

    if not nombre:

        flash(
            "Debe ingresar el nombre del paciente.",
            "error",
        )

        return redirect(
            url_for("turnos.inicio")
        )

    try:

        numero = _sistema().tomar_turno(

            nombre=nombre,

            prioridad=prioridad,

            categoria=categoria,
        )

        flash(
            f"Paciente registrado: {numero}",
            "success",
        )

    except Exception as exc:

        flash(
            str(exc),
            "error",
        )

    return redirect(
        url_for("turnos.inicio")
    )


@turnos_bp.post("/iniciar")
def iniciar_simulacion():

    _sistema().iniciar_simulacion()

    flash(
        "Simulación iniciada.",
        "success"
    )

    return redirect(
        url_for("turnos.inicio")
    )


@turnos_bp.post("/detener")
def detener_simulacion():

    _sistema().detener_simulacion()

    flash(
        "Simulación detenida.",
        "warning"
    )

    return redirect(
        url_for("turnos.inicio")
    )


@turnos_bp.get("/api/estado")
def estado():

    sistema = _sistema()

    sistema.actualizar_simulacion()

    return jsonify({

        "paciente_actual":
            sistema.paciente_actual,

        "tiempo_restante":
            sistema.tiempo_restante,

        "cola":
            sistema.ver_cola(),

        "historial":
            sistema.historial(),

        "simulacion_activa":
            sistema.simulacion_activa,

    })


@turnos_bp.post("/guardar")
def guardar_estado():

    ruta = _archivo_estado()

    try:

        _sistema().guardar_estado(ruta)

        flash(
            "Estado guardado correctamente.",
            "success",
        )

    except Exception as exc:

        flash(
            f"Error al guardar: {exc}",
            "error",
        )

    return redirect(
        url_for("turnos.inicio")
    )


@turnos_bp.post("/cargar")
def cargar_estado():

    ruta = _archivo_estado()

    try:

        sistema = _sistema().cargar_estado(ruta)

        current_app.extensions[
            "sistema_turnos"
        ] = sistema

        flash(
            "Estado restaurado correctamente.",
            "success",
        )

    except FileNotFoundError:

        flash(
            "No existe un archivo guardado.",
            "warning",
        )

    except Exception as exc:

        flash(
            f"Error: {exc}",
            "error",
        )

    return redirect(
        url_for("turnos.inicio")
    )