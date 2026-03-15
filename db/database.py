import aiosqlite

async def create_tables(app):
    db = await aiosqlite.connect("database.db")
    await db.execute("""CREATE TABLE IF NOT EXISTS users(
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            tg_id BIGINT UNIQUE,
                                            name TEXT NULL,
                                            age INTEGER NULL,
                                            amount_of_games INTEGER DEFAULT 0
                                            )""")
    
    # БД после запроса поменялась? Да.
    await db.commit() # сохраниться
    await db.close() # закрыть соединение
    
    
