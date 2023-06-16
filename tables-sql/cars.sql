CREATE TABLE public.cars
(
    id serial NOT NULL,
    company integer NOT NULL,
    model character varying(64) NOT NULL,
    type character varying(12) NOT NULL,
    is_available boolean DEFAULT true,
    "created_at" timestamp with time zone DEFAULT now(),
    PRIMARY KEY (id),
    CONSTRAINT car_company_fk FOREIGN KEY (company)
        REFERENCES public.company (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
);

ALTER TABLE IF EXISTS public.cars
    OWNER to postgres;