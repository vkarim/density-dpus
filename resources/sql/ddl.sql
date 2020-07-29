-- assumes PostGres SQL/TimeScaleDB
-- Note: Just a rough draft, can use more optimal data types based on domain knowledge

CREATE TABLE location (
  location_id INT GENERATED ALWAYS AS IDENTITY,
  name text not null,
  street_address text not null,
  city text not null,
  state text not null,
  zipcode text not null,
  PRIMARY KEY(location_id)
);

CREATE TABLE space (
  space_id INT GENERATED ALWAYS AS IDENTITY,
  location_id INT not null,
  name text not null,
  description text,
  PRIMARY KEY(space_id),
  CONSTRAINT fk_location FOREIGN KEY(location_id) REFERENCES location(location_id)
);

--associate with 1 or 2 spaces via the 'doorway_spaces' table
CREATE TABLE doorway (
  doorway_id INT GENERATED ALWAYS AS IDENTITY,
  name text not null,
  description text,
  PRIMARY KEY(doorway_id)
);


CREATE TABLE doorway_spaces (
  doorway_id int,
  space_id int,
  is_positive_space boolean NOT NULL,
  PRIMARY KEY(doorway_id, space_id),
  CONSTRAINT fk_space FOREIGN KEY space_id REFERENCES space(space_id),
  CONSTRAINT fk_doorway FOREIGN KEY doorway_id REFERENCES doorway(doorway_id)
);

CREATE TABLE dpu (
  dpu_id INT GENERATED ALWAYS AS IDENTITY,
  name text,
  doorway_id int not null,
  PRIMARY KEY(dpu_id),
  CONSTRAINT fk_doorway FOREIGN KEY doorway_id REFERENCES doorway(doorway_id)
);

CREATE TABLE spacePersonCount (
 time TIMESTAMPTZ not null,
 space_id int not null,
 count int not null,
 CONSTRAINT fk_space FOREIGN KEY space_id REFERENCES space(space_id)
);

-- create a TimeScaleDB hypertable based on the above 'spacePersonCount':
-- https://docs.timescale.com/latest/api#create_hypertable