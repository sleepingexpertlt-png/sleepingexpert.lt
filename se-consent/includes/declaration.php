<?php
/**
 * [se_cookie_declaration] — slapukų deklaracija privatumo politikos puslapiui.
 * [cookie_declaration] palaikomas kaip Cookiebot įskiepio sinonimas, kad nereikėtų taisyti puslapių.
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('init', function () {
    add_shortcode('se_cookie_declaration', 'se_consent_declaration_shortcode');
    if (!shortcode_exists('cookie_declaration')) {
        add_shortcode('cookie_declaration', 'se_consent_declaration_shortcode');
    }
});

function se_consent_declaration_shortcode() {
    $s    = se_consent_settings();
    $t    = $s['texts'][se_consent_lang()];
    $lt   = se_consent_lang() === 'lt';
    $by   = [];
    foreach (se_consent_cookie_list() as $c) {
        $by[$c['category']][] = $c;
    }

    ob_start();
    ?>
    <div class="se-c-decl">
        <p class="se-c-decl__state" data-se-consent-state>
            <?php echo esc_html($lt ? 'Jūsų sutikimo būsena bus parodyta įkėlus puslapį.' : 'Your consent status will be shown once the page loads.'); ?>
        </p>
        <p>
            <a href="#se-consent" class="se-consent-open"><?php echo esc_html($t['reopen']); ?></a>
        </p>
        <?php foreach (SE_CONSENT_CATEGORIES as $cat) : ?>
            <h3><?php echo esc_html($t['cat'][$cat][0]); ?> (<?php echo count($by[$cat] ?? []); ?>)</h3>
            <p><?php echo esc_html($t['cat'][$cat][1]); ?></p>
            <?php if (!empty($by[$cat])) : ?>
                <table class="se-c-decl__table">
                    <thead><tr>
                        <th><?php echo esc_html($lt ? 'Pavadinimas' : 'Name'); ?></th>
                        <th><?php echo esc_html($lt ? 'Tiekėjas' : 'Provider'); ?></th>
                        <th><?php echo esc_html($lt ? 'Paskirtis' : 'Purpose'); ?></th>
                        <th><?php echo esc_html($lt ? 'Galiojimas' : 'Expiry'); ?></th>
                    </tr></thead>
                    <tbody>
                    <?php foreach ($by[$cat] as $c) : ?>
                        <tr>
                            <td><code><?php echo esc_html($c['name']); ?></code></td>
                            <td><?php echo esc_html($c['provider']); ?></td>
                            <td><?php echo esc_html($c['purpose']); ?></td>
                            <td><?php echo esc_html($c['expiry']); ?></td>
                        </tr>
                    <?php endforeach; ?>
                    </tbody>
                </table>
            <?php endif; ?>
        <?php endforeach; ?>
    </div>
    <script data-se-consent-ignore>
    (function () {
        var el = document.querySelector('[data-se-consent-state]');
        if (!el || !window.SEConsent) return;
        var lt = <?php echo $lt ? 'true' : 'false'; ?>;
        function render() {
            var s = window.SEConsent.get();
            if (!s) { el.textContent = lt ? 'Sutikimas dar neduotas.' : 'No consent given yet.'; return; }
            var names = { preferences: <?php echo wp_json_encode($t['cat']['preferences'][0]); ?>, statistics: <?php echo wp_json_encode($t['cat']['statistics'][0]); ?>, marketing: <?php echo wp_json_encode($t['cat']['marketing'][0]); ?> };
            var on = [<?php echo wp_json_encode($t['cat']['necessary'][0]); ?>];
            for (var k in names) if (s.c[k]) on.push(names[k]);
            el.textContent = (lt ? 'Leidžiate: ' : 'Allowed: ') + on.join(', ') + '. ' +
                (lt ? 'Sutikimo ID: ' : 'Consent ID: ') + s.id + ', ' + new Date(s.t).toLocaleString();
        }
        render();
        window.SEConsent.onChange(render);
    })();
    </script>
    <?php
    return (string) ob_get_clean();
}
