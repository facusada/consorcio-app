"""
Servicio de generacion de PDF para liquidaciones.
Usa Jinja2 para renderizar el template HTML y WeasyPrint para convertir a PDF.
"""
from decimal import Decimal
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

DIRECTORIO_TEMPLATES = Path(__file__).parent.parent / "templates"

_env = Environment(loader=FileSystemLoader(str(DIRECTORIO_TEMPLATES)))


def _formato_monto(valor) -> str:
    try:
        n = float(valor)
    except (TypeError, ValueError):
        n = 0.0
    entero = int(n)
    centavos = round((n - entero) * 100)
    return f"$ {entero:,}".replace(",", ".") + f",{centavos:02d}"


_env.filters["formato_monto"] = _formato_monto


def generar_pdf_liquidacion(contexto: dict) -> bytes:
    """
    Recibe el contexto con los datos de la liquidacion y devuelve el PDF como bytes.
    Requiere WeasyPrint instalado con sus dependencias del sistema (cairo, pango).
    """
    try:
        from weasyprint import HTML
    except ImportError as e:
        raise RuntimeError(
            "WeasyPrint no esta instalado o faltan dependencias del sistema. "
            "Revisar Dockerfile para las libs cairo/pango."
        ) from e

    template = _env.get_template("liquidacion_pdf.html")
    html_str = template.render(**contexto)
    return HTML(string=html_str).write_pdf()


def renderizar_html_liquidacion(contexto: dict) -> str:
    """Renderiza solo el HTML, util para tests y preview."""
    template = _env.get_template("liquidacion_pdf.html")
    return template.render(**contexto)
