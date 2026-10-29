-- Últimos 12 meses con datos completos.
SELECT strftime(mes, '%Y-%m') AS mes, inflacion_pct, oficial_prom, blue_prom, brecha_pct, riesgo_pais_prom
FROM fct_mensual
WHERE oficial_prom IS NOT NULL
ORDER BY mes DESC
LIMIT 12;
