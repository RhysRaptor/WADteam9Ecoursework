$(document).ready(function() {
	$('#like_btn').click(function() {
		var catememeIdVar;
		catememeIdVar = $(this).attr('data-memeid');

		$.get('/rango/like_meme/',
			{'meme_id': catememeIdVar},
			function(data) {
				$('#like_count').html(data);
				$('#like_btn').hide();
			})
	});
});
