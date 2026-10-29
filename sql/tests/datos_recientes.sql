-- La serie de inflación no puede tener más de 4 meses de atraso.
SELECT max(mes) AS ultimo FROM stg_inflacion HAVING max(mes) < current_date - INTERVAL 4 MONTH;
