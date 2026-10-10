<?php
/**
 * Administravimas: Nustatymai → SE Consent (nustatymai, žurnalas su statistika, CSV eksportas).
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('admin_menu', function () {
    add_options_page('SE Consent', 'SE Consent', 'manage_options', 'se-consent', 'se_consent_admin_page');
});

add_action('admin_post_se_consent_save', 'se_consent_admin_save');
add_action('admin_post_se_consent_export', 'se_consent_admin_export');

function se_consent_admin_save() {
    if (!current_user_can('manage_options')) {
        wp_die('Forbidden', 403);
    }
    check_admin_referer('se_consent_save');
    $in  = wp_unslash($_POST);
    $old = se_consent_settings();

    $new = $old;
    foreach (['gcm_enabled', 'gcm_ads_redaction', 'gcm_url_passthrough', 'auto_block', 'cookiebot_compat', 'floating_button'] as $k) {
        $new[$k] = empty($in[$k]) ? 0 : 1;
    }
    $new['gcm_mode']             = ($in['gcm_mode'] ?? '') === 'basic' ? 'basic' : 'advanced';
    $new['position']             = ($in['position'] ?? '') === 'center' ? 'center' : 'bottom';
    $new['expiry_days']          = max(1, min(395, (int) ($in['expiry_days'] ?? 365)));
    $new['log_retention_months'] = max(1, min(120, (int) ($in['log_retention_months'] ?? 24)));
    $new['ga_cookie_days']       = max(0, min(395, (int) ($in['ga_cookie_days'] ?? 395)));
    $new['cookie_domain']        = preg_replace('/[^a-z0-9.\-]/i', '', (string) ($in['cookie_domain'] ?? ''));
    $new['privacy_url']          = esc_url_raw((string) ($in['privacy_url'] ?? ''));
    $new['color_primary']        = sanitize_hex_color((string) ($in['color_primary'] ?? '')) ?: '#142b6f';
    $new['color_accent']         = sanitize_hex_color((string) ($in['color_accent'] ?? '')) ?: '#ffd602';
    $new['extra_rules']          = sanitize_textarea_field((string) ($in['extra_rules'] ?? ''));
    $new['cookies']              = sanitize_textarea_field((string) ($in['cookies'] ?? ''));

    foreach (array_keys(se_consent_default_texts()) as $lang) {
        foreach (['title', 'body', 'accept_all', 'reject_all', 'customize', 'save'] as $k) {
            if (isset($in['texts'][$lang][$k])) {
                $new['texts'][$lang][$k] = sanitize_textarea_field((string) $in['texts'][$lang][$k]);
            }
        }
    }
    if (!empty($in['bump_version'])) {
        $new['consent_version'] = (int) $old['consent_version'] + 1;
    }

    update_option(SE_CONSENT_OPTION, $new);
    wp_safe_redirect(admin_url('options-general.php?page=se-consent&saved=1'));
    exit;
}

function se_consent_admin_export() {
    if (!current_user_can('manage_options')) {
        wp_die('Forbidden', 403);
    }
    check_admin_referer('se_consent_export');
    global $wpdb;
    $table = se_consent_log_table();
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="se-consent-log-' . gmdate('Y-m-d') . '.csv"');
    $out = fopen('php://output', 'w');
    fputcsv($out, ['consent_id', 'created_at_utc', 'version', 'method', 'preferences', 'statistics', 'marketing', 'ip_masked', 'user_agent', 'url']);
    $last = 0;
    do { // dalimis, kad didelis žurnalas neišnaudotų atminties
        $rows = $wpdb->get_results($wpdb->prepare("SELECT * FROM {$table} WHERE id > %d ORDER BY id LIMIT 5000", $last), ARRAY_A); // phpcs:ignore
        foreach ($rows as $r) {
            $last = (int) $r['id'];
            unset($r['id']);
            fputcsv($out, $r);
        }
    } while (count($rows) === 5000);
    fclose($out);
    exit;
}

function se_consent_admin_page() {
    $s     = se_consent_settings();
    $tab   = sanitize_key($_GET['tab'] ?? 'settings');
    $base  = admin_url('options-general.php?page=se-consent');
    ?>
    <div class="wrap">
        <h1>SE Consent</h1>
        <?php if (!empty($_GET['saved'])) : ?>
            <div class="notice notice-success is-dismissible"><p>Išsaugota. Jei naudojate puslapių podėlį (cache), išvalykite jį.</p></div>
        <?php endif; ?>
        <nav class="nav-tab-wrapper">
            <a class="nav-tab <?php echo $tab === 'settings' ? 'nav-tab-active' : ''; ?>" href="<?php echo esc_url($base); ?>">Nustatymai</a>
            <a class="nav-tab <?php echo $tab === 'log' ? 'nav-tab-active' : ''; ?>" href="<?php echo esc_url($base . '&tab=log'); ?>">Sutikimų žurnalas</a>
        </nav>
        <?php $tab === 'log' ? se_consent_admin_log() : se_consent_admin_settings($s); ?>
    </div>
    <?php
}

function se_consent_admin_settings(array $s) {
    $cb = function ($k, $label) use ($s) {
        printf('<label><input type="checkbox" name="%1$s" value="1" %2$s> %3$s</label><br>', esc_attr($k), checked(!empty($s[$k]), true, false), esc_html($label));
    };
    ?>
    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
        <input type="hidden" name="action" value="se_consent_save">
        <?php wp_nonce_field('se_consent_save'); ?>
        <table class="form-table" role="presentation">
            <tr><th>Banerio versija</th><td>
                <strong><?php echo (int) $s['consent_version']; ?></strong>
                <label style="margin-left:12px"><input type="checkbox" name="bump_version" value="1"> Padidinti (visi lankytojai vėl pamatys banerį)</label>
                <p class="description">Didinkite, kai pridedate naują sekiklį ar keičiate slapukų paskirtį.</p>
            </td></tr>
            <tr><th>Google Consent Mode v2</th><td>
                <?php $cb('gcm_enabled', 'Įjungta'); ?>
                <select name="gcm_mode">
                    <option value="advanced" <?php selected($s['gcm_mode'], 'advanced'); ?>>Advanced — Google žymos veikia be slapukų iki sutikimo (konversijų modeliavimas)</option>
                    <option value="basic" <?php selected($s['gcm_mode'], 'basic'); ?>>Basic — Google žymos blokuojamos iki sutikimo</option>
                </select><br>
                <?php $cb('gcm_ads_redaction', 'ads_data_redaction (be sutikimo nesiųsti reklamos identifikatorių)'); ?>
                <?php $cb('gcm_url_passthrough', 'url_passthrough (gclid perdavimas per URL be slapukų)'); ?>
                Google slapukų (_ga, _gcl_au) galiojimas <input type="number" name="ga_cookie_days" value="<?php echo (int) $s['ga_cookie_days']; ?>" min="0" max="395" style="width:80px"> d.
                <span class="description">(Google numatytai — 2 metai; leidžiama ≤ 395 d. = 13 mėn.; 0 — nekeisti)</span>
            </td></tr>
            <tr><th>Blokavimas</th><td>
                <?php $cb('auto_block', 'Automatiškai blokuoti žinomus sekiklius iki sutikimo'); ?>
                <?php $cb('cookiebot_compat', 'Cookiebot suderinamumas (window.Cookiebot, data-cookieconsent, GTM cookie_consent_* įvykiai)'); ?>
                <p class="description">Papildomos taisyklės, po vieną eilutėje: <code>URL ar kodo fragmentas | statistics</code> (kategorijos: preferences, statistics, marketing).</p>
                <textarea name="extra_rules" rows="4" class="large-text code"><?php echo esc_textarea($s['extra_rules']); ?></textarea>
                <p class="description">Patikrinti puslapį be blokavimo (tik administratoriui): pridėkite <code>?se_consent_off=1</code>.</p>
            </td></tr>
            <tr><th>Slapukų sąrašas</th><td>
                <p class="description">Formatas: <code>pavadinimas | tiekėjas | kategorija | paskirtis | galiojimas</code>. <code>*</code> — bet kokie simboliai. Naudojamas deklaracijoje, banerio detalėse ir trinant slapukus atšaukus sutikimą. Naujus slapukus randa <code>tools/scan.mjs</code>.</p>
                <textarea name="cookies" rows="14" class="large-text code"><?php echo esc_textarea($s['cookies']); ?></textarea>
            </td></tr>
            <tr><th>Išvaizda</th><td>
                <select name="position">
                    <option value="bottom" <?php selected($s['position'], 'bottom'); ?>>Juosta apačioje</option>
                    <option value="center" <?php selected($s['position'], 'center'); ?>>Langas centre</option>
                </select>
                Pagrindinė <input type="text" name="color_primary" value="<?php echo esc_attr($s['color_primary']); ?>" size="8">
                Akcentas <input type="text" name="color_accent" value="<?php echo esc_attr($s['color_accent']); ?>" size="8"><br>
                <?php $cb('floating_button', 'Rodyti mygtuką sutikimui pakeisti (kairėje apačioje)'); ?>
            </td></tr>
            <tr><th>Galiojimas ir saugojimas</th><td>
                Sutikimas galioja <input type="number" name="expiry_days" value="<?php echo (int) $s['expiry_days']; ?>" min="1" max="395" style="width:80px"> d. &nbsp;
                Žurnalas saugomas <input type="number" name="log_retention_months" value="<?php echo (int) $s['log_retention_months']; ?>" min="1" max="120" style="width:70px"> mėn.<br>
                Slapuko domenas <input type="text" name="cookie_domain" value="<?php echo esc_attr($s['cookie_domain']); ?>" placeholder=".sleepingexpert.lt">
                <span class="description">(tuščia — tik šis domenas)</span><br>
                Privatumo politika <input type="text" name="privacy_url" value="<?php echo esc_attr($s['privacy_url']); ?>" class="regular-text">
            </td></tr>
            <?php foreach ($s['texts'] as $lang => $t) : ?>
                <tr><th>Tekstai (<?php echo esc_html(strtoupper($lang)); ?>)</th><td>
                    <?php foreach (['title' => 'Antraštė', 'accept_all' => 'Sutikti', 'reject_all' => 'Atmesti', 'customize' => 'Nustatymai', 'save' => 'Išsaugoti'] as $k => $label) : ?>
                        <label style="display:inline-block;min-width:90px"><?php echo esc_html($label); ?></label>
                        <input type="text" name="texts[<?php echo esc_attr($lang); ?>][<?php echo esc_attr($k); ?>]" value="<?php echo esc_attr($t[$k]); ?>" class="regular-text"><br>
                    <?php endforeach; ?>
                    <textarea name="texts[<?php echo esc_attr($lang); ?>][body]" rows="3" class="large-text"><?php echo esc_textarea($t['body']); ?></textarea>
                </td></tr>
            <?php endforeach; ?>
        </table>
        <p>Trumpieji kodai: <code>[se_cookie_declaration]</code> — slapukų deklaracija, <code>[se_consent_link]</code> — nuoroda nustatymams atidaryti.</p>
        <?php submit_button('Išsaugoti'); ?>
    </form>
    <?php
}

function se_consent_admin_log() {
    global $wpdb;
    $table = se_consent_log_table();
    $st    = se_consent_log_stats(30);
    $pct   = function ($n) use ($st) {
        return $st['total'] ? round($n * 100 / $st['total']) . '%' : '—';
    };
    $rows = $wpdb->get_results("SELECT * FROM {$table} ORDER BY id DESC LIMIT 100", ARRAY_A); // phpcs:ignore
    ?>
    <h2>Paskutinės 30 dienų</h2>
    <table class="widefat striped" style="max-width:720px">
        <tr><td>Sprendimų iš viso</td><td><strong><?php echo (int) $st['total']; ?></strong></td></tr>
        <tr><td>Sutiko su visais</td><td><?php echo (int) $st['accept_all'] . ' (' . esc_html($pct($st['accept_all'])) . ')'; ?></td></tr>
        <tr><td>Tik būtinieji</td><td><?php echo (int) $st['reject_all'] . ' (' . esc_html($pct($st['reject_all'])) . ')'; ?></td></tr>
        <tr><td>Pasirinko patys</td><td><?php echo (int) $st['custom'] . ' (' . esc_html($pct($st['custom'])) . ')'; ?></td></tr>
        <tr><td>Leido statistiką</td><td><?php echo esc_html($pct($st['statistics'])); ?></td></tr>
        <tr><td>Leido rinkodarą</td><td><?php echo esc_html($pct($st['marketing'])); ?></td></tr>
    </table>
    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="margin:16px 0">
        <input type="hidden" name="action" value="se_consent_export">
        <?php wp_nonce_field('se_consent_export'); ?>
        <?php submit_button('Eksportuoti visą žurnalą (CSV)', 'secondary', 'submit', false); ?>
    </form>
    <h2>Paskutiniai 100 įrašų</h2>
    <table class="widefat striped">
        <thead><tr><th>Laikas (UTC)</th><th>Sutikimo ID</th><th>Būdas</th><th>Nuost.</th><th>Stat.</th><th>Rink.</th><th>Versija</th><th>IP</th><th>Puslapis</th></tr></thead>
        <tbody>
        <?php foreach ($rows as $r) : ?>
            <tr>
                <td><?php echo esc_html($r['created_at']); ?></td>
                <td><code><?php echo esc_html($r['consent_id']); ?></code></td>
                <td><?php echo esc_html($r['method']); ?></td>
                <td><?php echo $r['preferences'] ? '✓' : '—'; ?></td>
                <td><?php echo $r['statistics'] ? '✓' : '—'; ?></td>
                <td><?php echo $r['marketing'] ? '✓' : '—'; ?></td>
                <td><?php echo (int) $r['version']; ?></td>
                <td><?php echo esc_html($r['ip_masked']); ?></td>
                <td><?php echo esc_html($r['url']); ?></td>
            </tr>
        <?php endforeach; ?>
        </tbody>
    </table>
    <?php
}
