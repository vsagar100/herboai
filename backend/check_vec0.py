import sqlite3
from sqlite_vec import load as load_sqlite_vec, serialize_float32

conn = sqlite3.connect(":memory:")
conn.enable_load_extension(True)
load_sqlite_vec(conn)  # registers vec0 in this connection

# Create a tiny demo table with 3-D vectors
conn.execute("""
CREATE VIRTUAL TABLE demo USING vec0(
  id INTEGER PRIMARY KEY,
  name TEXT,
  embedding FLOAT[3]
);
""")

# Insert two points
v1 = serialize_float32([0.1, 0.2, 0.3])
v2 = serialize_float32([0.1, 0.21, 0.31])
conn.execute("INSERT INTO demo(name, embedding) VALUES (?,?)", ("a", v1))
conn.execute("INSERT INTO demo(name, embedding) VALUES (?,?)", ("b", v2))
conn.commit()

# Query nearest to a probe
probe = serialize_float32([0.1, 0.205, 0.305])
rows = conn.execute("""
  SELECT id, name, distance
  FROM demo
  WHERE embedding MATCH ?
    AND k = 2
""", (probe,)).fetchall()

print("KNN:", [(r[1], r[2]) for r in rows])  # [('b', ...), ('a', ...)]
