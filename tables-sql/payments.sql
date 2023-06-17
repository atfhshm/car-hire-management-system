CREATE TABLE IF NOT EXISTS payments
(
    id serial NOT NULL,
    booking integer NOT NULL,
    amout integer NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT payment_booking_fk FOREIGN KEY (booking)
        REFERENCES bookings (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);
