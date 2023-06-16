CREATE TABLE users
(
    id serial NOT NULL,
    username character varying(32) NOT NULL,
    email character varying(32) NOT NULL,
    first_name character varying(32) NOT NULL,
    last_name character varying(32) NOT NULL,
    type character varying(10) NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT NOW(),
    is_active boolean NOT NULL DEFAULT true,
    password character varying(128) NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS users
    OWNER to postgres;