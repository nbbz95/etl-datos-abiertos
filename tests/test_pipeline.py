from pathlib import Path

import duckdb

from etl import pipeline

FIXTURES = Path(__file__).parent / "fixtures"


def test_pipeline_completo_con_fixtures(tmp_path):
    base = tmp_path / "w.duckdb"
    # datos_recientes depende de la fecha actual; con fixtures fijos se omite.
    resultados, hechos = pipeline.ejecutar(
        FIXTURES, base, omitir_tests={"datos_recientes"}
    )
    assert {r["nombre"] for r in resultados} == {
        "01_ultimos_12_meses",
        "02_resumen_anual",
        "03_inflacion_vs_dolar",
        "04_correlacion",
    }
    assert hechos["mes"].is_unique
    assert hechos["brecha_pct"].notna().any()


def test_resumen_anual_compone_inflacion(tmp_path):
    base = tmp_path / "w.duckdb"
    resultados, _ = pipeline.ejecutar(FIXTURES, base, omitir_tests={"datos_recientes"})
    anual = next(r for r in resultados if r["nombre"] == "02_resumen_anual")
    fila_2024 = dict(
        zip(anual["columnas"], next(f for f in anual["filas"] if f[0] == 2024))
    )
    assert fila_2024["meses"] == 12
    assert 117 < fila_2024["inflacion_anual_pct"] < 119  # INDEC: 117,8% en 2024


def test_tests_de_datos_detectan_duplicados():
    con = duckdb.connect()
    con.execute(
        "CREATE TABLE fct_mensual AS SELECT DATE '2024-01-01' AS mes FROM range(2)"
    )
    sql = (pipeline.SQL / "tests" / "meses_unicos.sql").read_text()
    assert con.execute(sql).fetchall()
