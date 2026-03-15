import customtkinter as ctk
from pathlib import Path
import subprocess
import sys
from database.integrity import verify_integrity

from password import open_password_window


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# -------- Safe base path for EXE and Python --------
def get_base_path():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent


BASE_DIR = get_base_path()


# -------- Open database in DB Browser --------
def open_database():
    db_path = BASE_DIR / "database" / "security_log.db"

    print("Opening database:", db_path)

    if not db_path.exists():
        print("Database not found!")
        return

    db_browser = r"C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe"

    subprocess.Popen([db_browser, str(db_path)])

# -------- Main App --------
app = ctk.CTk()
app.geometry("400x300")
app.title("Fortify")

inti = verify_integrity()
label1 = ctk.CTkLabel(app, text="")
label1.pack()
if(inti):
    
    label1.configure(text="Database Integrity Verified")
else:
    label1.configure(text="⚠️TAMPER WARNING: Database modified!⚠️")
    
    

password_button = ctk.CTkButton(
    app,
    text="Check Password Strength",
    command=lambda: open_password_window(app)
)

password_button.pack(pady=20)


database_button = ctk.CTkButton(
    app,
    text="Check Database",
    command=open_database
)

database_button.pack(pady=10)


app.mainloop()