SELECT 
    DATE(transit_timestamp) AS date, 
    SUM(ridership) AS total_ridership
FROM `nyc-subway-data-453606.nyc_ridership.subway_ridership`
WHERE transit_mode = 'subway'
AND borough = 'Manhattan'
GROUP BY date
ORDER BY date;
