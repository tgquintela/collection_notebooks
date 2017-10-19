
/*

# Task 1

1. write an SQL query that sums up reading for horror readers by day.
- how much did they read?
- how many readers are there?
- what country are the readers from?

*/


/* reading for horror readers by day */
SELECT readings_horror.days, COUNT(DISTINCT readings_horror.visitor_id)
FROM (SELECT reading.visitor_id, to_char(reading.created_at,'YYYY-MM-DD') as days, reading.story_id, reading.visit_id
      FROM (SELECT id
              FROM stories
              WHERE stories.category_one = 'horror' or stories.category_two = 'horror') AS stories_horror
      INNER JOIN reading ON stories_horror.id = reading.story_id) AS readings_horror
GROUP BY readings_horror.days
ORDER BY readings_horror.days;


/* How much did they read? (Days) */
SELECT readings_horror.visitor_id, COUNT(DISTINCT readings_horror.days)
FROM (SELECT reading.visitor_id, to_char(reading.created_at,'YYYY-MM-DD') as days, reading.story_id, reading.visit_id
      FROM (SELECT id
              FROM stories
              WHERE stories.category_one = 'horror' or stories.category_two = 'horror') AS stories_horror
      INNER JOIN reading ON stories_horror.id = reading.story_id) AS readings_horror
GROUP BY readings_horror.visitor_id;


/* how many readers are there? */
SELECT COUNT(*)
FROM (SELECT DISTINCT reading_books_horror.visitor_id
      FROM (SELECT readings_horror.created_at, readings_horror.story_id, readings_horror.visitor_id, visits.country
            FROM (SELECT reading.visitor_id, reading.created_at, reading.story_id, reading.visit_id
                  FROM (SELECT id
                        FROM stories
                        WHERE stories.category_one = 'horror' or stories.category_two = 'horror') AS stories_horror
                  INNER JOIN reading ON stories_horror.id = reading.story_id) AS readings_horror
            INNER JOIN visits ON readings_horror.visit_id=visits.visitor_id) AS reading_books_horror) AS visitors;


/* what country are the readers from? */
SELECT DISTINCT reading_books_horror.country
FROM (SELECT readings_horror.created_at, readings_horror.story_id, readings_horror.visitor_id, visits.country
      FROM (SELECT reading.visitor_id, reading.created_at, reading.story_id, reading.visit_id
            FROM (SELECT id
                  FROM stories
                  WHERE stories.category_one = 'horror' or stories.category_two = 'horror') AS stories_horror
            INNER JOIN reading ON stories_horror.id = reading.story_id) AS readings_horror
      INNER JOIN visits ON readings_horror.visit_id=visits.visitor_id) AS reading_books_horror;
