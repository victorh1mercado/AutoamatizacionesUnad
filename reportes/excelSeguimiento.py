from openpyxl import Workbook
from pathlib import Path

RUTA_REPORTE = Path("Reportes")
ARCHIVO = RUTA_REPORTE / "Seguimiento_Foros.xlsx"

wb = None
ws = None


def crear_reporte_seguimiento():

    global wb, ws

    RUTA_REPORTE.mkdir(exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "Seguimiento"

    ws.append([
        "Grupo",
        "Autor",
        "Fecha",
        "Asunto",
        "Responde a",
        "Requiere respuesta",
        "Horas transcurridas",
        "Prioridad",
        "Vencido",
        "Respondido",
        "Respondió",
        "Fecha respuesta",
        "Tiempo respuesta (h)"
    ])

    wb.save(ARCHIVO)


def registrar_publicaciones(grupo, publicaciones):

    global wb, ws

    if wb is None:
        crear_reporte_seguimiento()

    if isinstance(publicaciones, dict):
        publicaciones = publicaciones.get("publicaciones", [])

    for pub in publicaciones:

        ws.append([

            grupo,

            pub.get("autor", ""),

            str(pub.get("fecha", "")),

            pub.get("asunto", ""),

            pub.get("respuesta_a", ""),

            "SI" if pub.get("requiere_respuesta") else "NO",

            pub.get("horas_transcurridas", ""),

            pub.get("prioridad", ""),

            "SI" if pub.get("vencido") else "NO",

            "SI" if pub.get("respondido") else "NO",

            pub.get("respondio", ""),

            str(pub.get("fecha_respuesta", "")),

            pub.get("tiempo_respuesta", "")

        ])

    wb.save(ARCHIVO)