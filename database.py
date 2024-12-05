import aiosqlite

async def create_table():
    async with aiosqlite.connect('quiz_bot.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (
                                user_id INTEGER PRIMARY KEY, 
                                question_index INTEGER
                            )''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                user_id INTEGER PRIMARY KEY, 
                correct_answers INTEGER,
                total_questions INTEGER
            )
        ''')
        await db.commit()

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect('quiz_bot.db') as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()

async def get_quiz_index(user_id):
    async with aiosqlite.connect('quiz_bot.db') as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id, )) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def save_quiz_result(user_id, correct_answers, total_questions):
    async with aiosqlite.connect('quiz_bot.db') as db:
        await db.execute('''
            INSERT OR REPLACE INTO quiz_results (user_id, correct_answers, total_questions)
            VALUES (?, ?, ?)
        ''', (user_id, correct_answers, total_questions))
        await db.commit()

async def get_quiz_result(user_id):
    async with aiosqlite.connect('quiz_bot.db') as db:
        async with db.execute('''
            SELECT correct_answers, total_questions FROM quiz_results WHERE user_id = ?
        ''', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result if result else (0, 0)  # Если данных нет, вернуть (0, 0)

async def reset_stats(user_id):
    async with aiosqlite.connect('quiz_bot.db') as db:
        await db.execute('''
            UPDATE quiz_results 
            SET correct_answers = 0, total_questions = 0
            WHERE user_id = ?
        ''', (user_id,))
        await db.commit()