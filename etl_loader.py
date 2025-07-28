import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from sqlalchemy import create_engine

class ETLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CISD - Ciera Independent School District ETL Student Files")
        self.root.geometry("540x350")
        self.root.configure(bg='#F4F4F9')

        self.file_path = tk.StringVar()

        # Title Label
        tk.Label(root, text="CISD ETL: Student Files Loader",
                 font=('Helvetica', 18, 'bold'), bg='#F4F4F9', fg='#265073').pack(pady=10)

        # Browse Button
        self.browse_btn = ttk.Button(root, text="Browse for CSV File", command=self.browse_file)
        self.browse_btn.pack(pady=(5, 2))

        # File Location Display
        tk.Label(root, text="Selected file:", font=('Helvetica', 10, 'italic'),
                 bg='#F4F4F9').pack()
        self.file_display = tk.Entry(root, textvariable=self.file_path, width=65, state='readonly',
                                     font=('Consolas', 9))
        self.file_display.pack(pady=(0, 10))

        # Progress Label
        self.progress_label = tk.Label(root, text="", bg='#F4F4F9', fg='#5C5C5C', font=('Helvetica', 10))
        self.progress_label.pack(pady=(0, 6))

        # Visual List of Loaded Files
        self.load_listbox = tk.Listbox(root, width=70, height=8, font=('Consolas', 10), bg='#EAF2FB')
        self.load_listbox.pack(pady=(5, 8))

        # Exit Button
        ttk.Button(root, text="Exit", command=self.root.quit).pack(side=tk.BOTTOM, pady=8)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if file_path:
            self.file_path.set(file_path)
            self.progress_label.config(text="Processing file, please wait...")
            self.root.update()
            self.run_etl(file_path)

    def run_etl(self, file_path):
        try:
            # Show visual feedback in listbox
            self.load_listbox.delete(0, tk.END)
            self.load_listbox.insert(tk.END, f"Loading: {file_path}")

            # DB connection settings
            DB_USER = 'CieraH0lder'
            DB_PASSWORD = 'Getj0b!'
            DB_HOST = 'localhost'
            DB_PORT = '5432'
            DB_NAME = 'CISD'

            engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip().str.lower()

            # --- ETL ---
            student_df = df[[ 'gender', 'peer_influence', 'learning_disabilities', 'distance_from_home', 'motivation_level', 'sleep_hours', 'attendance' ]]
            household_df = df[[ 'parental_education_level', 'parental_involvement', 'internet_access', 'family_income', 'distance_from_home', 'access_to_resources' ]]
            academics_df = df[[ 'hours_studied', 'previous_scores', 'tutoring_sessions', 'teacher_quality', 'school_type', 'attendance', 'exam_score' ]]

            # Confirm before loading
            summary = (
                f"Ready to insert:\n\n"
                f"Student Profiles: {len(student_df)}\n"
                f"Household Profiles: {len(household_df)}\n"
                f"Student Academics: {len(academics_df)}\n\n"
                f"Do you want to continue?"
            )
            proceed = messagebox.askyesno("Confirm Insert", summary)
            if not proceed:
                self.progress_label.config(text="Operation cancelled. No data inserted.")
                return

            # Insert & visualize each step
            self.load_listbox.insert(tk.END, "Inserting student profiles...")
            self.root.update()
            student_df.to_sql('student_profile', engine, if_exists='append', index=False)

            self.load_listbox.insert(tk.END, "Fetching new student IDs...")
            self.root.update()
            student_ids = pd.read_sql(
                f"SELECT student_id FROM student_profile ORDER BY student_id DESC LIMIT {len(student_df)}",
                engine
            ).iloc[::-1].reset_index(drop=True)
            household_df['student_id'] = student_ids['student_id']
            academics_df['student_id'] = student_ids['student_id']

            self.load_listbox.insert(tk.END, "Inserting household profiles...")
            self.root.update()
            household_df.to_sql('household_profile', engine, if_exists='append', index=False)

            self.load_listbox.insert(tk.END, "Inserting student academics...")
            self.root.update()
            academics_df.to_sql('student_academics', engine, if_exists='append', index=False)

            self.progress_label.config(text="✅ All data inserted successfully!")
            self.load_listbox.insert(tk.END, "Done!")
            messagebox.showinfo("Success", "✅ ETL complete!")

        except Exception as e:
            self.progress_label.config(text="❌ Error during ETL process!")
            self.load_listbox.insert(tk.END, f"Error: {str(e)}")
            messagebox.showerror("Error", f"ETL failed:\n{str(e)}")

# --- Launch the GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ETLApp(root)
    root.mainloop()