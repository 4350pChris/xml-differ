from db.connection import init_db, close_db
from laws.repo import clone_repo, repo_exists


async def run_import(connection_string: str):
    if not repo_exists():
        clone_repo()
    mongo_client = await init_db(connection_string)

    try:
        from laws.importer import import_files

        await import_files()
    finally:
        close_db(mongo_client)
