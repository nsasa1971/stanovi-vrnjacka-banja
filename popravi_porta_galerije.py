"""
popravi_porta_galerije.py
------------------------------
Za objekat "Porta Infinitas" (Porta 1, 2 i 3), svaki stan trenutno ima:
- "slika" (naslovna) = generican "stan_XXXX.webp" fajl
- "galerija" = jedan ili vise DRUGIH fajlova koji prikazuju ISTI plan stana,
  samo u drugoj rezoluciji/kompresiji (npr. P1S3.webp 1108x1108 i
  P1-Stan-3.webp 601x601 su ista skica stana, samo razlicit kvalitet)

Stanovi na istoj poziciji u zgradi (isti "tip" stana - prepoznat po
kvadraturi) dele identican plan - potvrdjeno vizuelno i poredjenjem
velicina/rezolucije fajlova (byte-identicni ili vizuelno identicni fajlovi).

Ova skripta za svaku grupu stanova istog tipa bira JEDNU, najkvalitetniju
sliku (najveca rezolucija, pa najveca velicina fajla) i postavlja je i kao
"slika" i kao jedinu stavku u "galerija" za sve stanove tog tipa.

Pokrenuti iz foldera sajta:

    python popravi_porta_galerije.py
"""

import re
import json

STANOVI_JS = "stanovi.js"

# (prefiks naslova, kvadratura) -> najkvalitetnija slika (unutar "slike/")
TIPOVI = {
    ("Porta 1", 32.53): "P1S1-crop.webp",
    ("Porta 1", 33.25): "P1S2-crop.webp",
    ("Porta 1", 37.12): "P1S3-crop.webp",
    ("Porta 1", 29.92): "P1S4-crop.webp",
    ("Porta 1", 31.65): "P1S5-crop.webp",
    ("Porta 1", 32.06): "P1S6-crop.webp",
    ("Porta 1", 23): "P1S7-crop.webp",
    ("Porta 1", 32.9): "P1-Stan-8-crop.webp",
    ("Porta 1", 37.98): "P1-Stan-13-crop.webp",
    ("Porta 1", 33.93): "P1-Stan-24-crop.webp",
    ("Porta 1", 67.31): "P1-Stan-25-crop.webp",
    ("Porta 2", 37.12): "P2-Stan-3-crop.webp",
    ("Porta 2", 29.92): "stan_4264-crop.webp",
    ("Porta 2", 31.65): "stan_4267-crop.webp",
    ("Porta 2", 32.06): "stan_4271-crop.webp",
    ("Porta 2", 32.9): "stan_4274-crop.webp",
    ("Porta 2", 33.93): "stan_4280-crop.webp",
    ("Porta 2", 38.22): "P2-Stan-3-1-crop.webp",
    ("Porta 2", 74.77): "P2-Stan-21-crop.webp",
    ("Porta 2", 76.25): "P2-Stan-22-crop.webp",
    ("Porta 3", 37.12): "P3-Stan-5-crop.webp",
    ("Porta 3", 29.92): "stan_4298-crop.webp",
    ("Porta 3", 31.65): "stan_4303-crop.webp",
    ("Porta 3", 32.06): "stan_4307-crop.webp",
    ("Porta 3", 23): "stan_4310-crop.webp",
    ("Porta 3", 32.9): "stan_4311-crop.webp",
    ("Porta 3", 33.93): "stan_4314-crop.webp",
    ("Porta 3", 67.31): "stan_4315-crop.webp",
    ("Porta 3", 37.98): "stan_4316-crop.webp",
}


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


def zgrada_prefiks(naslov):
    delovi = naslov.split(" ")
    return " ".join(delovi[:2])  # "Porta 1", "Porta 2", "Porta 3"


def main():
    stanovi = ucitaj_stanovi_js(STANOVI_JS)

    promenjeno = 0
    nepoklopljeno = []
    for x in stanovi:
        if x.get("objekat") != "Porta Infinitas":
            continue
        kljuc = (zgrada_prefiks(x.get("naslov", "")), x.get("kvadratura"))
        slika = TIPOVI.get(kljuc)
        if not slika:
            nepoklopljeno.append((x.get("id"), x.get("naslov"), x.get("kvadratura")))
            continue
        x["slika"] = f"slike/{slika}"
        x["galerija"] = [f"slike/{slika}"]
        promenjeno += 1
        print(f"[OK] {x['id']} ({x['naslov']}, {x.get('kvadratura')}m2): {slika}")

    sacuvaj_stanovi_js(STANOVI_JS, stanovi)
    print(f"\nUkupno azurirano: {promenjeno} stanova")
    if nepoklopljeno:
        print("Nepoklopljeno:", nepoklopljeno)


if __name__ == "__main__":
    main()
