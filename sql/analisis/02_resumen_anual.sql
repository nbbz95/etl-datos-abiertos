-- Inflación compuesta, devaluación del oficial y brecha promedio por año.
SELECT
    year(mes) AS anio,
    count(*) AS meses,
    round((exp(sum(ln(1 + inflacion_pct / 100))) - 1) * 100, 1) AS inflacion_anual_pct,
    round((exp(sum(ln(1 + coalesce(devaluacion_oficial_pct, 0) / 100))) - 1) * 100, 1) AS devaluacion_anual_pct,
    round(avg(brecha_pct), 1) AS brecha_prom_pct,
    round(avg(riesgo_pais_prom)) AS riesgo_pais_prom
FROM fct_mensual
WHERE oficial_prom IS NOT NULL
GROUP BY 1
ORDER BY 1 DESC;
