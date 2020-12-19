DROP TABLE IF EXISTS pitcher;

CREATE TABLE pitcher
    SELECT DISTINCT pitcher AS id, player_name AS name,
            CASE
				WHEN inning_topbot = 'Top' THEN home_team
               ELSE away_team
            END AS team
            FROM pitches;