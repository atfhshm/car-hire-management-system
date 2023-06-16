CREATE TABLE public.bookings
(
    id serial NOT NULL,
    car integer NOT NULL,
    "user" integer NOT NULL,
    hire_date timestamp with time zone NOT NULL DEFAULT NOW(),
    return_date time with time zone NOT NULL,
    created_at time with time zone DEFAULT Now(),
    PRIMARY KEY (id),
    CONSTRAINT booking_car_fk FOREIGN KEY (car)
        REFERENCES public.cars (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT booking_user_fk FOREIGN KEY ("user")
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
);

ALTER TABLE IF EXISTS public.bookings
    OWNER to postgres;