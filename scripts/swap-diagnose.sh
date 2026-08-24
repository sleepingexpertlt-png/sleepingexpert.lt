#!/usr/bin/env bash
# swap-diagnose.sh — TIK SKAITYMAS. Nieko nekeicia, nieko nerestartuoja.
# Naudojimas:  sudo bash scripts/swap-diagnose.sh
set -uo pipefail

hr() { printf '\n\033[1m== %s ==\033[0m\n' "$1"; }
kb2h() { awk -v k="${1:-0}" 'BEGIN{printf "%.1f GiB", k/1048576}'; }

hr "1. Bendra RAM / swap busena"
free -h
echo
swapon --show 2>/dev/null || cat /proc/swaps

hr "2. Ar sistema REALIAI plaka? (svarbiausia dalis)"
if [ -r /proc/pressure/memory ]; then
  echo "PSI /proc/pressure/memory:"; cat /proc/pressure/memory
  echo "  -> some avg60 < 1.00 = spaudimo nera. > 10.00 = rimtas thrashing."
else
  echo "PSI nepasiekiamas (senas kernel arba nera CONFIG_PSI)."
fi
echo
echo "Swap I/O per 10s (jei abu 0 -> swap yra saltas balastas, jokios zalos):"
r1=$(awk '/^pswpin/{i=$2} /^pswpout/{o=$2} END{print i" "o}' /proc/vmstat)
sleep 10
r2=$(awk '/^pswpin/{i=$2} /^pswpout/{o=$2} END{print i" "o}' /proc/vmstat)
awk -v a="$r1" -v b="$r2" 'BEGIN{
  split(a,x," "); split(b,y," ");
  printf "  swap-in : %d psl. (%.1f MiB/10s)\n", y[1]-x[1], (y[1]-x[1])*4/1024;
  printf "  swap-out: %d psl. (%.1f MiB/10s)\n", y[2]-x[2], (y[2]-x[2])*4/1024;
}'

hr "3. zram tikroji kaina RAM'e"
shopt -s nullglob
found=0
for z in /sys/block/zram*; do
  found=1; name=$(basename "$z")
  if [ -r "$z/mm_stat" ]; then
    read -r orig compr memused _rest < "$z/mm_stat"
    awk -v n="$name" -v o="$orig" -v c="$compr" -v m="$memused" 'BEGIN{
      printf "%s: nesuspausta %.2f GiB -> RAM uzima %.2f GiB (santykis %.2fx)\n", n, o/1073741824, m/1073741824, (m>0? o/m : 0);
      printf "  -> swapoff %s neto kainuotu ~%.2f GiB RAM (ne %.2f GiB!)\n", n, (o-m)/1073741824, o/1073741824;
    }'
  fi
done
[ "$found" = 0 ] && echo "zram irenginiu nera."

hr "4. TOP procesai pagal swap (kB)"
printf '%12s %12s %8s  %s\n' "SWAP" "RSS" "PID" "KOMANDA"
for p in /proc/[0-9]*; do
  [ -r "$p/smaps_rollup" ] || continue
  sw=$(awk '/^Swap:/{print $2; exit}' "$p/smaps_rollup" 2>/dev/null) || continue
  case "${sw:-0}" in ''|0) continue;; esac
  rss=$(awk '/^VmRSS:/{print $2}' "$p/status" 2>/dev/null)
  cmd=$(tr '\0' ' ' < "$p/cmdline" 2>/dev/null | cut -c1-64)
  [ -z "$cmd" ] && cmd="[$(awk '/^Name:/{print $2}' "$p/status" 2>/dev/null)]"
  printf '%12s %12s %8s  %s\n' "$sw" "${rss:-0}" "${p#/proc/}" "$cmd"
done | sort -rn | head -20
echo "  (kB. Pastaba: bendrinami puslapiai skaiciuojami kiekvienam procesui,"
echo "   todel suma gali virsyti realia swap apimti.)"

hr "5. TOP systemd servisai pagal atminti"
if command -v systemctl >/dev/null 2>&1; then
  systemctl list-units --type=service --state=running --no-legend --no-pager 2>/dev/null \
  | awk '{print $1}' | while read -r s; do
      m=$(systemctl show -p MemoryCurrent --value "$s" 2>/dev/null)
      case "$m" in ''|'[not set]'|18446744073709551615) continue;; esac
      printf '%14s  %s\n' "$m" "$s"
    done | sort -rn | head -15 | awk '{printf "%8.0f MiB  %s\n", $1/1048576, $2}'
else
  echo "systemctl nerastas."
fi

hr "6. Disko vieta ir swapfile'u dydziai"
df -h -x tmpfs -x devtmpfs 2>/dev/null
echo
awk 'NR>1 && $2=="file"{print $1}' /proc/swaps | while read -r f; do
  ls -lh "$f" 2>/dev/null | awk '{print "  swapfile: "$9"  dydis diske: "$5}'
  df -h "$f" 2>/dev/null | awk 'NR==2{print "     yra ant: "$1" ("$6"), laisva "$4}'
done

hr "7. VERDIKTAS: ka saugu isjungti DABAR"
avail=$(awk '/^MemAvailable:/{print $2}' /proc/meminfo)
echo "MemAvailable: $(kb2h "$avail")"
echo
tail -n +2 /proc/swaps | while read -r dev type size used prio; do
  cost=$used
  case "$dev" in */zram*)
    zn=$(basename "$dev")
    if [ -r "/sys/block/$zn/mm_stat" ]; then
      read -r o _c m _r < "/sys/block/$zn/mm_stat"
      cost=$(( (o - m) / 1024 ))
    fi ;;
  esac
  awk -v d="$dev" -v u="$used" -v c="$cost" -v a="$avail" -v p="$prio" 'BEGIN{
    need = c * 1.15 + 524288;   # +15% atsarga +512MiB rezervas
    printf "%-24s prio=%-4s uzimta %.2f GiB | RAM kaina %.2f GiB | reikia %.2f GiB -> %s\n",
      d, p, u/1048576, c/1048576, need/1048576,
      (a > need ? "SAUGU isjungti po viena" : "PAVOJINGA - OOM rizika");
  }'
done
echo
echo "SVARBU: niekada 'swapoff -a'. Tik po viena irengini, ir tik ta, kuris pazymetas SAUGU."
