import sys
import os
sys.path.append(os.getcwd())
from app.database.connection import SessionLocal
from sqlalchemy import text

db = SessionLocal()
try:
    db.execute(text("ALTER TABLE seller_requests ADD COLUMN district TEXT DEFAULT 'CHENNAI'"))
    db.commit()
    print('Added district to seller_requests successfully!')
except Exception as e:
    print('Error or already exists:', e)
