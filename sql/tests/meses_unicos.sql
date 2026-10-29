-- Cada mes aparece una sola vez en la tabla de hechos.
SELECT mes, count(*) FROM fct_mensual GROUP BY mes HAVING count(*) > 1;
