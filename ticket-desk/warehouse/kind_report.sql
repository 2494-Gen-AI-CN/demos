-- events of one kind; run with --parameter=kind::<kind>
SELECT ticket_key, event_date, hours_since_open
FROM desk_dw.fact_ticket_events
WHERE kind = @kind
ORDER BY ticket_key;
