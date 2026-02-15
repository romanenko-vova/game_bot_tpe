import aiosqlite
# CRUD - Create, Read, Update, Delete
async def add_user(tg_id):
    db = await aiosqlite.connect("database.db")
    await db.execute("INSERT INTO users (tg_id) VALUES(?)", [tg_id])
    await db.commit()
    await db.close()
    
async def get_user(tg_id):
    db = await aiosqlite.connect("database.db")
    db.row_factory = aiosqlite.Row
    res = await db.execute("SELECT * FROM users WHERE tg_id = ?", [tg_id])
    user = await res.fetchone()
    await db.close()
    if user:
        return dict(user)
    return None