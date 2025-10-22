.headers on
.mode column

DROP TABLE IF EXISTS signals;
CREATE TABLE signals (
  id CHAR(3) PRIMARY KEY,
  frequency FLOAT,
  magnitude FLOAT,
  phase FLOAT
);

DROP TABLE IF EXISTS samples;
CREATE TABLE samples (
  id INTEGER,
  x INTEGER,
  y INTEGER,
  signal_id CHAR(3),
  FOREIGN KEY (signal_id) REFERENCES signals,
  PRIMARY KEY(id,signal_id)
);

/*
SELECT * FROM signals;
SELECT * FROM samples;

.print "1) echantillons du signal 'X'"
SELECT * 
FROM signals,samples
WHERE signals.id=samples.signal_id
  AND signals.id='X';
*/