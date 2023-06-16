CREATE TABLE public.companies
(
    id serial NOT NULL,
    name character varying(32) NOT NULL,
    created_at timestamp with time zone DEFAULT NOW(),
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.companies
    OWNER to postgres;