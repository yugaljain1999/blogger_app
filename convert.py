from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import reflection
from sqlalchemy.schema import CreateTable
import sqlalchemy
import os

# === CONFIGURATION ===
mysql_url = "mysql+pymysql://root:root9896@127.0.0.1:3306/BlogApp"
sqlite_path = "output.sqlite"  # Output SQLite file

# === Connect to MySQL ===
mysql_engine = create_engine(mysql_url)
metadata = MetaData()
metadata.reflect(bind=mysql_engine)

# === Connect to SQLite ===
if os.path.exists(sqlite_path):
    os.remove(sqlite_path)
sqlite_engine = create_engine(f"sqlite:///{sqlite_path}")
metadata.create_all(bind=sqlite_engine)

# === Copy Data Table by Table ===
with mysql_engine.connect() as mysql_conn:
    with sqlite_engine.begin() as sqlite_conn:
        for table in metadata.sorted_tables:
            print(f"Migrating table: {table.name}")
            result = mysql_conn.execute(table.select())
            rows = [dict(row._mapping) for row in result]
            if rows:
                sqlite_conn.execute(table.insert(), rows)



print("✅ Migration complete! SQLite DB created at:", sqlite_path)
