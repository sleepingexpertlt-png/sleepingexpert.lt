<?php
/**
 * Plugin Name: SE – Užsakymo peržiūra su PVM
 * Description: Mano paskyra → Užsakymai → Peržiūrėti: užsakymo lentelėje ir spausdinamame „Individualus užsakymas“ dokumente sumos rodomos su PVM. Kiti puslapiai (krepšelis, apmokėjimas, laiškai, administravimas, išankstinė sąskaita) nesikeičia.
 * Version: 1.1.0
 * Author: Sleeping Expert
 * Requires Plugins: woocommerce
 * Text Domain: se-uzsakymas-su-pvm
 */

defined( 'ABSPATH' ) || exit;

function se_uzsakymas_su_pvm_is_view_order() {
	return ! is_admin()
		&& ! wp_doing_ajax()
		&& function_exists( 'is_wc_endpoint_url' )
		&& did_action( 'wp' )
		&& is_wc_endpoint_url( 'view-order' );
}

/**
 * 1. WooCommerce užsakymo lentelė: tik šio puslapio užklausos metu nustatymas
 *    woocommerce_tax_display_cart grąžinamas kaip „incl“. Duomenų bazėje niekas nekeičiama.
 */
add_filter( 'option_woocommerce_tax_display_cart', function ( $value ) {
	return se_uzsakymas_su_pvm_is_view_order() ? 'incl' : $value;
} );

/**
 * 2. „Individualus užsakymas“ (#se-order-confirmation): serveris paruošia sumas su PVM,
 *    o skriptas jas įrašo į dokumentą. Jei dokumento struktūra neatitinka, jis paliekamas nepakeistas.
 *    Išankstinė sąskaita (#se-proforma-invoice) neliečiama.
 */
add_action( 'wp_footer', function () {
	if ( ! se_uzsakymas_su_pvm_is_view_order() ) {
		return;
	}

	$order_id = absint( get_query_var( 'view-order' ) );
	$order    = $order_id ? wc_get_order( $order_id ) : false;
	if ( ! $order || ! current_user_can( 'view_order', $order_id ) || (float) $order->get_total_tax() <= 0 ) {
		return;
	}

	$args  = array( 'currency' => $order->get_currency() );
	$items = array();
	$sum   = 0.0;
	foreach ( $order->get_items() as $item ) {
		$qty   = max( 1, (float) $item->get_quantity() );
		$line  = (float) $item->get_subtotal() + (float) $item->get_subtotal_tax();
		$sum  += $line;
		$items[] = array(
			'name' => html_entity_decode( wp_strip_all_tags( $item->get_name() ), ENT_QUOTES, 'UTF-8' ),
			'unit' => wc_price( $line / $qty, $args ),
			'line' => wc_price( $line, $args ),
		);
	}

	$data = array(
		'items'    => $items,
		'subtotal' => wc_price( $sum, $args ),
		'shipping' => wc_price( (float) $order->get_shipping_total() + (float) $order->get_shipping_tax(), $args ),
	);
	?>
	<script id="se-uzsakymas-su-pvm">
	(function () {
		var D = <?php echo wp_json_encode( $data ); ?>;
		function norm(s) { return String(s || '').replace(/\s+/g, ' ').trim(); }
		function run() {
			var doc = document.getElementById('se-order-confirmation');
			if (!doc || doc.getAttribute('data-se-pvm')) return;
			var rows = doc.querySelectorAll('.se-doc-table tbody tr');
			if (rows.length !== D.items.length) return;

			// Pirma patikrinam, ar visos eilutės atitinka užsakymo prekes; jei ne – nieko nekeičiam.
			var plan = [];
			for (var i = 0; i < rows.length; i++) {
				var name = rows[i].querySelector('td strong');
				var cells = rows[i].querySelectorAll('td');
				if (!name || cells.length < 4 || norm(name.textContent) !== norm(D.items[i].name)) return;
				plan.push(cells);
			}
			plan.forEach(function (cells, i) {
				cells[2].innerHTML = D.items[i].unit;
				cells[3].innerHTML = D.items[i].line;
			});

			var th = doc.querySelectorAll('.se-doc-table thead th');
			if (th.length >= 4) { th[2].textContent = 'Kaina su PVM'; th[3].textContent = 'Suma su PVM'; }

			doc.querySelectorAll('.se-doc-totals tr').forEach(function (tr) {
				var l = tr.querySelector('.label'), v = tr.querySelector('.value');
				if (!l || !v) return;
				var t = norm(l.textContent);
				if (t === 'Produktų suma:') v.innerHTML = D.subtotal;
				else if (t === 'Pristatymas:') v.innerHTML = D.shipping;
				else if (/^PVM \(/.test(t)) l.textContent = 'iš jų ' + t;
			});
			doc.setAttribute('data-se-pvm', '1');
		}
		if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
	})();
	</script>
	<?php
}, 99 );
