-- Inflación mensual del INDEC, una fila por mes.
CREATE OR REPLACE TABLE stg_inflacion AS
SELECT DISTINCT ON (mes)
    date_trunc('month', CAST(fecha AS DATE)) AS mes,
    CAST(valor AS DOUBLE) AS inflacion_pct
FROM raw_inflacion
WHERE valor IS NOT NULL
ORDER BY mes, fecha DESC;
