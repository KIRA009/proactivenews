$('.category').click(function() {
	window.location.href = '/news/category/' + $(this).html().toLowerCase();
});

$('.save').hover(function() {
	if ($(this).html() == 'Saved')
		$(this).html('Unsave');
}, function() {
	if ($(this).html() == 'Unsave')
		$(this).html('Saved');
});