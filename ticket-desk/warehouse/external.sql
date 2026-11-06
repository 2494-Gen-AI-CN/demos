-- the agents' teams, read from Google Sheets where they live
CREATE OR REPLACE EXTERNAL TABLE desk_raw.agent_teams (
    name string,
    team string
)
OPTIONS (
    format = 'GOOGLE_SHEETS',
    uris = ['https://docs.google.com/spreadsheets/d/1TaeNHvSyc5_Z_XzBcsj8oeMFo-9cHPvneIvifIdrUTY'],
    skip_leading_rows=1
);

-- the sheet imported as a native table
CREATE OR REPLACE TABLE desk_raw.agent_teams_copy as
SELECT *
FROM desk_raw.agent_teams;

-- events per team
SELECT s.team, SUM(f.event_count) as events
FROM desk_dw.fact_ticket_events as f
JOIN desk_dw.dim_agent as a on a.agent_key=f.agent_key
JOIN desk_raw.agent_teams_copy as s on s.name=a.name
GROUP BY s.team
ORDER BY s.team;