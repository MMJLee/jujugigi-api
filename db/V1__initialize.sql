CREATE TABLE IF NOT EXISTS public.image (
    image_id serial NOT NULL,
    path varchar NOT NULL,
    file_name varchar NOT NULL,
    description varchar NOT NULL,
    rarity int NOT NULL,
    created_by varchar NOT NULL default 'jujugigi-api',
    created_on timestamptz NOT NULL default current_timestamp,
    updated_by varchar NOT NULL default 'jujugigi-api',
    updated_on timestamptz NOT NULL default current_timestamp,
    CONSTRAINT image_pk PRIMARY KEY (image_id),
    CONSTRAINT image_unique_name UNIQUE (file_name)
);

CREATE TABLE IF NOT EXISTS public.user_alias (
    user_alias_id serial NOT NULL,
    user_email varchar NOT NULL,
    user_alias varchar NOT NULL,
    created_by varchar NOT NULL default 'jujugigi-api',
    created_on timestamptz NOT NULL default current_timestamp,
    updated_by varchar NOT NULL default 'jujugigi-api',
    updated_on timestamptz NOT NULL default current_timestamp,
    CONSTRAINT user_alias_pk PRIMARY KEY (user_alias_id),
    CONSTRAINT user_alias_unique_user_email UNIQUE (user_email),
    CONSTRAINT user_alias_unique_user_alias UNIQUE (user_alias)
);

CREATE TABLE IF NOT EXISTS public.user_image (
    user_image_id serial NOT NULL,
    user_email varchar NOT NULL REFERENCES public.user_alias (user_email) ON UPDATE CASCADE,
    image_id int NOT NULL REFERENCES public.image (image_id) ON UPDATE CASCADE,
    opened bool NOT NULL default false,
    created_by varchar NOT NULL default 'jujugigi-api',
    created_on timestamptz NOT NULL default current_timestamp,
    updated_by varchar NOT NULL default 'jujugigi-api',
    updated_on timestamptz NOT NULL default current_timestamp,
    CONSTRAINT user_image_pk PRIMARY KEY (user_image_id),
    CONSTRAINT user_image_unique_user_email_image_id UNIQUE (user_email, image_id)
);
CREATE INDEX IF NOT EXISTS user_image_index_created_on ON public.user_image (created_on);

CREATE TABLE IF NOT EXISTS public.stripe (
    event_id varchar,
    object varchar,
    api_version date,
    created_on timestamptz,
    data jsonb,
    livemode boolean,
    pending_webhooks int,
    request jsonb,
    type varchar,
    CONSTRAINT stripe_pk PRIMARY KEY (event_id)
);

CREATE VIEW public.rankings AS (
    SELECT 
        ua.user_alias, 
        count(CASE WHEN i.rarity = 1 THEN 1 END) as common_count,
        count(CASE WHEN i.rarity = 2 THEN 1 END) as uncommon_count,
        count(CASE WHEN i.rarity = 3 THEN 1 END) as rare_count,
        count(CASE WHEN i.rarity = 4 THEN 1 END) as epic_count,
        count(CASE WHEN i.rarity = 5 THEN 1 END) as unique_count,
        count(1) as total_count
    FROM image i
    JOIN user_image ui ON i.image_id = ui.image_id
    JOIN user_alias ua ON ui.user_email = ua.user_email
    WHERE ui.opened = TRUE
    GROUP BY ua.user_alias
    ORDER BY 7 DESC, 6 DESC, 5 DESC, 4 DESC, 3 DESC, 2 DESC
);