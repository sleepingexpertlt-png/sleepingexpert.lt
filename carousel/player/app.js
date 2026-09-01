/* Sleeping Expert — karuseles logika.
   Veikia be interneto: duomenys is data/products.json, nuotraukos is data/images/.
   URL parametrai: ?interval=8 &only_sale=1 &orientation=portrait|landscape &nochrome=1 */
(function () {
  "use strict";

  var DISPLAY_DEFAULTS = {
    slide_seconds: 9,
    sale_slide_seconds: 12,
    sale_ratio: 0.5,
    sale_first: true,
    shuffle: true,
    show_qr: true,
    show_description: true,
    always_price_from: false,
    price_from_text: "nuo",
    show_stores: true,
    show_clock: true,
    summary_every: 8,
    transition_ms: 700,
    refresh_minutes: 15,
    reload_hours: 12,
    orientation: "auto",
    headline: "SLEEPING EXPERT",
    sale_badge_text: "AKCIJA",
    qr_caption: "Nuskenuok ir pamatyk",
    cta_text: "Klauskite konsultanto salone",
    sale_note: "",
    footer_text: "sleepingexpert.lt",
    stores: [],
    theme: {}
  };

  var CACHE_KEY = "se_carousel_payload_v1";
  var qs = new URLSearchParams(location.search);

  var state = {
    display: DISPLAY_DEFAULTS,
    payload: null,
    playlist: [],
    index: -1,
    layer: 0,
    paused: false,
    onlySale: qs.get("only_sale") === "1",
    timer: null,
    lastAdvance: Date.now(),
    pendingPayload: null,
    startedAt: Date.now()
  };

  var el = {
    stage: document.getElementById("stage"),
    slides: [document.getElementById("slide-a"), document.getElementById("slide-b")],
    headline: document.getElementById("headline"),
    clock: document.getElementById("clock"),
    stores: document.getElementById("stores"),
    footnote: document.getElementById("footnote"),
    progress: document.getElementById("progress"),
    toast: document.getElementById("toast"),
    boot: document.getElementById("boot"),
    bootMsg: document.getElementById("bootMsg"),
    help: document.getElementById("help")
  };

  /* ------------------------- pagalbines ------------------------- */
  function esc(text) {
    return String(text == null ? "" : text)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  var eurFormatter = null;
  try {
    eurFormatter = new Intl.NumberFormat("lt-LT", { style: "currency", currency: "EUR" });
  } catch (err) { eurFormatter = null; }

  function money(value) {
    if (typeof value !== "number" || !isFinite(value)) return "";
    if (eurFormatter) return eurFormatter.format(value);
    return value.toFixed(2).replace(".", ",") + " €";
  }

  function imgSrc(product) {
    var path = product.image || product.image_remote || "";
    if (/^(https?:|data:|blob:|\/)/i.test(path) || path.indexOf("data/") === 0) return path;
    return "data/" + path;
  }

  function shuffle(list) {
    for (var i = list.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    return list;
  }

  function toast(message, ms) {
    el.toast.textContent = message;
    el.toast.hidden = false;
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { el.toast.hidden = true; }, ms || 1800);
  }

  function fetchJson(path) {
    // vieno failo (offline) versijoje duomenys jau iterpti i puslapi
    if (window.__SE_DATA__) {
      var key = path.indexOf("display") !== -1 ? "display" : "products";
      var embedded = window.__SE_DATA__[key];
      return embedded ? Promise.resolve(embedded) : Promise.reject(new Error("nera iterptu duomenu"));
    }
    return fetch(path + "?t=" + Date.now(), { cache: "no-store" }).then(function (resp) {
      if (!resp.ok) throw new Error(path + " -> HTTP " + resp.status);
      return resp.json();
    });
  }

  /* ------------------------- duomenys ------------------------- */
  function loadDisplay() {
    return fetchJson("data/display.json").catch(function () { return {}; }).then(function (raw) {
      var display = Object.assign({}, DISPLAY_DEFAULTS, raw || {});
      if (qs.get("interval")) display.slide_seconds = display.sale_slide_seconds = parseFloat(qs.get("interval"));
      if (qs.get("orientation")) display.orientation = qs.get("orientation");
      if (qs.get("nochrome") === "1") { display.show_stores = false; display.show_clock = false; }
      state.display = display;
      applyChrome();
    });
  }

  function loadProducts(silent) {
    return fetchJson("data/products.json").then(function (payload) {
      if (!payload || !payload.products || !payload.products.length) throw new Error("tuscias produktu sarasas");
      try { localStorage.setItem(CACHE_KEY, JSON.stringify(payload)); } catch (err) { /* pilna atmintis — nesvarbu */ }
      return payload;
    }).catch(function (err) {
      if (silent) throw err;
      var cached = null;
      try { cached = JSON.parse(localStorage.getItem(CACHE_KEY) || "null"); } catch (e) { cached = null; }
      if (cached && cached.products && cached.products.length) {
        toast("Naudojami išsaugoti duomenys (nėra ryšio)", 4000);
        return cached;
      }
      throw err;
    });
  }

  /* ------------------------- grojarasctis ------------------------- */
  function buildPlaylist(payload) {
    var display = state.display;
    var all = (payload.products || []).slice();
    if (state.onlySale) all = all.filter(function (p) { return p.on_sale; });
    if (!all.length) all = (payload.products || []).slice();

    var sale = all.filter(function (p) { return p.on_sale; });
    var rest = all.filter(function (p) { return !p.on_sale; });

    if (display.shuffle) { shuffle(sale); shuffle(rest); }
    if (display.sale_first) {
      sale.sort(function (a, b) { return (b.discount_percent || 0) - (a.discount_percent || 0); });
    }

    var ratio = Math.max(0, Math.min(0.95, Number(display.sale_ratio) || 0));
    var wanted = sale.length;
    if (sale.length && ratio > 0 && rest.length) {
      wanted = Math.min(Math.round((rest.length * ratio) / (1 - ratio)), sale.length * 3);
      wanted = Math.max(wanted, sale.length);
    }
    var saleQueue = [];
    for (var i = 0; i < wanted && sale.length; i++) saleQueue.push(sale[i % sale.length]);

    var out = [], si = 0, ri = 0;
    while (si < saleQueue.length || ri < rest.length) {
      var takeSale = (ri >= rest.length) ||
        (si < saleQueue.length && si < (out.length + 1) * ratio);
      out.push({ type: "product", product: takeSale ? saleQueue[si++] : rest[ri++] });
    }

    var every = parseInt(display.summary_every, 10) || 0;
    if (every > 0 && sale.length >= 3) {
      var top = sale.slice().sort(function (a, b) {
        return (b.discount_percent || 0) - (a.discount_percent || 0);
      }).slice(0, 6);
      var withSummary = [];
      for (var k = 0; k < out.length; k++) {
        withSummary.push(out[k]);
        if ((k + 1) % every === 0) withSummary.push({ type: "summary", items: top, payload: payload });
      }
      out = withSummary;
    }
    return out;
  }

  /* ------------------------- atvaizdavimas ------------------------- */
  function renderProduct(product) {
    var display = state.display;
    var discounted = product.on_sale && product.discount_percent > 0;
    var showFrom = product.price_from || display.always_price_from === true;
    var category = (product.categories && product.categories[0]) || "Sleeping Expert";

    var badge = discounted
      ? '<div class="badge"><span class="badge__label">' + esc(display.sale_badge_text) +
        '</span><span class="badge__value">-' + product.discount_percent + '%</span></div>'
      : "";

    var oldPrice = discounted
      ? '<span class="price__old">' + esc(money(product.regular_price)) + "</span>" +
        (product.save_amount > 0
          ? '<span class="price__save">Sutaupote ' + esc(money(product.save_amount)) + "</span>"
          : "")
      : "";

    var qr = "";
    if (display.show_qr && product.url && window.QR) {
      try {
        qr = '<div class="qr"><div class="qr__box">' +
          QR.toSvg(product.url, { dark: "#142b6f", light: "#ffffff", quiet: 1 }) +
          '</div><div class="qr__caption">' + esc(display.qr_caption) + "</div></div>";
      } catch (err) { qr = ""; }
    }

    var cta = display.cta_text
      ? '<div class="cta' + (discounted ? "" : " cta--ghost") + '">' + esc(display.cta_text) + "</div>"
      : "";
    var note = (discounted && display.sale_note)
      ? '<div class="info__note">' + esc(display.sale_note) + "</div>" : "";

    var meta = [];
    if (product.sku) meta.push("Kodas: <b>" + esc(product.sku) + "</b>");
    meta.push(product.in_stock ? "<b>Yra sandėlyje</b>" : "Užsakoma");

    return '<div class="photo">' + badge +
        '<img src="' + esc(imgSrc(product)) + '" alt="' + esc(product.name) + '" loading="eager">' +
      "</div>" +
      '<div class="info">' +
        '<div class="info__main">' +
          '<div class="info__category">' + esc(category) + "</div>" +
          '<h1 class="info__name">' + esc(product.name) + "</h1>" +
          (display.show_description !== false && product.short
            ? '<p class="info__short">' + esc(product.short) + "</p>" : "") +
          '<div class="price">' +
            (showFrom ? '<span class="price__prefix">' + esc(display.price_from_text || "nuo") + "</span>" : "") +
            '<span class="price__now">' + esc(money(product.price)) + "</span>" +
            oldPrice +
          "</div>" + note + cta +
        "</div>" +
        '<div class="info__foot"><div class="info__meta">' + meta.join("<br>") + "</div>" + qr + "</div>" +
      "</div>";
  }

  function renderSummary(entry) {
    var counts = (entry.payload && entry.payload.counts) || {};
    var fromLabel = state.display.always_price_from === true
      ? (state.display.price_from_text || "nuo") : "";
    var cards = entry.items.map(function (product) {
      return '<div class="card">' +
        '<img class="card__img" src="' + esc(imgSrc(product)) + '" alt="">' +
        '<div class="card__body"><div class="card__name">' + esc(product.name) + "</div>" +
        '<div class="card__price">' +
        (fromLabel ? '<span class="card__from">' + esc(fromLabel) + "</span> " : "") +
        esc(money(product.price)) +
        '<span class="card__old">' + esc(money(product.regular_price)) + "</span></div></div>" +
        '<div class="card__cut">-' + (product.discount_percent || 0) + "%</div></div>";
    }).join("");

    return '<div class="summary__inner"><div class="summary__kicker">Šiuo metu</div>' +
      '<h1 class="summary__title">Akcijos — iki <em>-' + (counts.max_discount || 0) + "%</em></h1>" +
      '<div class="summary__grid">' + cards + "</div></div>";
  }

  function durationFor(entry) {
    var display = state.display;
    if (entry.type === "summary") return (Number(display.sale_slide_seconds) || 12) * 1000;
    var isSale = entry.product.on_sale;
    var seconds = isSale ? display.sale_slide_seconds : display.slide_seconds;
    return (Number(seconds) || 9) * 1000;
  }

  function preload(entry) {
    if (!entry) return;
    var list = entry.type === "summary" ? entry.items : [entry.product];
    list.forEach(function (product) { (new Image()).src = imgSrc(product); });
  }

  function runProgress(ms) {
    var bar = el.progress;
    bar.style.transition = "none";
    bar.style.width = "0%";
    void bar.offsetWidth;
    bar.style.transition = "width " + ms + "ms linear";
    bar.style.width = "100%";
  }

  function freezeProgress() {
    var width = getComputedStyle(el.progress).width;
    el.progress.style.transition = "none";
    el.progress.style.width = width;
  }

  function show(index) {
    if (!state.playlist.length) return;
    state.index = ((index % state.playlist.length) + state.playlist.length) % state.playlist.length;
    var entry = state.playlist[state.index];
    var ms = durationFor(entry);

    var next = el.slides[state.layer ^ 1];
    var current = el.slides[state.layer];
    next.className = "slide slide--" + (entry.type === "summary" ? "summary" : "product");
    next.style.setProperty("--kb", (ms + 800) + "ms");
    next.innerHTML = entry.type === "summary" ? renderSummary(entry) : renderProduct(entry.product);
    next.setAttribute("aria-hidden", "false");

    void next.offsetWidth;
    next.classList.add("is-active");
    current.classList.remove("is-active");
    current.setAttribute("aria-hidden", "true");
    state.layer ^= 1;

    document.body.classList.remove("is-booting", "is-error");
    state.lastAdvance = Date.now();
    preload(state.playlist[(state.index + 1) % state.playlist.length]);

    runProgress(ms);
    clearTimeout(state.timer);
    if (!state.paused) state.timer = setTimeout(advance, ms);
  }

  function advance() {
    if (state.pendingPayload && state.index >= state.playlist.length - 1) applyPayload(state.pendingPayload, true);
    show(state.index + 1);
  }

  function applyPayload(payload, quiet) {
    state.payload = payload;
    state.pendingPayload = null;
    state.playlist = buildPlaylist(payload);
    if (!quiet) state.index = -1;
    if (!state.playlist.length) {
      showError("Nerasta prekių pagal nustatytus filtrus.");
      return false;
    }
    return true;
  }

  function showError(message) {
    document.body.classList.add("is-error");
    el.bootMsg.textContent = message;
  }

  /* ------------------------- rėmelis ------------------------- */
  var THEME_VARS = {
    brand: "--brand",
    brand_deep: "--brand-deep",
    brand_soft: "--brand-soft",
    accent: "--accent",
    sale: "--sale",
    ink: "--ink",
    font: "--font",
    font_display: "--font-display"
  };

  function applyTheme(theme) {
    if (!theme) return;
    var root = document.documentElement;
    Object.keys(THEME_VARS).forEach(function (key) {
      if (theme[key]) root.style.setProperty(THEME_VARS[key], theme[key]);
    });
  }

  function applyChrome() {
    var display = state.display;
    applyTheme(display.theme);
    el.headline.textContent = display.headline || "";
    document.body.classList.toggle("force-portrait", display.orientation === "portrait");
    document.body.classList.toggle("force-landscape", display.orientation === "landscape");

    el.footnote.textContent = display.footer_text || "";
    if (display.show_stores && display.stores && display.stores.length) {
      el.stores.innerHTML = display.stores.map(function (store) {
        return '<div class="store"><b>' + esc(store.city) + "</b><span>" + esc(store.address) + "</span></div>";
      }).join("");
    } else {
      el.stores.innerHTML = "";
    }

    el.clock.hidden = !display.show_clock;
    if (display.show_clock) tickClock();
  }

  function tickClock() {
    var now = new Date();
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };
    el.clock.textContent = pad(now.getHours()) + ":" + pad(now.getMinutes());
  }

  /* ------------------------- valdymas ------------------------- */
  function togglePause() {
    state.paused = !state.paused;
    if (state.paused) {
      clearTimeout(state.timer);
      freezeProgress();
      toast("Pauzė");
    } else {
      toast("Tęsiama");
      show(state.index + 1);
    }
  }

  function bindKeys() {
    document.addEventListener("keydown", function (event) {
      switch (event.key) {
        case " ": event.preventDefault(); togglePause(); break;
        case "ArrowRight": clearTimeout(state.timer); show(state.index + 1); break;
        case "ArrowLeft": clearTimeout(state.timer); show(state.index - 1); break;
        case "f": case "F":
          if (document.fullscreenElement) document.exitFullscreen();
          else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
          break;
        case "r": case "R": refresh(true); break;
        case "s": case "S":
          state.onlySale = !state.onlySale;
          toast(state.onlySale ? "Rodomos tik akcijos" : "Rodomos visos prekės");
          if (state.payload && applyPayload(state.payload)) show(0);
          break;
        case "h": case "H": el.help.hidden = !el.help.hidden; break;
        default: break;
      }
    });
  }

  function refresh(manual) {
    loadProducts(true).then(function (payload) {
      var same = state.payload &&
        state.payload.generated_at === payload.generated_at &&
        state.payload.products.length === payload.products.length;
      if (same && !manual) return;
      if (manual) {
        if (applyPayload(payload)) { clearTimeout(state.timer); show(0); }
        toast("Duomenys atnaujinti (" + payload.products.length + " prekės)");
      } else {
        state.pendingPayload = payload;  // pakeisime svelniai, pasibaigus ciklui
      }
    }).catch(function (err) {
      if (manual) toast("Nepavyko atnaujinti: " + err.message, 3500);
    });
  }

  function startWatchdogs() {
    setInterval(tickClock, 20000);

    var refreshMs = Math.max(1, Number(state.display.refresh_minutes) || 15) * 60000;
    setInterval(function () { refresh(false); }, refreshMs);

    // jei skaidre "uzstrigo" (naršyklės triktis) — atstatome
    setInterval(function () {
      if (state.paused || !state.playlist.length) return;
      var stuckFor = Date.now() - state.lastAdvance;
      if (stuckFor > durationFor(state.playlist[state.index] || {}) * 3 + 15000) {
        show(state.index + 1);
      }
    }, 20000);

    // profilaktinis perkrovimas kiosko rezimui (atminties nutekejimams isvengti)
    var reloadHours = Number(state.display.reload_hours) || 0;
    if (reloadHours > 0) {
      setInterval(function () {
        if (Date.now() - state.startedAt > reloadHours * 3600000) location.reload();
      }, 600000);
    }

    document.addEventListener("visibilitychange", function () {
      if (!document.hidden && !state.paused && state.playlist.length) show(state.index + 1);
    });
  }

  /* ------------------------- startas ------------------------- */
  function boot() {
    document.documentElement.style.setProperty("--transition", (state.display.transition_ms || 700) + "ms");
    loadDisplay().then(function () {
      document.documentElement.style.setProperty("--transition", (state.display.transition_ms || 700) + "ms");
      return loadProducts(false);
    }).then(function (payload) {
      if (applyPayload(payload)) show(0);
      bindKeys();
      startWatchdogs();
    }).catch(function (err) {
      showError("Nepavyko įkelti duomenų: " + err.message);
      setTimeout(function () { location.reload(); }, 30000);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
