
CREATE TABLE zones(
    id SERIAL,
    country varchar(64),
    province varchar(64),
    lat float,
    long float,
    PRIMARY KEY (id)
)


CREATE TABLE cases(
    id SERIAL,
    date datetime,
    confirmed int,
    deaths int,
    recovered int,
    PRIMARY KEY (country)
)
