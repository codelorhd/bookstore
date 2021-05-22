
CREATE TABLE authors
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name text COLLATE "default",
    books text[] COLLATE "default",
    CONSTRAINT author_pkey PRIMARY KEY (id)
)



CREATE TABLE books
(
    isbn text COLLATE "default" NOT NULL,
    name text COLLATE "default",
    author text COLLATE "default",
    year integer,
    CONSTRAINT books_pkey PRIMARY KEY (isbn)
)


CREATE TABLE personel
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    username text COLLATE "default",
    password text COLLATE "default",
    mail text COLLATE "default",
    role text COLLATE "default",
    CONSTRAINT personel_pkey PRIMARY KEY (id)
)


CREATE TABLE users
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    username text COLLATE "default" NOT NULL,
    password text COLLATE "default" NOT NULL,
    mail text COLLATE "default",
    role text COLLATE "default",
    CONSTRAINT users_pkey PRIMARY KEY (id)
)