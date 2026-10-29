-- Cotizaciones diarias del dólar oficial y blue en formato largo.
CREATE OR REPLACE TABLE stg_dolar AS
SELECT DISTINCT ON (casa, fecha)
    casa,
    CAST(fecha AS DATE) AS fecha,
    CAST(compra AS DOUBLE) AS compra,
    CAST(venta AS DOUBLE) AS venta
FROM (
    SELECT * FROM raw_dolar_oficial
    UNION ALL
    SELECT * FROM raw_dolar_blue
)
WHERE venta IS NOT NULL
ORDER BY casa, fecha;
