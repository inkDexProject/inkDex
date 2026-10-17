import argparse
import logging
from pathlib import Path
from waitress import serve

from app import app


BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "inkdex.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

parser = argparse.ArgumentParser(description="Servidor Inkdex")
parser.add_argument(
    "--host",
    choices=["127.0.0.1", "0.0.0.0"],
    default="0.0.0.0",
    help="127.0.0.1 para uso individual; 0.0.0.0 para la red local",
)
parser.add_argument("--port", type=int, default=5000)
args = parser.parse_args()

logging.info("Inkdex inicia en %s:%s", args.host, args.port)

try:
    serve(app, host=args.host, port=args.port)
except Exception:
    logging.exception("Error al ejecutar Inkdex")
    raise
