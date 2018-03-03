SELECT I.itemId, I.itemName, I.Year, R.avgRating, R.numRating
FROM (
SELECT *
FROM itemFeature
WHERE Year >2008
)  AS I JOIN  (
SELECT itemId, AVG(rating) AS avgRating, COUNT(rating) AS numRating
FROM ratings
GROUP BY itemId
HAVING numRating>15
ORDER BY avgRating DESC
 ) AS R 
ON I.itemId = R.itemId 
ORDER BY R.avgRating DESC
;