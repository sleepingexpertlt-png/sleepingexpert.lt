# Swap runbook — saugus valymas ir perkėlimas

Skirta serveriui, kuriame veikia `frontier-agent`, `dashboard-api`, `letta` ir kt.
**Auksinė taisyklė: niekada `swapoff -a`.** Tik po vieną įrenginį.

---

## 0. Pirma atsakyk: ko trūksta — DISKO ar RAM?

Tai du skirtingi darbai su skirtingais sprendimais.

| Simptomas | Tikroji problema | Eik į |
|---|---|---|
| `df -h /` rodo mažai vietos, swapfile'ai valgo 6 GB šaknyje | **Diskas** | Scenarijus A |
| `free` rodo mažai laisvos, `vmstat` rodo nuolatinį `si/so`, servisai lėti | **RAM** | Scenarijus B |
| Swap užimtas, bet `si/so` = 0 ir PSI tylus | **Jokios problemos** | Nedaryk nieko |

Diagnostika (tik skaitymas, nieko nekeičia):

```bash
sudo bash scripts/swap-diagnose.sh
```

### Kaip skaityti rezultatą

- **Užimtas swap ≠ problema.** Anoniminiai puslapiai, išstumti prieš savaitę ir
  nuo tada nepaliesti, nekainuoja nieko. Svarbu tik srautas.
- **`/proc/pressure/memory`, eilutė `some avg60`:** < 1.00 = ramu; > 10.00 = thrashing.
- **`swap-out` per 10 s > 0 nuolat** = RAM tikrai trūksta, čia jau realus darbas.
- **zram triukas:** `swapon` rodo *nesuspaustą* dydį. 4 GB zram fiziškai RAM'e
  užima ~1,3–2 GB, ir tie baitai **jau įskaičiuoti** į `free` stulpelį `used`.
  Todėl `swapoff /dev/zram0` kainuoja tik skirtumą, ne visus 4 GB.
  Tikslus skaičius — 3 skripto skiltyje.

---

## Scenarijus A — reikia disko vietos (swapfile'ų perkėlimas)

Tikslas: `/swapfile2` (4 G) iš šaknies perkelti į kitą tomą, neprarandant swap
talpos ir nė sekundei nesumažinant bendros swap apimties.

**Esminis principas: PIRMA pridėk, TIK PASKUI atimk.** Kai aktyvus kitas swap
įrenginys, `swapoff` išstumtus puslapius gali perstumti į jį, o ne grūsti visus
į RAM. Be šito žingsnio rizikuoji būtent tuo OOM, kurio bijai.

```bash
# 1. Naujas swapfile ant kito tomo (pakeisk /mnt/data į savo)
sudo fallocate -l 4G /mnt/data/swapfile
# jei FS nepalaiko fallocate (btrfs/zfs) — naudok dd:
#   sudo dd if=/dev/zero of=/mnt/data/swapfile bs=1M count=4096 status=progress
sudo chmod 600 /mnt/data/swapfile
sudo mkswap /mnt/data/swapfile

# 2. Įjungiam ŽEMESNIU prioritetu nei zram
sudo swapon --priority 10 /mnt/data/swapfile
swapon --show          # dabar turi būti 3 diskiniai + zram

# 3. TIK DABAR išjungiam seną. Be -a! Vieną. Ir stebim.
sudo swapoff /swapfile2 &
watch -n2 'free -h; echo; swapon --show'
```

Jei `free` „available" krenta žemiau ~800 MB — **nutrauk** (`kill %1`) ir grįžk
prie B scenarijaus: pirma sumažink realų RAM poreikį.

```bash
# 4. Kai swapoff baigė — atlaisvinam diską
sudo rm /swapfile2

# 5. fstab: pašalink seną eilutę, pridėk naują (BE ŠITO neišgyvens reboot'o)
sudo cp /etc/fstab /etc/fstab.bak
sudo sed -i '\|^/swapfile2|d' /etc/fstab
echo '/mnt/data/swapfile none swap sw,pri=10 0 0' | sudo tee -a /etc/fstab

# 6. Patikrink, kad fstab nesulaužytas — kitaip serveris gali neužsikelti
sudo findmnt --verify --verbose
sudo swapon --show
```

> `/mnt/data` privalo būti sumontuotas **prieš** swap'ą. Jei tai atskiras tomas,
> patikrink montavimo tvarką arba naudok `x-systemd.requires=`.
> Swapfile'as **negali** būti ant NFS ar kito tinklinio FS.

---

## Scenarijus B — trūksta RAM (mažinam realų poreikį)

Tvarka nuo saugiausio prie rizikingiausio:

**B1. Nuvalyk page cache (nemokama, jokios rizikos servisams):**
```bash
sync && echo 1 | sudo tee /proc/sys/vm/drop_caches
```

**B2. Restartuok riebiausią servisą.** Kurį — pasako skripto 4 ir 5 skiltys.
Procesas, turintis daug `SWAP` bet mažai `RSS`, yra idealus kandidatas: jis
laiko šaltą balastą, o po restarto pradės nuo švaraus lapo.

```bash
sudo systemctl restart <servisas>     # po VIENĄ, tarp jų palauk 30 s
```

Prieš restartą patikrink, ar servisas turi būseną, kurią praras:
```bash
systemctl cat <servisas> | grep -E 'ExecStop|KillSignal|TimeoutStop'
```

**B3. Uždėk ribas, kad nesikartotų:**
```bash
sudo systemctl edit <servisas>
# [Service]
# MemoryHigh=2G
# MemoryMax=3G
```
`MemoryHigh` stabdo ir spaudžia procesą švelniai; `MemoryMax` žudo. Visada
nustatyk `MemoryHigh` žemiau už `MemoryMax`.

**B4. Sureguliuok swappiness.** Kai yra zram, aukštas swappiness yra *geras* —
suspaudimas RAM'e pigesnis už disko I/O:
```bash
echo 'vm.swappiness=100' | sudo tee /etc/sysctl.d/99-swap.conf
sudo sysctl --system
```
Be zram, tik su diskiniu swap — atvirkščiai, `10`–`20`.

**B5. Prioritetai.** zram privalo turėti **aukščiausią** prioritetą, kad
sistema pirma naudotų RAM suspaudimą ir tik paskui diską:
```bash
swapon --show      # PRIO stulpelis: zram turi būti didžiausias skaičius
```
Jei ne — tai jau savaime yra našumo bug'as, verta pataisyti.

---

## Ko NEDARYTI

- ❌ `swapoff -a`, kai suma swap'e > MemAvailable — garantuotas OOM arba valandų kibimas.
- ❌ Ištrinti swapfile'ą jo neišjungus (`rm` prieš `swapoff`) — kernel toliau rašo
  į nebeegzistuojančius blokus, sistema griūva.
- ❌ Redaguoti `/etc/fstab` be `findmnt --verify` — serveris gali neužsikelti,
  o tau reikės konsolės per hosterio panelę.
- ❌ Daryti tai sesijos pabaigoje, be laiko stebėti. `swapoff` 4 GB nuo lėto
  disko gali užtrukti 10–30 min.

## Rollback

```bash
sudo swapoff /mnt/data/swapfile          # jei naujas kelia problemų
sudo cp /etc/fstab.bak /etc/fstab        # grąžinam seną fstab
sudo findmnt --verify
```
Jei ištrynei seną swapfile'ą, atkurti paprasta:
`fallocate` → `chmod 600` → `mkswap` → `swapon`.
