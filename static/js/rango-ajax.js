$(document).ready(function() {
	$('#dislike_btn').click(function() {
		var catememeIdVar;
		catememeIdVar = $(this).attr('data-memeid');

		$.get('/rango/dislike_meme/',
			{'meme_id': catememeIdVar},
			function(data) {
				$('#like_count').html(data);
				$('#dislike_btn').hide();
			})
	});
});

