# Proyecto 1 - Sistema de Gestion de Turnos (MVC Flask)

Implementacion completa del sistema de turnos solicitado:

- Cola normal FIFO.
- Cola prioritaria (se atiende antes que la normal).
- Historial de atendidos con estructura tipo pila.
- Persistencia JSON para guardar y cargar estado.
- Interfaz web Flask (MVC) y menu de texto en consola.

## Estructura MVC

- `app/models/sistema_gestion_turnos.py`: logica de negocio y estructuras de datos.
- `app/controllers/turnos_controller.py`: rutas y acciones HTTP.
- `app/templates/index.html`: vista principal con acciones de menu.
- `app/__init__.py`: fabrica de aplicacion Flask.

## Requisitos

- Python 3.11+ (recomendado)
- Flask 3.1.1

Instalacion:

```bash
py -m pip install -r requirements.txt
```

## Ejecucion Flask

```bash
py run.py
```

Abrir en navegador: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Interfaz de texto (consola)

```bash
py menu_texto.py
```

Menu esperado:

```text
=== Sistema de Turnos - Banco XYZ ===
1. Tomar turno normal
2. Tomar turno prioritario
3. Atender siguiente
4. Ver cola actual
5. Ver historial
6. Guardar estado
7. Salir
```

## Persistencia

El estado se guarda en:

- `data/estado_turnos.json`

Se utiliza automaticamente desde la interfaz de consola al iniciar y salir.
En Flask se puede guardar/cargar con los botones correspondientes.

## Pruebas

```bash
py -m unittest discover -s tests
```
