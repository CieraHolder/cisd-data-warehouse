import pandas as pd
from sqlalchemy import create_engine, text

# Database connection info
DB_USER = 'CieraH0lder'
DB_PASSWORD = 'Getj0b!'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'CISD'

engine = create_engine(
    f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

# Fetch student_id and address from student_profile
df = pd.read_sql('SELECT student_id, address FROM student_profile', engine)

# Helper to split address
def split_address(addr):
    try:
        # Expects: 123 Main St, Castle Rock, CO 80104
        if pd.isna(addr):
            return pd.Series([None, None, None, None])
        parts = addr.split(',')
        if len(parts) != 3:
            return pd.Series([None, None, None, None])
        street = parts[0].strip()
        city = parts[1].strip()
        state_zip = parts[2].strip().split()
        state = state_zip[0] if len(state_zip) > 0 else None
        zipcode = state_zip[1] if len(state_zip) > 1 else None
        return pd.Series([street, city, state, zipcode])
    except Exception as e:
        print(f"Error splitting address '{addr}': {e}")
        return pd.Series([None, None, None, None])

df[['street', 'city', 'state', 'zipcode']] = df['address'].apply(split_address)

# Insert into student_address
with engine.begin() as conn:
    inserted = 0
    for i, row in df.iterrows():
        if pd.notna(row['student_id']) and pd.notna(row['street']):
            sql = text("""
                INSERT INTO student_address (student_id, street, city, state, zipcode)
                VALUES (:student_id, :street, :city, :state, :zipcode)
            """)
            conn.execute(sql, {
                "student_id": row['student_id'],
                "street": row['street'],
                "city": row['city'],
                "state": row['state'],
                "zipcode": int(row['zipcode']) if str(row['zipcode']).isdigit() else None
            })
            inserted += 1

print(f"✅ Done! Inserted {inserted} rows with student_id into student_address table.")

