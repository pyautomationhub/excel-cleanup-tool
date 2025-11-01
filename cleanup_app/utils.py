import pandas as pd
import numpy as np
import re
import tempfile
import os

def cleanup_excel(file):
    df = pd.read_excel(file)

    def curata_text(x):
        if pd.isna(x):
            return np.nan
        x = str(x).strip()
        x = re.sub(r'\s+', ' ', x)
        x = x.capitalize()
        return x

    text_cols = ["Nume", "Prenume", "Departament", "Funcție", "Manager direct", "Oraș", "Tip contract", "Status"]
    for col in df.columns.intersection(text_cols):
        df[col] = df[col].astype(str).apply(curata_text)

    # Emailuri și telefoane
    if "Email" in df.columns:
        df["Email"] = df["Email"].str.lower().str.strip()

    if "Număr de telefon" in df.columns:
        df["Număr de telefon"] = df["Număr de telefon"].astype(str).str.replace(r"\s+", "", regex=True)

    # Salarii
    if "Salariu brut" in df.columns:
        df["Salariu brut"] = df["Salariu brut"].apply(
            lambda v: float(re.findall(r"\d+", str(v).replace("RON", ""))[0]) if re.findall(r"\d+", str(v)) else np.nan
        )

    # Date
    for col in ["Data nașterii", "Data angajării", "Data ultimei evaluări"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    # Eliminăm duplicate și rânduri goale
    df = df.drop_duplicates(subset=["Nume", "Prenume", "CNP"], keep="first").dropna(how="all")

    # Completăm câteva câmpuri lipsă
    if "Status" in df.columns:
        df["Status"] = df["Status"].fillna("Activ")
    if "Tip contract" in df.columns:
        df["Tip contract"] = df["Tip contract"].fillna("Permanent")

    # Salvăm fișierul curățat într-un fișier temporar
    cleaned_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    df.to_excel(cleaned_file.name, index=False)
    cleaned_file.close()
    return cleaned_file.name
