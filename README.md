# ETL de datos abiertos de Argentina

Pipeline ETL que cruza **inflación, dólar oficial, dólar blue y riesgo país** en un warehouse **DuckDB**, con modelos y tests de datos escritos en SQL (estilo dbt) y orquestado con GitHub Actions todos los días.

**Reporte:** https://nbbz95.github.io/etl-datos-abiertos/

## Flujo

```
extract   etl/fuentes.py      4 endpoints de ArgentinaDatos → data/raw/*.json
load      etl/pipeline.py     JSON → tablas raw_* en DuckDB
transform sql/staging/        tipado, deduplicación y limpieza → stg_*
          sql/marts/          tabla de hechos mensual → fct_mensual
test      sql/tests/          consultas que deben devolver 0 filas
analyze   sql/analisis/       consultas finales → reporte HTML
publish   GitHub Pages        reporte + CSV, Parquet y el .duckdb para descargar
```

Si falla un test de datos (meses duplicados, huecos en la serie, valores fuera de rango o datos atrasados), el pipeline corta y no publica.

## Modelo de datos

`fct_mensual`, una fila por mes:

| Columna | Descripción |
|---|---|
| `mes` | Primer día del mes |
| `inflacion_pct` | Inflación mensual (INDEC) |
| `oficial_prom`, `blue_prom` | Promedio mensual del precio de venta |
| `brecha_pct` | Brecha promedio blue vs oficial |
| `devaluacion_oficial_pct` | Variación del cierre del oficial contra el mes anterior |
| `riesgo_pais_prom` | Promedio mensual del EMBI, en puntos básicos |

## Análisis incluidos

1. Últimos 12 meses.
2. Inflación y devaluación anual compuestas (con `exp(sum(ln(1 + x)))`), brecha y riesgo país promedio.
3. Si el dólar corrió por encima o por debajo de la inflación en los últimos 12 meses.
4. Correlaciones entre inflación, devaluación, brecha y riesgo país.

## Correr localmente

```bash
pip install -r requirements.txt pytest
python -m pytest -q          # tests del pipeline con fixtures reales
python -m etl                # ETL completo → site/
python -m http.server -d site 8000
```

Para explorar el warehouse: `duckdb site/datos/warehouse.duckdb` y por ejemplo `SELECT * FROM fct_mensual ORDER BY mes DESC LIMIT 12;`.

## Stack

Python, DuckDB, SQL, pandas, pytest, GitHub Actions y GitHub Pages.

Fuente: [ArgentinaDatos](https://argentinadatos.com) (INDEC, BCRA, JP Morgan).
