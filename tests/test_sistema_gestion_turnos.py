"""Pruebas unitarias del modelo principal."""

from pathlib import Path
import tempfile
import unittest

from app.models.sistema_gestion_turnos import SistemaGestionTurnos


class SistemaGestionTurnosTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sistema = SistemaGestionTurnos("Clinica Central")

    def test_fifo_en_cola_normal(self):
        self.sistema.tomar_turno("Ana")
        self.sistema.tomar_turno("Luis")

        primero = self.sistema.atender_siguiente()
        segundo = self.sistema.atender_siguiente()

        self.assertEqual(primero["nombre"], "Ana")
        self.assertEqual(segundo["nombre"], "Luis")

    def test_prioridad_antes_de_normal(self):
        self.sistema.tomar_turno("Cliente Normal")
        self.sistema.tomar_turno("Cliente VIP", prioritario=True)

        primero = self.sistema.atender_siguiente()
        self.assertTrue(primero["prioritario"])
        self.assertEqual(primero["nombre"], "Cliente VIP")

    def test_historial_como_pila(self):
        self.sistema.tomar_turno("Uno")
        self.sistema.tomar_turno("Dos")
        self.sistema.atender_siguiente()
        self.sistema.atender_siguiente()

        historial = self.sistema.historial(2)
        self.assertEqual(historial[0]["nombre"], "Dos")
        self.assertEqual(historial[1]["nombre"], "Uno")

    def test_persistencia_json(self):
        self.sistema.tomar_turno("Maria")
        self.sistema.tomar_turno("Pedro", prioritario=True)
        self.sistema.atender_siguiente()

        with tempfile.TemporaryDirectory() as tmp:
            archivo = Path(tmp) / "estado.json"
            self.sistema.guardar_estado(str(archivo))

            restaurado = SistemaGestionTurnos.cargar_estado(str(archivo))
            cola = restaurado.ver_cola()
            self.assertEqual(restaurado.nombre_servicio, "Clinica Central")
            self.assertEqual(len(cola), 1)
            self.assertEqual(cola[0]["nombre"], "Maria")
            self.assertEqual(restaurado.historial(1)[0]["nombre"], "Pedro")


if __name__ == "__main__":
    unittest.main()
