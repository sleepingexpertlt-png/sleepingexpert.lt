<?php
/**
 * SE Bio Link — serves https://sleepingexpert.lt/link/ as a standalone page.
 *
 * Įdiegimas (vieną kartą): WP Admin → Snippets → Add New → įklijuoti šį kodą
 * (be pirmos eilutės "<?php"), Scope: "Run snippet everywhere", Save & Activate.
 *
 * Kaip veikia: deploy.py įkelia biolink/index.html į WP media kaip
 * "se-biolink-<data>.html". Šis snippet'as, gavęs užklausą į /link/, suranda
 * naujausią tokį failą ir atiduoda jį be temos, be header/footer, be WP užklausų.
 * Jei failo nėra, snippet'as nieko nedaro ir WP toliau dirba įprastai (404).
 */
add_action( 'init', function () {
	$uri = isset( $_SERVER['REQUEST_URI'] ) ? (string) $_SERVER['REQUEST_URI'] : '';
	$path = strtolower( trim( (string) parse_url( $uri, PHP_URL_PATH ), '/' ) );
	if ( $path !== 'link' ) {
		return;
	}

	$items = get_posts( array(
		'post_type'      => 'attachment',
		'post_status'    => 'inherit',
		'posts_per_page' => 1,
		'orderby'        => 'date',
		'order'          => 'DESC',
		's'              => 'se-biolink',
		'search_columns' => array( 'post_title', 'post_name' ),
		'fields'         => 'ids',
	) );
	if ( empty( $items ) ) {
		return;
	}

	$file = get_attached_file( (int) $items[0] );
	if ( ! $file || ! is_readable( $file ) ) {
		return;
	}

	// Viena kanoninė forma: /link/ su pasviruoju brūkšniu.
	if ( substr( (string) parse_url( $uri, PHP_URL_PATH ), -1 ) !== '/' ) {
		wp_safe_redirect( home_url( '/link/' . ( ! empty( $_SERVER['QUERY_STRING'] ) ? '?' . $_SERVER['QUERY_STRING'] : '' ) ), 301 );
		exit;
	}

	nocache_headers();
	header( 'Content-Type: text/html; charset=utf-8' );
	header( 'Cache-Control: public, max-age=300' );
	header( 'X-LiteSpeed-Cache-Control: no-cache' );
	header( 'X-Robots-Tag: all' );
	readfile( $file );
	exit;
}, 1 );
