async def run_import():
    from db.connection import init_db, close_db
    from laws.repo import clone_repo, repo_exists

    if not repo_exists():
        clone_repo()
    mongo_client = await init_db()

    try:
        from laws.importer import import_files

        await import_files()
    finally:
        close_db(mongo_client)
