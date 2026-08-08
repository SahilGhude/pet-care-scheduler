import psycopg2

conn = psycopg2.connect(
    host="db.foobtedfwjvpfbmrozou.supabase.co",
    database="postgres",
    user="postgres",
    password="YOUR_PASSWORD",
    port=5432
)

print("Connected Successfully")