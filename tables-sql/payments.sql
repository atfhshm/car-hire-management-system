CREATE TABLE public.payments
(
    id serial NOT NULL,
    booking integer NOT NULL,
    amout integer NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT payment_booking_fk FOREIGN KEY (booking)
        REFERENCES public.bookings (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS public.payments
    OWNER to postgres;