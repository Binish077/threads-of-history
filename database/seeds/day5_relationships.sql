-- Day 5 relationship seed data for the Dance of the Dragons core graph
-- These links connect the first 20 entities into a meaningful political network.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

INSERT INTO relationships (id, source_id, target_id, type, valid_from, valid_to, weight, confidence)
VALUES
  -- Targaryen core lineage and succession
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Viserys I Targaryen'), (SELECT id FROM entities WHERE name = 'Aemma Arryn'), 'marriage', '0100-01-01', '0105-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Aemma Arryn'), (SELECT id FROM entities WHERE name = 'Rhaenyra Targaryen'), 'mother_of', '0105-01-01', '0130-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Viserys I Targaryen'), (SELECT id FROM entities WHERE name = 'Rhaenyra Targaryen'), 'father_of', '0105-01-01', '0130-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Viserys I Targaryen'), (SELECT id FROM entities WHERE name = 'Alicent Hightower'), 'marriage', '0106-01-01', '0117-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Viserys I Targaryen'), (SELECT id FROM entities WHERE name = 'Aegon II Targaryen'), 'father_of', '0112-01-01', '0130-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Alicent Hightower'), (SELECT id FROM entities WHERE name = 'Aegon II Targaryen'), 'mother_of', '0112-01-01', '0130-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Viserys I Targaryen'), (SELECT id FROM entities WHERE name = 'Aemond Targaryen'), 'father_of', '0112-01-01', '0130-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Alicent Hightower'), (SELECT id FROM entities WHERE name = 'Aemond Targaryen'), 'mother_of', '0112-01-01', '0130-12-31', 1.0, 1.0),

  -- Velaryon branch and Laenor
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Corlys Velaryon'), (SELECT id FROM entities WHERE name = 'Rhaenys Targaryen'), 'marriage', '0100-01-01', '0130-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Corlys Velaryon'), (SELECT id FROM entities WHERE name = 'Laenor Velaryon'), 'father_of', '0109-01-01', '0120-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Rhaenys Targaryen'), (SELECT id FROM entities WHERE name = 'Laenor Velaryon'), 'mother_of', '0109-01-01', '0120-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Rhaenyra Targaryen'), (SELECT id FROM entities WHERE name = 'Laenor Velaryon'), 'marriage', '0114-01-01', '0120-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Rhaenyra Targaryen'), (SELECT id FROM entities WHERE name = 'Jacaerys Velaryon'), 'mother_of', '0114-01-01', '0129-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Laenor Velaryon'), (SELECT id FROM entities WHERE name = 'Jacaerys Velaryon'), 'father_of', '0114-01-01', '0129-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Rhaenyra Targaryen'), (SELECT id FROM entities WHERE name = 'Lucerys Velaryon'), 'mother_of', '0116-01-01', '0129-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Laenor Velaryon'), (SELECT id FROM entities WHERE name = 'Lucerys Velaryon'), 'father_of', '0116-01-01', '0129-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Rhaenyra Targaryen'), (SELECT id FROM entities WHERE name = 'Joffrey Velaryon'), 'mother_of', '0118-01-01', '0129-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Laenor Velaryon'), (SELECT id FROM entities WHERE name = 'Joffrey Velaryon'), 'father_of', '0118-01-01', '0129-12-31', 1.0, 1.0),

  -- Marriage and political ties
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Rhaenyra Targaryen'), (SELECT id FROM entities WHERE name = 'Laenor Velaryon'), 'marriage', '0114-01-01', '0120-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Rhaenyra Targaryen'), (SELECT id FROM entities WHERE name = 'Daemon Targaryen'), 'marriage', '0120-01-01', '0130-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Corlys Velaryon'), (SELECT id FROM entities WHERE name = 'Rhaenys Targaryen'), 'marriage', '0100-01-01', '0130-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'House Velaryon'), (SELECT id FROM entities WHERE name = 'House Targaryen'), 'alliance', '0001-01-01', '0131-12-31', 1.0, 1.0),

  -- Black/green faction alignment
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Rhaenyra Targaryen'), (SELECT id FROM entities WHERE name = 'House Stark'), 'political_support', '0120-01-01', '0131-12-31', 0.9, 0.9),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Rhaenyra Targaryen'), (SELECT id FROM entities WHERE name = 'House Arryn'), 'political_support', '0120-01-01', '0131-12-31', 0.9, 0.9),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Aegon II Targaryen'), (SELECT id FROM entities WHERE name = 'House Hightower'), 'political_support', '0120-01-01', '0131-12-31', 0.9, 0.9),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Aegon II Targaryen'), (SELECT id FROM entities WHERE name = 'House Baratheon'), 'political_support', '0120-01-01', '0131-12-31', 0.9, 0.9),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Rhaenyra Targaryen'), (SELECT id FROM entities WHERE name = 'House Velaryon'), 'political_support', '0120-01-01', '0131-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Aegon II Targaryen'), (SELECT id FROM entities WHERE name = 'House Targaryen'), 'claim', '0120-01-01', '0130-12-31', 1.0, 1.0),

  -- Rivalry and conflict
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Rhaenyra Targaryen'), (SELECT id FROM entities WHERE name = 'Aegon II Targaryen'), 'rivalry', '0120-01-01', '0130-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Aegon II Targaryen'), (SELECT id FROM entities WHERE name = 'Rhaenyra Targaryen'), 'rivalry', '0120-01-01', '0130-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Rhaenyra Targaryen'), (SELECT id FROM entities WHERE name = 'Aemond Targaryen'), 'rivalry', '0120-01-01', '0130-12-31', 0.9, 0.9),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Lucerys Velaryon'), (SELECT id FROM entities WHERE name = 'Aemond Targaryen'), 'rivalry', '0127-01-01', '0129-12-31', 0.95, 0.95),

  -- Other key support chains
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Daemon Targaryen'), (SELECT id FROM entities WHERE name = 'Corlys Velaryon'), 'alliance', '0120-01-01', '0131-12-31', 1.0, 1.0),
  (gen_random_uuid(), (SELECT id FROM entities WHERE name = 'Alicent Hightower'), (SELECT id FROM entities WHERE name = 'Otto Hightower'), 'family', '0104-01-01', '0131-12-31', 1.0, 1.0);

-- Attach the same source to every relationship in this seed set.
WITH source_row AS (
  SELECT id
  FROM sources
  WHERE title = 'Dance of the Dragons'
    AND citation = 'https://awoiaf.westeros.org/index.php/Dance_of_the_Dragons'
  LIMIT 1
)
INSERT INTO relationship_sources (relationship_id, source_id)
SELECT r.id, s.id
FROM relationships r
CROSS JOIN source_row s;

-- This file intentionally seeds the most important political and familial edges for the
-- MVP graph. Additional relations can be added once the core graph is validated.
