<?php
/**
 * Plugin Name: SE – Užsakymo peržiūra su PVM
 * Description: Mano paskyra → Užsakymai → Peržiūrėti: prekių eilučių ir suvestinės sumas rodo su PVM. Kiti puslapiai (krepšelis, apmokėjimas, laiškai, administravimas, PDF) nesikeičia.
 * Version: 1.0.0
 * Author: Sleeping Expert
 * Requires Plugins: woocommerce
 * Text Domain: se-uzsakymas-su-pvm
 */

defined( 'ABSPATH' ) || exit;

/**
 * WooCommerce užsakymo peržiūros šablone (order-details) sumos formuojamos pagal
 * nustatymą woocommerce_tax_display_cart. Tik šio puslapio užklausos metu
 * grąžiname „incl“. Duomenų bazėje niekas neįrašoma ir užsakymų sumos nekeičiamos.
 */
add_filter( 'option_woocommerce_tax_display_cart', 'se_uzsakymas_su_pvm_display' );

function se_uzsakymas_su_pvm_display( $value ) {
	if ( is_admin() || wp_doing_ajax() || ! function_exists( 'is_wc_endpoint_url' ) ) {
		return $value;
	}
	if ( did_action( 'wp' ) && is_wc_endpoint_url( 'view-order' ) ) {
		return 'incl';
	}
	return $value;
}
