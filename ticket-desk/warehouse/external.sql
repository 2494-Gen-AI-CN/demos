-- the agents' teams, read from the Google Sheet where they live
CREATE OR REPLACE EXTERNAL TABLE desk_raw.agent_teams (
  name STRING,
  team STRING
)
OPTIONS (
  format = 'GOOGLE_SHEETS',
  uris = ['https://docs.google.com/spreadsheets/d/18xC_I26atMz2bCnpuhpucV8BYHpxWxCr_RtJAx5M_3A'],
  skip_leading_rows = 1
);

-- events per team
SELECT s.team, SUM(f.event_count) AS events
FROM desk_dw.fact_ticket_events AS f
JOIN desk_dw.dim_agent AS a ON a.agent_key = f.agent_key
JOIN desk_raw.agent_teams AS s ON s.name = a.name
GROUP BY s.team
ORDER BY s.team;

-- the Sheet imported as a native table
CREATE OR REPLACE TABLE desk_raw.agent_teams_copy AS
SELECT *
FROM desk_raw.agent_teams;
