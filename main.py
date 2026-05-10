from src.utils.db import engine

conn = engine.connect()

print("CONNECTED TO NEON DB!")