SELECT 
    YEAR(ridership_date) AS year, 
    SUM(ridership_count) AS total_ridership
FROM `nyc-subway-data-453606.nyc_ridership.subway_ridership`
WHERE MONTH(ridership_date) = 1
GROUP BY YEAR(ridership_date)
ORDER BY year;