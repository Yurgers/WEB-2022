import sqlite3

conn = sqlite3.connect(r'../mt_web_8.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
	"id"	INTEGER,
	"username"	TEXT UNIQUE,
	"password"  TEXT,
	"name"	TEXT,
	"email" TEXT UNIQUE,
	"gender"	TEXT,
	"birthdate"  INTEGER,
	"is_active"  INTEGER DEFAULT 1,
	PRIMARY KEY("id" AUTOINCREMENT)
)	
""")

conn.commit()