-- upgrade --
CREATE TABLE IF NOT EXISTS "adminuser" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "password" VARCHAR(200) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_superuser" BOOL NOT NULL  DEFAULT False
);
COMMENT ON COLUMN "adminuser"."password" IS 'Will auto hash with raw password when change';
CREATE TABLE IF NOT EXISTS "permission" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "label" VARCHAR(50) NOT NULL,
    "model" VARCHAR(50) NOT NULL,
    "action" SMALLINT NOT NULL  DEFAULT 4
);
COMMENT ON COLUMN "permission"."action" IS 'create: 1\ndelete: 2\nupdate: 3\nread: 4';
CREATE TABLE IF NOT EXISTS "role" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "label" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "first_name" VARCHAR(63) NOT NULL,
    "last_name" VARCHAR(63) NOT NULL,
    "password" VARCHAR(127) NOT NULL,
    CONSTRAINT "uid_user_first_n_340da3" UNIQUE ("first_name", "last_name")
);
CREATE TABLE IF NOT EXISTS "adminlog" (
    "admin_log_id" SERIAL NOT NULL PRIMARY KEY,
    "action" VARCHAR(20) NOT NULL,
    "model" VARCHAR(50) NOT NULL,
    "content" JSONB NOT NULL,
    "admin_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "role_permission" (
    "role_id" INT NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE,
    "permission_id" INT NOT NULL REFERENCES "permission" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "role_user" (
    "role_id" INT NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
