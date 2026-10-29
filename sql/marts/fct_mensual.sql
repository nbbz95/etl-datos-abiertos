-- Tabla de hechos mensual: une las tres fuentes por mes, desde que hay cotizaciones del dólar.
CREATE OR REPLACE TABLE fct_mensual AS
WITH dolar AS (
    SELECT
        date_trunc('month', fecha) AS mes,
        avg(venta) FILTER (WHERE casa = 'oficial') AS oficial_prom,
        avg(venta) FILTER (WHERE casa = 'blue') AS blue_prom,
        arg_max(venta, fecha) FILTER (WHERE casa = 'oficial') AS oficial_cierre,
        arg_max(venta, fecha) FILTER (WHERE casa = 'blue') AS blue_cierre
    FROM stg_dolar
    GROUP BY 1
),
riesgo AS (
    SELECT date_trunc('month', fecha) AS mes, avg(puntos) AS riesgo_pais_prom
    FROM stg_riesgo_pais
    GROUP BY 1
)
SELECT
    i.mes,
    i.inflacion_pct,
    round(d.oficial_prom, 2) AS oficial_prom,
    round(d.blue_prom, 2) AS blue_prom,
    round((d.blue_prom / d.oficial_prom - 1) * 100, 2) AS brecha_pct,
    round((d.oficial_cierre / lag(d.oficial_cierre) OVER (ORDER BY i.mes) - 1) * 100, 2) AS devaluacion_oficial_pct,
    round(r.riesgo_pais_prom) AS riesgo_pais_prom
FROM stg_inflacion i
JOIN dolar d USING (mes)
LEFT JOIN riesgo r USING (mes)
ORDER BY i.mes;
