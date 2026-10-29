-- Riesgo país (EMBI) diario, en puntos básicos.
CREATE OR REPLACE TABLE stg_riesgo_pais AS
SELECT DISTINCT ON (fecha)
    CAST(fecha AS DATE) AS fecha,
    CAST(valor AS INTEGER) AS puntos
FROM raw_riesgo_pais
WHERE valor IS NOT NULL
ORDER BY fecha;
