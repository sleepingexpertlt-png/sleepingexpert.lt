<?php
/**
 * Automatinis blokavimas: HTML išvestyje <script>/<iframe>, atitinkantys žinomus sekiklius,
 * paverčiami neaktyviais (type="text/plain" / data-se-src), kol lankytojas neduoda sutikimo.
 * Naršyklėje juos vėl įjungia assets/consent.js.
 *
 * Tai daroma serveryje, o ne naršyklėje, nes tik taip sekiklis negali paleisti nė vienos
 * eilutės prieš sutikimą. Puslapių podėlis (cache) nepažeidžiamas: HTML vienodas visiems.
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('template_redirect', function () {
    if (!se_consent_settings()['auto_block'] || !se_consent_should_filter_request()) {
        return;
    }
    ob_start('se_consent_ob_callback');
}, 0);

function se_consent_should_filter_request() {
    if (is_admin() || wp_doing_ajax() || is_feed() || is_customize_preview()
        || (defined('REST_REQUEST') && REST_REQUEST)
        || (defined('XMLRPC_REQUEST') && XMLRPC_REQUEST)
        || isset($_GET['se_consent_off']) && current_user_can('manage_options')) {
        return false;
    }
    return (bool) apply_filters('se_consent_filter_request', true);
}

function se_consent_ob_callback($html) {
    foreach (headers_list() as $h) {
        if (stripos($h, 'content-type:') === 0 && stripos($h, 'text/html') === false) {
            return $html;
        }
    }
    if (stripos($html, '<html') === false) {
        return $html;
    }
    return se_consent_block_html($html, se_consent_rules());
}

/**
 * Gryna funkcija (be WP priklausomybių), kad būtų testuojama atskirai.
 *
 * @param string $html
 * @param array{src: array<string,string>, inline: array<string,string>} $rules
 */
function se_consent_block_html($html, array $rules) {
    $html = preg_replace_callback(
        '#<script\b([^>]*)>(.*?)</script>#is',
        function ($m) use ($rules) {
            return se_consent_block_script($m[0], $m[1], $m[2], $rules);
        },
        $html
    );
    return preg_replace_callback(
        '#<iframe\b([^>]*)>#i',
        function ($m) use ($rules) {
            return se_consent_block_iframe($m[0], $m[1], $rules);
        },
        $html
    );
}

function se_consent_attr($attrs, $name) {
    if (preg_match('#\s' . preg_quote($name, '#') . '\s*=\s*(["\'])(.*?)\1#is', $attrs, $m)) {
        return $m[2];
    }
    if (preg_match('#\s' . preg_quote($name, '#') . '\s*=\s*([^\s"\'>]+)#i', $attrs, $m)) {
        return $m[1];
    }
    return null;
}

function se_consent_match($haystack, array $patterns) {
    if ($haystack === '' || $haystack === null) {
        return null;
    }
    foreach ($patterns as $pattern => $category) {
        if (stripos($haystack, (string) $pattern) !== false) {
            return $category;
        }
    }
    return null;
}

function se_consent_block_script($full, $attrs, $body, array $rules) {
    if (preg_match('#\sdata-se-consent-ignore\b#i', $attrs) || preg_match('#\sid\s*=\s*["\']?se-consent#i', $attrs)) {
        return $full;
    }

    // Cookiebot žymėjimas paliekamas veikiantis: data-cookieconsent="marketing" => data-se-consent="marketing".
    $cb = se_consent_attr($attrs, 'data-cookieconsent');
    if ($cb !== null) {
        if (strtolower($cb) === 'ignore') {
            return $full;
        }
        $cats = array_values(array_intersect(array_map('trim', explode(',', strtolower($cb))), SE_CONSENT_CATEGORIES));
        if ($cats && se_consent_attr($attrs, 'data-se-consent') === null) {
            return se_consent_rewrite_script($full, $attrs, implode(',', $cats));
        }
        return $full;
    }
    if (se_consent_attr($attrs, 'data-se-consent') !== null) {
        return $full;
    }

    $type = strtolower((string) se_consent_attr($attrs, 'type'));
    if (!in_array($type, ['', 'text/javascript', 'application/javascript', 'module'], true)) {
        return $full; // JSON-LD, šablonai ir pan.
    }

    $src = se_consent_attr($attrs, 'src');
    $cat = $src !== null ? se_consent_match($src, $rules['src']) : se_consent_match($body, $rules['inline']);
    if ($cat === null || $cat === 'necessary') {
        return $full;
    }
    return se_consent_rewrite_script($full, $attrs, $cat);
}

function se_consent_rewrite_script($full, $attrs, $cat) {
    $type     = se_consent_attr($attrs, 'type');
    $newAttrs = preg_replace('#\stype\s*=\s*(["\'])[^"\']*\1|\stype\s*=\s*[^\s>]+#i', '', $attrs);
    $extra    = ' type="text/plain" data-se-consent="' . htmlspecialchars($cat, ENT_QUOTES) . '"';
    if ($type !== null && strtolower($type) !== 'text/plain') {
        $extra .= ' data-se-type="' . htmlspecialchars($type, ENT_QUOTES) . '"';
    }
    $pos = stripos($full, '>');
    // Atributų dalis pakeičiama tik atidarančioje žymoje; turinys nekeičiamas.
    return '<script' . $newAttrs . $extra . substr($full, $pos);
}

function se_consent_block_iframe($full, $attrs, array $rules) {
    if (preg_match('#\s(data-se-consent-ignore|data-se-src)\b#i', $attrs)) {
        return $full;
    }
    $cb  = se_consent_attr($attrs, 'data-cookieconsent');
    $src = se_consent_attr($attrs, 'src');
    if ($src === null) {
        return $full;
    }
    $cat = $cb !== null ? strtolower($cb) : se_consent_match($src, $rules['src']);
    if ($cat === null || $cat === 'ignore' || $cat === 'necessary') {
        return $full;
    }
    $newAttrs = preg_replace('#\ssrc\s*=#i', ' data-se-src=', $attrs, 1);
    return '<iframe' . $newAttrs . ' data-se-consent="' . htmlspecialchars($cat, ENT_QUOTES) . '">';
}
