CREATE TABLE IF NOT EXISTS cars
(
    id serial NOT NULL,
    company integer NOT NULL,
    model character varying(64) NOT NULL,
    type character varying(12) NOT NULL,
    is_available boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT now(),
    PRIMARY KEY (id),
    CONSTRAINT car_company_fk FOREIGN KEY (company)
        REFERENCES companies (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
);