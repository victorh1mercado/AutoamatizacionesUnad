import os
from dotenv import load_dotenv

load_dotenv()

URL_CAMPUS = os.getenv("URL_CAMPUS")

USUARIO_UNAD = os.getenv("USUARIO_UNAD")
CLAVE_UNAD = os.getenv("CLAVE_UNAD")
CURSO = "AulaA"