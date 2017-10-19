
/* 

Creation of the database from *.csv files.

*/


/* Create the table `reading` */
CREATE TABLE reading
(
  is_app_event boolean,
  visitor_id character varying,
  id character varying,
  visit_id character varying,
  tracking_time timestamp without time zone,
  created_at timestamp without time zone,
  story_id character varying,
  user_id character varying
);

/* Import the table `reading` */
COPY reading
FROM 'path/to/file/reading.csv' DELIMITER ',' CSV HEADER;


/* Create the table `stories` */
CREATE TABLE stories
(
  id character varying,
  user_id character varying,
  teaser character varying,
  title character varying,
  cover character varying,
  category_one character varying,
  category_two character varying
);

/* Import the table `stories` */
COPY stories
FROM 'path/to/file/stories.csv' DELIMITER ',' CSV HEADER;


/* Create the table `visits` */
CREATE TABLE visits
(
  visitor_id character varying,
  user_id character varying,
  country character varying,
  timezone character varying,
  location_accuracy int
);

/* Import the table `visits` */
COPY visits
FROM 'path/to/file/visits.csv' DELIMITER ',' CSV HEADER;



