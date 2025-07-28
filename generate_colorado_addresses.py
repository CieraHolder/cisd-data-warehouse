import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine, text
from faker import Faker
import random

class AddressGenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CISD Student Address Generator")
        self.root.geometry("480x230")
        self.root.configure(bg="#F4F4F9")

        tk.Label(root, text="CISD Student Address Generator",
                 font=('Helvetica', 16, 'bold'), bg='#F4F4F9', fg='#265073').pack(pady=12)

        self.run_btn = ttk.Button(root, text="Generate & Update Douglas County Addresses", command=self.run_address_gen)
        self.run_btn.pack(pady=6)

        self.status_label = tk.Label(root, text="", font=('Helvetica', 11), bg='#F4F4F9', fg='#333333')
        self.status_label.pack(pady=2)

        self.count_label = tk.Label(root, text="", font=('Consolas', 11, 'bold'), bg='#F4F4F9', fg='#008040')
        self.count_label.pack(pady=10)

        ttk.Button(root, text="Exit", command=self.root.quit).pack(side=tk.BOTTOM, pady=10)

    def run_address_gen(self):
        self.status_label.config(text="Connecting to database...")
        self.count_label.config(text="")
        self.root.update()

        # Database connection
        DB_USER = 'CieraH0lder'
        DB_PASSWORD = 'Getj0b!'
        DB_HOST = 'localhost'
        DB_PORT = '5432'
        DB_NAME = 'CISD'

        engine = create_engine(
            f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        )

        # Fetch all student IDs
        df = pd.read_sql('SELECT student_id FROM student_profile', engine)

        # Douglas County cities and ZIP codes
        douglas_cities = [
            ("Castle Rock", "80104"),
            ("Castle Pines", "80108"),
            ("Highlands Ranch", "80126"),
            ("Parker", "80134"),
            ("Lone Tree", "80124"),
            ("Larkspur", "80118"),
            ("Sedalia", "80135"),
            ("Roxborough Park", "80125"),
            ("Franktown", "80116")
        ]

        fake = Faker()

        def generate_douglas_address():
            street = fake.street_address()
            city, zipcode = random.choice(douglas_cities)
            return f"{street}, {city}, CO {zipcode}"

        # Generate Douglas County addresses
        df['address'] = [generate_douglas_address() for _ in range(len(df))]

        # Confirmation dialog
        summary = (
            f"This will generate and update Douglas County addresses for {len(df)} student records.\n\n"
            f"Do you want to continue?"
        )
        proceed = messagebox.askyesno("Are You Sure?", summary)
        if not proceed:
            self.status_label.config(text="Operation cancelled. No changes made.")
            return

        self.status_label.config(text="Updating addresses in database...")
        self.root.update()

        updated = 0
        with engine.begin() as conn:
            for i, row in df.iterrows():
                sql = text("UPDATE student_profile SET address = :addr WHERE student_id = :id")
                result = conn.execute(sql, {"addr": row['address'], "id": row['student_id']})
                if result.rowcount > 0:
                    updated += 1

        self.status_label.config(text=f"✅ {updated} addresses updated.")
        self.count_label.config(text=f"{updated} records updated.")
        messagebox.showinfo("Done!", f"{updated} Douglas County addresses generated and added to the database.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AddressGenApp(root)
    root.mainloop()
