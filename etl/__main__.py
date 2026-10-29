"""Corre el ETL completo: python -m etl [--sin-descarga]"""

import argparse
import json
import shutil
from pathlib import Path

from etl import fuentes, pipeline, reporte

RAIZ = Path(__file__).resolve().parent.parent


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--raw",
        type=Path,
        default=RAIZ / "data" / "raw",
        help="Carpeta con los JSON crudos",
    )
    p.add_argument(
        "--sin-descarga",
        action="store_true",
        help="Usar los crudos que ya están en --raw",
    )
    p.add_argument("--destino", type=Path, default=RAIZ / "site")
    args = p.parse_args()

    if not args.sin_descarga:
        fuentes.descargar(args.raw)
    base = args.destino / "datos" / "warehouse.duckdb"
    resultados, hechos = pipeline.ejecutar(args.raw, base)

    datos = args.destino / "datos"
    hechos.to_csv(datos / "fct_mensual.csv", index=False)
    hechos.to_parquet(datos / "fct_mensual.parquet", index=False)
    (datos / "analisis.json").write_text(
        json.dumps(resultados, ensure_ascii=False, default=str), encoding="utf-8"
    )
    reporte.generar(resultados, args.destino, RAIZ / "web" / "plantilla.html")
    shutil.copy(RAIZ / "web" / "estilos.css", args.destino / "estilos.css")
    print(f"listo    sitio en {args.destino}")


if __name__ == "__main__":
    main()
