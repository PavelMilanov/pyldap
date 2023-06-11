from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "acts" RENAME COLUMN "file" TO "file_name";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "acts" RENAME COLUMN "file_name" TO "file";"""
