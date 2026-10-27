-- Average temperature by city
SELECT
    city,
    ROUND(AVG(temperature), 2) AS avg_temperature
FROM read_parquet('data/processed/weather.parquet')
GROUP BY city
ORDER BY avg_temperature DESC;




-- Query 2: Daily average temperature by city
SELECT
    city,
    CAST(timestamp AS DATE) AS day,
    ROUND(AVG(temperature), 2) AS avg_temperature
FROM read_parquet('data/processed/weather.parquet')
GROUP BY city, CAST(timestamp AS DATE)
ORDER BY day, city;



-- Query 3: Daily precipitation by city
SELECT
    city,
    CAST(timestamp AS DATE) AS day,
    ROUND(SUM(precipitation), 2) AS total_precipitation,
    COUNT(precipitation) AS measured_hours
FROM read_parquet('data/processed/weather.parquet')
GROUP BY city, CAST(timestamp AS DATE)
ORDER BY total_precipitation DESC, day, city;


SELECT
    city,
    CAST(timestamp AS DATE) AS day,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    ROUND(max_temperature - min_temperature, 2) AS temperature_range
FROM read_parquet('data/processed/weather.parquet')
GROUP BY city, CAST(timestamp AS DATE)
ORDER BY temperature_range DESC, day, city;