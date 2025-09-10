from app.db.db import engine, Base


Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")
