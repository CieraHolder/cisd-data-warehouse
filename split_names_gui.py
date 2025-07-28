import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
from sqlalchemy import create_engine, text

class NameSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Split Student Names - CISD")
        self.root.geometry("400x210")
        self.root.configure(bg="#F4F4F9")

        ttk.Label(root, text="CISD: Split Student Names", font=("Helvetica", 16, "bold"), background="#F4F4F9", foreground="#265073").pack(pady=10)

        self.status_label = ttk.Label(root, text="", background="#F4F4F9")
        self.status_label.pack(pady=5)

        ttk.Button(root, text="Split & Update Names", command=self.run_split).pack(pady=6)
        ttk.Button(root, text="Exit", command=self.root.quit).pack(side=tk.BOTTOM, pady=8)

    def run_split(self):
        self.status_label.config(text="Connecting to database...")
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

        df = pd.read_sql('SELECT student_id, student_name FROM student_profile', engine)

        # Split names
        def split_name(full_name):
            if pd.isna(full_name) or str(full_name).strip() == "":
                return pd.Series([None, None])
            parts = full_name.strip().split()
            if len(parts) == 0:
                return pd.Series([None, None])
            elif len(parts) == 1:
                return pd.Series([parts[0], None])
            else:
                return pd.Series([parts[0], parts[-1]])

        split = df['student_name'].apply(split_name)
        df['first_name'] = split[0]
        df['last_name'] = split[1]

        # Calculate updates/skipped
        num_to_update = df['first_name'].notna().sum()
        num_skipped = df['first_name'].isna().sum()

        summary = (
            f"{num_to_update} records will be updated with split names.\n"
            f"{num_skipped} records have no name and will be skipped.\n\n"
            f"Do you want to commit these changes?"
        )

        proceed = messagebox.askyesno("Are You Sure?", summary)
        if not proceed:
            self.status_label.config(text="Operation cancelled. No changes made.")
            return

        # Perform updates
        self.status_label.config(text="Updating records in database...")
        self.root.update()

        updated = 0
        with engine.begin() as conn:
            for i, row in df.iterrows():
                if pd.notna(row['first_name']):
                    sql = text("""
                        UPDATE student_profile
                        SET first_name = :first, last_name = :last
                        WHERE student_id = :id
                    """)
                    result = conn.execute(sql, {"first": row['first_name'], "last": row['last_name'], "id": row['student_id']})
                    if result.rowcount > 0:
                        updated += 1

        self.status_label.config(text=f"✅ {updated} records updated.")
        messagebox.showinfo("Done!", f"{updated} names split and updated in the database.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NameSplitterApp(root)
    root.mainloop()
