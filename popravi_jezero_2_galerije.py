"""
popravi_jezero_2_galerije.py
------------------------------
Za objekat "Jezero", zgrada/Objekat 2 (stanovi sa naslovom "Jezero II-XX"),
postavlja tacnu galeriju: SAMO slika plana samog stana (bez slike pozicije
na spratu, jer za Objekat 2 nemamo pouzdane slike pozicije - raspored
stanova po spratu se razlikuje od Objekta 1, pa bi kopiranje pozicije sa
Objekta 1 pokazivalo pogresnu kvadraturu za vecinu stanova).

Mapiranje je provereno tako sto se kvadratura na slici plana poklapa sa
kvadraturom stana u stanovi.js.

Pokrenuti iz foldera sajta:

    python popravi_jezero_2_galerije.py
"""

import re
import json

STANOVI_JS = "stanovi.js"

# broj stana -> plan slika (unutar "slike/")
GRUPE = [
    ([1], "Stan-broj-1-suteren-naslovna-3.webp"),
    ([2], "Stan-2-Objekat-2.webp"),
    ([3], "Stan-3-Objekat-2.webp"),
    ([4], "Stan-broj-4-suteren-naslovna-1.webp"),
    ([5], "Prizemlje-Stan-broj-5.webp"),
    ([6, 11, 17], "Stan-broj-6-11-i-17-naslovna.webp"),
    ([7, 8, 12, 13, 18, 19], "Stan-broj-7-i-8-i-12-i-13-i-18-i-19-naslovna.webp"),
    ([9, 14, 20], "P9_I14_II20-Objekat-2-NASLOVNA.webp"),
    ([10], "Prizemlje-Stan-broj-10.webp"),
    ([15, 21], "I15_II21-Objekat-2.webp"),
    ([16, 22], "I16_II22-Objekat-2.webp"),
    ([23], "PS-23.webp"),
    ([25], "PS-25.webp"),
    ([26], "PS-26.webp"),
    ([27], "PS-27.webp"),
    ([28], "PS-28.webp"),
]

BROJ_U_SLIKU = {}
for brojevi, plan in GRUPE:
    for b in brojevi:
        BROJ_U_SLIKU[b] = plan

NASLOV_RE = re.compile(r"^Jezero II-(\d+)$")


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
        plan = BROJ_U_SLIKU.get(broj)
        if not plan:
            nepoklopljeno.append(x.get("naslov"))
            continue
        x["slika"] = f"slike/{plan}"
        x["galerija"] = [f"slike/{plan}"]
        promenjeno += 1
        print(f"[OK] {x['id']} ({x['naslov']}, {x.get('kvadratura')}m2): {plan}")

    sacuvaj_stanovi_js(STANOVI_JS, stanovi)
    print(f"\nUkupno azurirano: {promenjeno} stanova")
    if nepoklopljeno:
        print("Nepoklopljeno (broj stana nije prepoznat):", nepoklopljeno)


if __name__ == "__main__":
    main()
