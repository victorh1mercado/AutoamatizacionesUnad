import os
from dotenv import load_dotenv

load_dotenv()

URL_CAMPUS = os.getenv("URL_CAMPUS")

USUARIO_UNAD = os.getenv("USUARIO_UNAD")
CLAVE_UNAD = os.getenv("CLAVE_UNAD")
CURSO = "AulaA"


# ==========================================
# asunto que se pondra en el Foro
# ==========================================

ASUNTO_FORO = "📢 ¡ATENCIÓN GRUPO! Checklist Fase 2 + Cita de Aclaración de Dudas (Jueves 8:00 p.m.)"

# ==========================================
# MODOS DE EJECUCIÓN
# ==========================================

MODO_SIMULACION = 0
MODO_PRODUCCION = 1

# Cambiar únicamente esta variable
MODO = MODO_SIMULACION