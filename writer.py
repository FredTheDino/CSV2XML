#!/usr/bin/python3
import csv

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

with open("data.csv", "rb") as f:
    changed = f.read()
    changed = translate(translations, changed)
    tmp = open("tmp.csv", "wb")
    tmp.write(changed)
    tmp.close()
    tmp = open("tmp.csv", "r")
    reader = csv.DictReader(tmp, delimiter=";")

    preamble = b'<?xml version="1.0" encoding="utf-8"?><Parts xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    out = open("out.xml", "wb+")
    out.write(preamble)
    for row in reader:
        for key in row:
            if row[key]:
                tmp = f"<{key}>{row[key]}</{key}>".encode()
                tmp = translate_back(translations, tmp)
                out.write(tmp)
            else:
                out.write(f"<{key} />".encode())
    out.write(b"</Parts>")


