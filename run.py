"""Punto de entrada para ejecutar la app Flask."""

from app import create_app

app = create_app("Banco XYZ")

if __name__ == "__main__":
    app.run(debug=True)
