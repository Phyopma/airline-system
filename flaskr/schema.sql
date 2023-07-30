DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS airline;
DROP TABLE IF EXISTS flight;
DROP TABLE IF EXISTS seat;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS city;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  role TEXT NOT NULL
);

CREATE TABLE airline (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (admin_id) REFERENCES user (id)
);

CREATE TABLE city (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE flight (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    airline_id INTEGER NOT NULL,
    origin_city_id INTEGER NOT NULL,
    destination_city_id INTEGER NOT NULL,
    total_seats INTEGER NOT NULL,
    available_seats INTEGER NOT NULL,
    departure_time TEXT NOT NULL,
    duration TEXT NOT NULL,
    FOREIGN KEY (airline_id) REFERENCES airline (id),
    FOREIGN KEY (origin_city_id) REFERENCES city (id),
    FOREIGN KEY (destination_city_id) REFERENCES city (id)
);

CREATE TABLE seat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER NOT NULL,
    number INTEGER NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (flight_id) REFERENCES flight (id)
);

CREATE TABLE booking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_id INTEGER NOT NULL,
    flight_id INTEGER NOT NULL,
    seat_id INTEGER NOT NULL,
    booked_at TEXT NOT NULL,
    FOREIGN KEY (passenger_id) REFERENCES user (id),
    FOREIGN KEY (flight_id) REFERENCES flight (id),
    FOREIGN KEY (seat_id) REFERENCES seat (id)
);

