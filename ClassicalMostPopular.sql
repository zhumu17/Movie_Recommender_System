SELECT I.itemId, I.itemName, R.avgRating, R.numRating
FROM Inventory AS I JOIN (
SELECT itemId, AVG(rating) AS avgRating, COUNT(rating) AS numRating
FROM ratings
GROUP BY itemId
HAVING numRating>100
ORDER BY avgRating DESC
LIMIT 100 ) AS R 
ON I.itemId = R.itemId
ORDER BY R.avgRating DESC
;