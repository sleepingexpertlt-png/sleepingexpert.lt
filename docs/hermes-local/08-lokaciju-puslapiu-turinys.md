# Lokacijų puslapiai — PARUOŠTAS TURINYS (prioritetas #1, 2026-08-27)

Pagrindas: po AI-referrer fix'o (349cf5e6) paaiškėjo, kad **3 lokacijų puslapiai
traukia 32 % viso AI srauto** — 13,3 sesijos/puslapį, 5× daugiau nei produktų
puslapiai (2,5). Ir jie veda tiesiai į pagrindinį tikslą — maršrutus.

Iki šiol nebuvo optimizuoti nė karto.

## Ką duomenys sako apie žmogų, kuris čia ateina

AI jį atsiuntė su klausimu apie konkretų saloną arba „kur išbandyti čiužinį".
Vadinasi puslapis privalo per 3 sekundes atsakyti: **ką čia rasiu, kada atidaryta,
kaip nuvažiuoti.** Jei to nėra virš lankstymo linijos — maršrutas neįvyksta.

## Privaloma struktūra (visoms 3 lokacijoms)

1. **H1:** „Sleeping Expert [Miestas] — čiužinių salonas, [gatvė]"
2. **Maršruto mygtukas VIRŠ lankstymo linijos** — ne poraštėje. Tai vienintelis
   elementas, kuris tiesiogiai matuojamas mūsų KPI.
3. **Trumpai blokas** (30–55 ž.) — žr. tekstus žemiau
4. **Praktinė informacija** lentele: adresas · darbo laikas · telefonas · aukštas/
   orientyras · parkavimas → **VPS ima iš GBP per gmb_agent.py, ne iš owner**
5. **„Ką galiu išbandyti vietoje"** — skiriamasis blokas, žr. žemiau
6. **DUK** (5 kl., FAQPage JSON-LD)
7. **LocalBusiness JSON-LD** su NAP, geo, openingHours, sameAs → GBP profilis
8. Nuoroda į GBP profilį („Žiūrėti atsiliepimus Google")

---

## VILNIUS — Kalvarijų g. 125, PC Baldų Rojus

**Trumpai (48 ž.):**
Sleeping Expert salonas Vilniuje veikia prekybos centre „Baldų Rojus",
Kalvarijų g. 125. Čia galima atsigulti ir išbandyti čiužinius prieš perkant —
skirtingus kietumus, spyruoklių tipus ir pagalvių aukščius. Konsultantas padeda
parinkti pagal svorį ir miego pozą, ne pagal kainą.

**DUK:**

1. **Ar galiu išbandyti čiužinį Vilniaus salone?**
   Taip, čiužiniai išstatyti taip, kad ant jų būtų galima atsigulti. Rekomenduojame
   pagulėti bent 10 minučių ta poza, kuria miegate — trumpesnis bandymas mažai ką
   pasako.

2. **Kaip nuvažiuoti ir kur palikti automobilį?**
   Salonas yra PC „Baldų Rojus", Kalvarijų g. 125. `[VPS: parkavimo info iš GBP,
   jei yra; jei nėra — praleisti, neišgalvoti]`

3. **Kokios prekės yra salone, o kokias reikia užsakyti?**
   Salone stovi populiariausi modeliai išbandymui; visą asortimentą galima
   užsakyti vietoje. Hibridiniai čiužiniai sudaro apie 55 % mūsų pardavimų, todėl
   jų pasirinkimas salone didžiausias.

4. **Ar konsultantas padeda parinkti kietumą?**
   Taip — parinkimas remiasi svoriu ir miego poza. Šonu miegantiems paprastai
   tinka minkštesnis (H2–H3), ant nugaros ar pilvo — kietesnis (H3–H4).

5. **Kokia garantija taikoma?**
   Priklauso nuo technologijos: hibridiniams iki 20 metų, latekso iki 15,
   memory foam iki 10. Tikslios sąlygos — salone.

---

## KLAIPĖDA — Taikos pr. 56, PC HELIOS

**Trumpai (46 ž.):**
Sleeping Expert salonas Klaipėdoje veikia PC HELIOS, Taikos pr. 56. Čiužinius
galima išbandyti vietoje — atsigulti, palyginti kietumus ir pagalvių aukščius.
Konsultantas parenka pagal svorį ir miego pozą. Neradus tinkamo salone, visas
asortimentas užsakomas vietoje.

**DUK:** tie patys 5 klausimai, adresas ir orientyras pakeisti į Klaipėdos.

---

## UKMERGĖ — Kauno g. 9

**Trumpai (44 ž.):**
Sleeping Expert salonas Ukmergėje, Kauno g. 9, dirba nuo 2026 m. gegužės.
Čiužinius ir pagalves galima išbandyti vietoje prieš perkant. Konsultantas
padeda parinkti kietumą pagal svorį ir miego pozą, o viso asortimento prekes
galima užsakyti tiesiai salone.

**DUK:** tie patys 5 klausimai + vienas vietinis: **„Ar pristatote į Ukmergės
rajoną?"** `[OWNER FAKTAS]`

---

## Ko NEDARYTI

- Nekopijuoti to paties teksto į visus tris puslapius (near-duplicate = T3
  scaled-content signalas). Trumpai blokai jau parašyti skirtingi — išlaikyti.
- Nerašyti parkavimo, darbo laiko ar telefono iš galvos. Imti iš GBP arba palikti.
- Draudžiami žodžiai: premium, exclusive, Italijos dizaineriai, geriausi pasaulyje.
- Neteigti, kad konkretus modelis „yra sandėlyje" — atsargos kinta.

## Patikra prieš įkėlimą

- [ ] Maršruto mygtukas matomas be scroll'o mobiliajame
- [ ] LocalBusiness JSON-LD apvyniotas `<script type="application/ld+json">`
- [ ] FAQPage JSON-LD atskiras, validus
- [ ] Darbo laikas/telefonas sutampa su GBP (ne kopija iš seno teksto)
- [ ] Trys puslapiai NĖRA identiški
- [ ] `[OWNER FAKTAS]` / `[VPS: …]` žymos arba užpildytos, arba pašalintos
- [ ] Draft, ne publish

## Matavimas (kaip sužinosim, ar suveikė)

Bazė 2026-08-27: Klaipėda 13, Ukmergė 13, Vilnius 6 maršrutai / 7 d.
AI srautas į lokacijas: 40 sesijų / 28 d. iš 3 puslapių.
Po pakeitimo sekti abu skaičius savaitinėje patikroje. Vilnius — pagrindinis
taikinys: didžiausios impresijos (329), mažiausi maršrutai.
