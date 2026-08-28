#!/usr/bin/env bash
# Paleidzia Chromium pilno ekrano (kiosko) rezimu ir isjungia ekrano uzmigima.
# Naudojimas:  ./kiosk/start-kiosk.sh [URL]
# Numatytas URL: http://localhost:8080/
set -euo pipefail

URL="${1:-http://localhost:8080/}"
PROFILE="${HOME}/.config/se-carousel-kiosk"

# 1) ekranas neuzmiega ir nerodo pelės žymeklio
if command -v xset >/dev/null 2>&1; then
  xset s off || true
  xset s noblank || true
  xset -dpms || true
fi
command -v unclutter >/dev/null 2>&1 && (unclutter -idle 1 -root &) || true

# 2) laukiame, kol serveris atsakys (iki 60 s)
if command -v curl >/dev/null 2>&1 && [[ "$URL" == http* ]]; then
  for _ in $(seq 1 60); do
    curl -sf -o /dev/null "$URL" && break
    sleep 1
  done
else
  sleep 5   # nera curl arba atidaromas failas — trumpa pauze ir pirmyn
fi

# 3) issivalome "Chromium netvarkingai issijunge" pranesima
if [ -f "${PROFILE}/Default/Preferences" ]; then
  sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/; s/"exited_cleanly":false/"exited_cleanly":true/' \
    "${PROFILE}/Default/Preferences" || true
fi

# 4) surandame Chromium
BROWSER=""
for candidate in chromium-browser chromium google-chrome-stable google-chrome; do
  if command -v "$candidate" >/dev/null 2>&1; then BROWSER="$candidate"; break; fi
done
if [ -z "$BROWSER" ]; then
  echo "Nerasta Chromium/Chrome. Idiek:  sudo apt install -y chromium-browser" >&2
  exit 1
fi

exec "$BROWSER" \
  --kiosk \
  --start-fullscreen \
  --user-data-dir="$PROFILE" \
  --noerrdialogs \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --disable-features=TranslateUI \
  --disable-pinch \
  --overscroll-history-navigation=0 \
  --check-for-update-interval=31536000 \
  --autoplay-policy=no-user-gesture-required \
  --password-store=basic \
  "$URL"
