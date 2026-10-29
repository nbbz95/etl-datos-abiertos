-- ¿El dólar oficial corrió por encima o por debajo de la inflación? Últimos 12 meses.
WITH ult AS (
    SELECT * FROM fct_mensual WHERE devaluacion_oficial_pct IS NOT NULL ORDER BY mes DESC LIMIT 12
)
SELECT
    round((exp(sum(ln(1 + inflacion_pct / 100))) - 1) * 100, 1) AS inflacion_12m_pct,
    round((exp(sum(ln(1 + devaluacion_oficial_pct / 100))) - 1) * 100, 1) AS devaluacion_12m_pct,
    CASE
        WHEN sum(ln(1 + devaluacion_oficial_pct / 100)) < sum(ln(1 + inflacion_pct / 100))
        THEN 'El dólar subió menos que los precios (apreciación real del peso)'
        ELSE 'El dólar subió más que los precios (depreciación real del peso)'
    END AS lectura
FROM ult;
