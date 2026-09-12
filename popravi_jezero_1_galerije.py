"""
popravi_jezero_1_galerije.py
------------------------------
Za objekat "Jezero", zgrada/Objekat 1 (stanovi sa naslovom "Jezero I-XX"),
postavlja tacnu i cistu galeriju za svaki stan: TACNO dve slike -
1) osnova (plan) samog stana, 2) slika pozicije tog stana na celom spratu
(sa zelenim oznacenim stanom).

Stanovi na istoj "vertikali" (isti raspored na Prizemlju/Prvom/Drugom
spratu) dele isti plan i istu poziciju - to je tacno onako kako su i same
slike napravljene (npr. P5_I11_II17 pokriva stanove 5, 11 i 17).

Pokrenuti iz foldera sajta:

    python popravi_jezero_1_galerije.py
"""

import re
import json

STANOVI_JS = "stanovi.js"

# broj stana -> (plan slika, pozicija slika), sve unutar "slike/"
GRUPE = [
    ([1], "Stan-broj-1.webp", "1_1.webp"),
    ([2], "Stan-broj-2.webp", "1_2.webp"),
    ([3], "Stan-broj-3.webp", "1_3.webp"),
    ([4], "Stan-4-bjekat-1.webp", "1_4.webp"),
    ([5, 11, 17], "P5_I11_II17-Objekat-1.webp", "1_51117.webp"),
    ([6, 12, 18], "P6_I12_II18-Objekat-1.webp", "1_61218.webp"),
    ([7, 13, 19], "P7_I13_II19-Objekat-1.webp", "1_71319.webp"),
    ([8, 14, 20], "P8_I14_II20-Objekat-1-NASLOVNA.webp", "1_81420.webp"),
    ([9, 15, 21], "P9_I15_II21-Objekat-1.webp", "1_91521.webp"),
    ([10, 16, 22], "P10_I16_II22-Objekat-1-NASLOVNA.webp", "1_101622.webp"),
    ([23], "PS23-Objekat-1.webp", "1_23.webp"),
    ([24], "PS24-Objekat-1.webp", "1_24.webp"),
    ([25], "PS25-Objekat-1.webp", "1_25.webp"),
    ([26], "PS26-Objekat-1.webp", "1_26.webp"),
    ([27], "PS27-Objekat-1.webp", "1_27.webp"),
    ([28], "PS28-Objekat-1.webp", "1_28.webp"),
]

BROJ_U_SLIKE = {}
for brojevi, plan, pozicija in GRUPE:
    for b in brojevi:
        BROJ_U_SLIKE[b] = (plan, pozicija)

NASLOV_RE = re.compile(r"^Jezero I-(\d+)$")


def ucitaj_stanovi_js(putanja):
    with open(putanja, "r", encoding="utf-8") as f:
        sadrzaj = f.read()
    m = re.search(r"=\s*(\[.*\])\s*;?\s*$", sadrzaj, re.DOTALL)
    if not m:
        raise ValueError(f"Nisam uspeo da pronadjem JSON niz unutar {putanja}")
    return json.loads(m.group(1))


def sacuvaj_stanovi_js(putanja, stanovi):
    js_izlaz = f"const podaciStanovi = {json.dumps(stanovi, indent=2, ensure_ascii=False)};\n"
    with open(putanja, "w", encoding="utf-8") as f:
        f.write(js_izlaz)


def main():
    stanovi = ucitaj_stanovi_js(STANOVI_JS)

    promenjeno = 0
    nepoklopljeno = []
    for x in stanovi:
        if x.get("objekat") != "Jezero":
            continue
        m = NASLOV_RE.match(x.get("naslov", ""))
        if not m:
            continue
        broj = int(m.group(1))
        par = BROJ_U_SLIKE.get(broj)
        if not par:
            nepoklopljeno.append(x.get("naslov"))
            continue
        plan, pozicija = par
        nova_galerija = [f"slike/{plan}", f"slike/{pozicija}"]
        x["slika"] = f"slike/{plan}"
        x["galerija"] = nova_galerija
        promenjeno += 1
        print(f"[OK] {x['id']} ({x['naslov']}): slika + pozicija postavljene")

    sacuvaj_stanovi_js(STANOVI_JS, stanovi)
    print(f"\nUkupno azurirano: {promenjeno} stanova")
    if nepoklopljeno:
        print("Nepoklopljeno (broj stana nije prepoznat):", nepoklopljeno)


if __name__ == "__main__":
    main()
