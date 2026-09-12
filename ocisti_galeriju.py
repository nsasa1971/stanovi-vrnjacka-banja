"""
ocisti_galeriju.py
--------------------
WordPress izvoz je za neke stanove u galeriju ubacio SVE slike pozicija na
spratu za CEO objekat (ne samo za taj stan) - npr. stan "Jezero I-02" je u
galeriji imao i slike pozicija za stanove 3, 24, 25, 26, 27, 28 itd, jer je
to bio deo opsteg "estate_gallery" polja u WordPress-u.

Ova skripta za svaki stan izvlaci njegov SOPSTVENI broj sa kraja naslova
(npr. "Jezero I-02" -> 2, "Porta 2 Stan 06" -> 6), i iz galerije zadrzava
SAMO slike ciji naziv fajla sadrzi taj broj kao celu cifru (ne kao deo neke
druge cifre) - npr. "1_2.png" ostaje, "1_23.png" ili "1_61218.png" se
uklanjaju jer se odnose na druge stanove.

Ako bi filtriranje ostavilo praznu galeriju (znaci nijedna slika se ne
poklapa sa brojem stana - moze se desiti kod kombinovanih naziva), stan
ostaje NEDIRNUT (zadrzava celu staru galeriju) da se ne bi slucajno obrisalo
nesto validno.

Pokrenuti iz foldera sajta:

    python ocisti_galeriju.py
"""

import os
import re
import json

STANOVI_JS = "stanovi.js"


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


def broj_stana(naslov):
    """Izvlaci broj sa kraja naslova, npr. 'Jezero I-02' -> 2."""
    m = re.search(r"(\d+)\s*$", naslov or "")
    return int(m.group(1)) if m else None


def tokeni_iz_imena(url):
    """Sve cele cifre iz naziva fajla (bez ekstenzije), npr.
    '1_61218.png' -> ['1', '61218'], 'Stan-2-bjekat-1.jpg' -> ['2', '1']."""
    ime = os.path.splitext(os.path.basename(url.split("?")[0]))[0]
    return re.findall(r"\d+", ime)


def main():
    stanovi = ucitaj_stanovi_js(STANOVI_JS)

    promenjeno = 0
    for x in stanovi:
        broj = broj_stana(x.get("naslov", ""))
        galerija = x.get("galerija") or []
        if not galerija or broj is None:
            continue

        nova_galerija = [u for u in galerija if str(broj) in tokeni_iz_imena(u)]

        if not nova_galerija:
            continue  # ne diraj - filtriranje bi ostavilo prazno

        if len(nova_galerija) != len(galerija):
            print(f"[OK] Stan {x['id']} ({x['naslov']}): {len(galerija)} -> {len(nova_galerija)} slika u galeriji")
            x["galerija"] = nova_galerija
            promenjeno += 1

    sacuvaj_stanovi_js(STANOVI_JS, stanovi)
    print(f"\nUkupno izmenjeno stanova: {promenjeno}")
    print(f"Gotovo! {STANOVI_JS} je azuriran.")


if __name__ == "__main__":
    main()
