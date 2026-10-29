-- No faltan meses intermedios en la serie de inflación.
WITH m AS (SELECT mes, lag(mes) OVER (ORDER BY mes) AS anterior FROM stg_inflacion)
SELECT * FROM m WHERE anterior IS NOT NULL AND mes <> anterior + INTERVAL 1 MONTH;
