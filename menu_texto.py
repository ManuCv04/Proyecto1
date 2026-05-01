"""Interfaz de texto para el Sistema de Gestion de Turnos."""

from __future__ import annotations

from pathlib import Path

from app.models.sistema_gestion_turnos import SistemaGestionTurnos


ARCHIVO_ESTADO = Path("data/estado_turnos.json")


def mostrar_menu(nombre_servicio: str) -> None:
    print(f"\n=== Sistema de Turnos - {nombre_servicio} ===")
    print("1. Tomar turno normal")
    print("2. Tomar turno prioritario")
    print("3. Atender siguiente")
    print("4. Ver cola actual")
    print("5. Ver historial")
    print("6. Guardar estado")
    print("7. Salir")


def crear_o_cargar(nombre_servicio: str) -> SistemaGestionTurnos:
    if ARCHIVO_ESTADO.exists():
        try:
            sistema = SistemaGestionTurnos.cargar_estado(str(ARCHIVO_ESTADO))
            print("Estado cargado desde archivo JSON.")
            return sistema
        except (OSError, ValueError, KeyError):
            print("No se pudo cargar el estado previo, se creara uno nuevo.")
    return SistemaGestionTurnos(nombre_servicio)


def main() -> None:
    sistema = crear_o_cargar("Banco XYZ")

    while True:
        mostrar_menu(sistema.nombre_servicio)
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            nombre = input("Nombre del cliente: ").strip()
            try:
                turno = sistema.tomar_turno(nombre, prioritario=False)
                print(f"Turno asignado: {turno}")
            except ValueError as exc:
                print(f"Error: {exc}")
        elif opcion == "2":
            nombre = input("Nombre del cliente prioritario: ").strip()
            try:
                turno = sistema.tomar_turno(nombre, prioritario=True)
                print(f"Turno prioritario asignado: {turno}")
            except ValueError as exc:
                print(f"Error: {exc}")
        elif opcion == "3":
            atendido = sistema.atender_siguiente()
            if atendido:
                print(f"Atendido: {atendido['turno']} - {atendido['nombre']}")
            else:
                print("No hay turnos pendientes.")
        elif opcion == "4":
            cola = sistema.ver_cola()
            if not cola:
                print("No hay turnos pendientes.")
            for item in cola:
                tipo = "Prioritario" if item["prioritario"] else "Normal"
                print(f"{item['turno']} - {item['nombre']} ({tipo})")
        elif opcion == "5":
            ultimos = sistema.historial(10)
            if not ultimos:
                print("No hay historial de atendidos.")
            for item in ultimos:
                print(f"{item['turno']} - {item['nombre']} (Atendido: {item['hora_atencion']})")
        elif opcion == "6":
            sistema.guardar_estado(str(ARCHIVO_ESTADO))
            print(f"Estado guardado en {ARCHIVO_ESTADO}.")
        elif opcion == "7":
            sistema.guardar_estado(str(ARCHIVO_ESTADO))
            print("Saliendo. Estado guardado.")
            break
        else:
            print("Opcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    main()
