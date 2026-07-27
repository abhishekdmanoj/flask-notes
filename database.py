import psycopg2
import os
import time

#Connection, while making sure it will wait for Postgres to fully start up and ready


while True:
	try:
		conn = psycopg2.connect(
			host = os.getenv("POSTGRES_HOST"),
			database = os.getenv("POSTGRES_DB"),
			user = os.getenv("POSTGRES_USER"),
			password = os.getenv("POSTGRES_PASSWORD"),
			port = os.getenv("POSTGRES_PORT")
		)

		cursor = conn.cursor()
		print("Connected to PostgreSQL")
		break

	except psycopg2.OperationalError as e:
		print(f"Database connection failed: {e}")
		print("Retrying in 2 seconds...")
		time.sleep(2)

	except Exception as e:
		print(f"Unable to connect to Postgres database: {e}")
		raise


#Base table creation

try :
	cursor.execute("""CREATE TABLE IF NOT EXISTS users(
               id SERIAL PRIMARY KEY,
	       username TEXT UNIQUE NOT NULL,
	       email TEXT UNIQUE NOT NULL,
	       password_hash TEXT NOT NULL)
               """)

	conn.commit()
	print("Users table created")

except Exception as e:
	conn.rollback()
	print("Error creating users table.")
	print(e)
	raise


try:

	cursor.execute("""CREATE TABLE IF NOT EXISTS notes(
			id SERIAL PRIMARY KEY,
			note TEXT NOT NULL,
			user_id INTEGER NOT NULL REFERENCES users(id))
			""")

	conn.commit()
	print("Notes table created successfully.")

except Exception as e:
	conn.rollback()
	print(f"Error creating Notes table: {e}")
	raise
