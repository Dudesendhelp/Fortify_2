# Fortify

A small Windows desktop app (CustomTkinter) to:

- Check password strength (basic character-set checks + entropy)
- Generate a QR code from the password
- Log security events to a local SQLite database (`database/security_log.db`)

## Project layout

- `Fortify.py`: main GUI entry point
- `password.py`: password checker + QR generator window
- `Password_checker/`: password scoring + common-password utilities
- `database/`: SQLite logging and integrity fingerprinting

## Setup (run from source)

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Run the app:

```bash
python Fortify.py
```

## Important: generate the common-password hash table

`Password_checker/code/password_importer.py` expects a file at:

`Password_checker/common_passwords/password_hash_table.pkl`

If that file is missing, the app will crash when you submit a password / generate a QR.

To generate it from the included CSV:

```bash
cd Password_checker\common_passwords
python hash_table.py
```

That script reads `common_passwords.csv` and writes `password_hash_table.pkl` in the same folder.

## Database

Logs are stored in:

- Source run: `database/security_log.db`
- Frozen EXE: `<folder_with_exe>\database\security_log.db`

The app writes rows into a `security_events` table (`timestamp`, `event_type`, `security_score`).

## Building an EXE (PyInstaller)

If you use PyInstaller directly, a typical build looks like:

```bash
pyinstaller --noconsole --onefile Fortify.py
```

Notes:

- You must include runtime data files next to the EXE (or bundle them), especially:
  - `Password_checker\common_passwords\password_hash_table.pkl`
  - (optional) `database\` folder if you want a pre-existing DB
- When running as an EXE, the database is created/updated next to the EXE under `database\security_log.db`.

## Troubleshooting

- **Submit/QR does nothing or crashes**: generate `password_hash_table.pkl` (see above).
- **No DB rows written**: ensure the EXE has permission to create `<exe_folder>\database\security_log.db` and that you are opening the same DB file the app writes to.
