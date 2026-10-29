"""Load + transform en DuckDB: carga los JSON crudos y corre los modelos SQL en orden."""

from pathlib import Path

import duckdb

RAIZ = Path(__file__).resolve().parent.parent
SQL = RAIZ / "sql"


def cargar_crudos(con, carpeta: Path):
    for archivo in sorted(carpeta.glob("*.json")):
        con.execute(
            f"CREATE OR REPLACE TABLE raw_{archivo.stem} AS SELECT * FROM read_json_auto(?)",
            [str(archivo)],
        )
        n = con.execute(f"SELECT count(*) FROM raw_{archivo.stem}").fetchone()[0]
        print(f"load     raw_{archivo.stem}: {n} filas")


def correr_modelos(con):
    for capa in ("staging", "marts"):
        for archivo in sorted((SQL / capa).glob("*.sql")):
            con.execute(archivo.read_text())
            print(f"model    {capa}/{archivo.name}")


def correr_tests(con, omitir=()):
    """Cada test es una consulta que debe devolver cero filas, al estilo dbt."""
    fallas = []
    for archivo in sorted((SQL / "tests").glob("*.sql")):
        if archivo.stem in omitir:
            continue
        filas = con.execute(archivo.read_text()).fetchall()
        estado = "OK" if not filas else f"FALLA ({len(filas)} filas)"
        print(f"test     {archivo.stem}: {estado}")
        if filas:
            fallas.append(archivo.stem)
    return fallas


def correr_analisis(con):
    resultados = []
    for archivo in sorted((SQL / "analisis").glob("*.sql")):
        consulta = archivo.read_text()
        rel = con.sql(consulta)
        resultados.append(
            {
                "nombre": archivo.stem,
                "titulo": consulta.splitlines()[0].removeprefix("--").strip(),
                "sql": consulta.strip(),
                "columnas": rel.columns,
                "filas": [list(f) for f in rel.fetchall()],
            }
        )
    return resultados


def ejecutar(carpeta_raw: Path, base: Path, omitir_tests=()):
    base.parent.mkdir(parents=True, exist_ok=True)
    if base.exists():
        base.unlink()
    con = duckdb.connect(str(base))
    try:
        cargar_crudos(con, carpeta_raw)
        correr_modelos(con)
        fallas = correr_tests(con, omitir_tests)
        if fallas:
            raise RuntimeError(f"Fallaron los tests de datos: {', '.join(fallas)}")
        return correr_analisis(con), con.execute(
            "SELECT * FROM fct_mensual ORDER BY mes"
        ).df()
    finally:
        con.close()
