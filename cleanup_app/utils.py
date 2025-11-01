# utils.py

import pandas as pd
import numpy as np
import re
import tempfile

def cleanup_excel(file):
    """
    Curăță orice fișier Excel încărcat:
    - spații și caractere neuniforme în text
    - normalizează valorile numerice
    - detectează coloanele ce par date și le convertește
    - elimină duplicate și rânduri complet goale
    - returnează calea către fișierul temporar curățat
    """
    df = pd.read_excel(file)

    # 🔹 Curățare text în toate coloanele de tip object
    def curata_text(x):
        if pd.isna(x):
            return np.nan
        x = str(x).strip()
        x = re.sub(r'\s+', ' ', x)  # elimină spații multiple
        return x

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].apply(curata_text)

    # 🔹 Normalizare valori numerice
    for col in df.columns:
        # dacă conținutul poate fi numeric, îl convertim
        df[col] = pd.to_numeric(df[col], errors="ignore")

    # 🔹 Detectare automat coloane ce par date
    for col in df.columns:
        if df[col].dtype == "object":
            sample = df[col].dropna().astype(str).head(10)
            if sample.str.contains(r'\d{4}|\d{1,2}/\d{1,2}/\d{2,4}', regex=True).any():
                try:
                    df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
                except:
                    pass

    # 🔹 Elimină duplicate (pe toate coloanele) și rânduri complet goale
    df = df.drop_duplicates().dropna(how="all")

    # 🔹 Salvare fișier curățat într-un fișier temporar
    cleaned_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    df.to_excel(cleaned_file.name, index=False)
    cleaned_file.close()

    return cleaned_file.name
