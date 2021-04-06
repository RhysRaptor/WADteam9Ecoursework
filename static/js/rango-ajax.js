$(document).ready(function() {
	$('#like_btn').click(function() {
		var catememeIdVar;
		catememeIdVar = $(this).attr('data-memeid');

		$.get('/rango/like_meme/',
			{'meme_id': catememeIdVar},
			function(data) {
				$('#like_count').html(data)
				$('#like_btn').hide();
			})
	});
	$('#dislike_btn').click(function() {
		var catememeIdVar;
		catememeIdVar = $(this).attr('data-memeid');

		$.get('/rango/dislike_meme/',
			{'meme_id': catememeIdVar},
			function(data) {
				$('#dislike_count').html(data);
				$('#dislike_btn').hide();
			})
	});
});

