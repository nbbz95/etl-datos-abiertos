"""Extract: descarga las fuentes crudas a data/raw/ tal como vienen."""

import json
import urllib.request
from pathlib import Path

BASE = "https://api.argentinadatos.com/v1"
FUENTES = {
    "inflacion": f"{BASE}/finanzas/indices/inflacion",
    "dolar_oficial": f"{BASE}/cotizaciones/dolares/oficial",
    "dolar_blue": f"{BASE}/cotizaciones/dolares/blue",
    "riesgo_pais": f"{BASE}/finanzas/indices/riesgo-pais",
}


def descargar(destino: Path):
    destino.mkdir(parents=True, exist_ok=True)
    for nombre, url in FUENTES.items():
        req = urllib.request.Request(url, headers={"User-Agent": "etl-datos-abiertos"})
        with urllib.request.urlopen(req, timeout=60) as r:
            datos = json.load(r)
        if not datos:
            raise RuntimeError(f"La fuente {nombre} vino vacía")
        (destino / f"{nombre}.json").write_text(json.dumps(datos), encoding="utf-8")
        print(f"extract  {nombre}: {len(datos)} registros")
