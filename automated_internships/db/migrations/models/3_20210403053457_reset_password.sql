-- upgrade --
CREATE TABLE IF NOT EXISTS "changepassword" (
    "value" VARCHAR(20) NOT NULL UNIQUE,
    "active" BOOL NOT NULL  DEFAULT False,
    "user_id" INT NOT NULL  PRIMARY KEY REFERENCES "user" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "changepassword";
