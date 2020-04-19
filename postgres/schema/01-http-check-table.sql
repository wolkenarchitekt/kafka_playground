CREATE TABLE http_check (
    timestamp timestamp with time zone, -- 8 bytes
    response_time_seconds real,         -- 4 bytes
    status_code smallint,               -- 2 bytes
    matches_regex bool                  -- 1 byte
);
