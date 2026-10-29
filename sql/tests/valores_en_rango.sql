-- Valores imposibles indican un error de carga (el máximo histórico mensual fue 196,6% en 1989).
SELECT * FROM fct_mensual
WHERE inflacion_pct < -10 OR inflacion_pct > 250
   OR oficial_prom <= 0 OR blue_prom <= 0
   OR riesgo_pais_prom < 0;
