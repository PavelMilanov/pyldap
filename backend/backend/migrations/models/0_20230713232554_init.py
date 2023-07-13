from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "acts" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "file_name" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "customers" (
    "name" VARCHAR(15) NOT NULL  PRIMARY KEY,
    "act_id_id" UUID REFERENCES "acts" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "static_ip" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "ip" VARCHAR(15) NOT NULL UNIQUE,
    "description" TEXT
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
