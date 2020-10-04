CREATE TABLE availability_data (
    id SERIAL PRIMARY KEY,
    host VARCHAR NOT NULL,
    status_code SMALLINT NOT NULL,
    elapsed_time REAL NOT NULL,
    regex_matched BOOLEAN,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);