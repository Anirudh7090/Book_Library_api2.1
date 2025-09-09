from app.db.db import engine, Base

# Create all tables in the database
Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")
