SELECT 
    DATE(transit_timestamp) AS date, 
    fare_class_category, 
    SUM(ridership) AS total_ridership
FROM `nyc-subway-data-453606.nyc_ridership.subway_ridership`
WHERE transit_mode = 'subway'
GROUP BY date, fare_class_category
ORDER BY date, total_ridership DESC;