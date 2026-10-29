-- Correlación entre variables mensuales desde 2018.
SELECT
    round(corr(inflacion_pct, devaluacion_oficial_pct), 2) AS inflacion_vs_devaluacion,
    round(corr(inflacion_pct, brecha_pct), 2) AS inflacion_vs_brecha,
    round(corr(brecha_pct, riesgo_pais_prom), 2) AS brecha_vs_riesgo_pais
FROM fct_mensual
WHERE mes >= DATE '2018-01-01';
