CREATE TABLE website_status (
    status_code integer,
    timestamp timestamp,
    matches_regex bool,
    response_time_seconds float
);


ALTER TABLE website_status OWNER TO postgres;