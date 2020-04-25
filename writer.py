#!/usr/bin/python3
import csv
import sys
import os
from tkinter import messagebox

def report_error(message):
    messagebox.showinfo("FEL!", message)
    os.exit(1)

translations = {
    b"\x86": b"!", # å
    b"\x84": b"\"", # ä
    b"\x94": b"#", # ö
    b"\x90": b"^", # ???
    b"\x8f": b"?", # Å
    b"\x8e": b"`", # Ä
    b"\x99": b"'", # Ö
}

def translate(translations, data):
    for a in translations:
        b = translations[a]
        data = data.replace(a, b)
    return data

def translate_back(translations, data):
    for a in translations:
        b = translations[a]
        data = data.replace(b, a)
    return data

TMP_FILENAME = "__tmp.csv"

print(len(sys.argv))
if len(sys.argv) < 2:
    report_error("Du gav in för få argument, ge in EN fil.")

if len(sys.argv) > 2:
    report_error("Du gav in förmånga argument, ge in EN fil.")

source_file = sys.argv[1]
if not source_file.endswith(".csv"):
    report_error("Kan bara läsa \".csv\" filer!")

dest_file = source_file.rsplit(".", 1)[0] + ".xml"

if not os.path.isfile(source_file):
    report_error("Kan inte hitta filen.")

with open("data.csv", "rb") as f:
    changed = f.read()
    changed = translate(translations, changed)
    tmp = open(TMP_FILENAME, "wb")
    tmp.write(changed)
    tmp.close()
    tmp = open(TMP_FILENAME, "r")
    reader = csv.DictReader(tmp, delimiter=";")

    preamble = b'<?xml version="1.0" encoding="utf-8"?><Parts xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    out = open(dest_file, "wb+")
    out.write(preamble)
    for row in reader:
        for key in row:
            if row[key]:
                data = f"<{key}>{row[key]}</{key}>".encode()
                data = translate_back(translations, data)
                out.write(data)
            else:
                out.write(f"<{key} />".encode())
    out.write(b"</Parts>")
    tmp.close()
    os.remove(TMP_FILENAME)

messagebox.showinfo("Hurra!", "Filen är nu konverterad till XML.")

