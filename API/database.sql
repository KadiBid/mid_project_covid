
CREATE TABLE zones(
    id SERIAL,
    country varchar(64),
    province varchar(64),
    lat float,
    long float,
    PRIMARY KEY (id)
)