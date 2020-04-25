#!/usr/bin/python3

#
# ============= LICENSE =============
#
# Skrivet av: Edvard Thörnros
# Email:      edvard@thornros.com
# Datum:      2020-04-25
#
# Om du finner detta script användbart får du gärna typ, ge mig pengar,
# fattig student liksom. Om du hittar något som inte fungerar är det
# bara att skicka ett mail till edvard@thornros.com så tittar jag på det.
# Du får gärna distrubura det till någon som eventuellt behöver det.
# Jag är inte ansvarig för potentiell skada som detta script gör och om du
# gör ändringar i det bör du även ändra denna text.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#

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

