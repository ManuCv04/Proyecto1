"""Controlador Flask para exponer acciones del sistema de turnos."""

from __future__ import annotations

from pathlib import Path

from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for


turnos_bp = Blueprint("turnos", __name__)


def _sistema():
    return current_app.extensions["sistema_turnos"]


def _archivo_estado() -> str:
    return str(Path(current_app.root_path).parent / "data" / "estado_turnos.json")


@turnos_bp.get("/")
def inicio():
    sistema = _sistema()
    return render_template(
        "index.html",
        nombre_servicio=sistema.nombre_servicio,
        cola=sistema.ver_cola(),
        historial=sistema.historial(10),
    )


@turnos_bp.post("/turnos")
def tomar_turno():
    nombre = request.form.get("nombre", "")
    prioritario = request.form.get("prioritario", "false").lower() == "true"
    try:
        numero = _sistema().tomar_turno(nombre=nombre, prioritario=prioritario)
        flash(f"Turno asignado correctamente: {numero}", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    return redirect(url_for("turnos.inicio"))


@turnos_bp.post("/atender")
def atender_siguiente():
    atendido = _sistema().atender_siguiente()
    if atendido is None:
        flash("No hay turnos pendientes.", "warning")
    else:
        flash(f"Atendido: {atendido['turno']} - {atendido['nombre']}", "success")
    return redirect(url_for("turnos.inicio"))


@turnos_bp.get("/api/cola")
def ver_cola():
    return jsonify(_sistema().ver_cola())


@turnos_bp.get("/api/historial")
def ver_historial():
    n = request.args.get("n", default=10, type=int)
    return jsonify(_sistema().historial(n))


@turnos_bp.post("/guardar")
def guardar_estado():
    ruta = _archivo_estado()
    _sistema().guardar_estado(ruta)
    flash(f"Estado guardado en {ruta}", "success")
    return redirect(url_for("turnos.inicio"))


@turnos_bp.post("/cargar")
def cargar_estado():
    ruta = _archivo_estado()
    try:
        sistema = _sistema().cargar_estado(ruta)
        current_app.extensions["sistema_turnos"] = sistema
        flash("Estado restaurado correctamente.", "success")
    except FileNotFoundError:
        flash("No existe un estado guardado todavia.", "warning")
    return redirect(url_for("turnos.inicio"))
