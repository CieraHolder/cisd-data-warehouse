import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine, text
from faker import Faker

class NameGenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CISD Student Name Generator")
        self.root.geometry("450x230")
        self.root.configure(bg='#F4F4F9')

        # Title Label
        tk.Label(root, text="CISD Student Name Generator",
                 font=('Helvetica', 16, 'bold'), bg='#F4F4F9', fg='#265073').pack(pady=12)

        # Button to start name generation
        self.run_btn = ttk.Button(root, text="Generate & Update Student Names", command=self.run_name_gen)
        self.run_btn.pack(pady=(8, 8))

        # Status Display
        self.status_label = tk.Label(root, text="", font=('Helvetica', 11), bg='#F4F4F9', fg='#333333')
        self.status_label.pack(pady=2)

        # Records updated display
        self.records_label = tk.Label(root, text="", font=('Consolas', 11, 'bold'), bg='#F4F4F9', fg='#008040')
        self.records_label.pack(pady=10)

        # Exit Button
        ttk.Button(root, text="Exit", command=self.root.quit).pack(side=tk.BOTTOM, pady=10)

    def run_name_gen(self):
        self.status_label.config(text="Connecting to database and fetching students...")
        self.records_label.config(text="")
        self.root.update()

        try:
            # Database connection config
            DB_USER = 'CieraH0lder'
            DB_PASSWORD = 'Getj0b!'
            DB_HOST = 'localhost'
            DB_PORT = '5432'
            DB_NAME = 'CISD'

            engine = create_engine(
                f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
            )

            # Fetch student_id and gender
            df = pd.read_sql('SELECT student_id, gender FROM student_profile', engine)

            fake = Faker()
            def gen_name(gender):
                g = str(gender).strip().lower()
                if g in ['male', 'm']:
                    return fake.name_male()
                elif g in ['female', 'f']:
                    return fake.name_female()
                else:
                    return fake.name()

            self.status_label.config(text="Generating names...")
            self.root.update()
            df['student_name'] = df['gender'].apply(gen_name)

            self.status_label.config(text="Updating records in database...")
            self.root.update()

            update_count = 0
            with engine.begin() as conn:
                for i, row in df.iterrows():
                    sql = text(
                        "UPDATE student_profile SET student_name = :name WHERE student_id = :id"
                    )
                    result = conn.execute(sql, {"name": row['student_name'], "id": row['student_id']})
                    if result.rowcount > 0:
                        update_count += 1

            self.status_label.config(text="✅ Done!")
            self.records_label.config(text=f"{update_count} records updated.")
            messagebox.showinfo("Complete", f"✅ {update_count} student names generated and updated!")

        except Exception as e:
            self.status_label.config(text="❌ Error during name generation.")
            self.records_label.config(text="")
            messagebox.showerror("Error", f"Failed to generate/update student names:\n\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NameGenApp(root)
    root.mainloop()
