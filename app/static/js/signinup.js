$('.nav-item').hover(function() {
	if (!$(this).children('.nav-link').hasClass('active'))
		$(this).addClass('hover');
	$(this).children('.nav-link').addClass('hover');
}, function() {
	if (!$(this).children('.nav-link').hasClass('active'))
		$(this).removeClass('hover');
	$(this).children('.nav-link').removeClass('hover');
});

$('#show-password').click(function(event) {
	$password = $('#password');
	if ($password.attr('type') == "password") {
		$(this).html('Hide Password');
		$password.attr('type', 'text');
	}
	else {
		$(this).html('Show Password');
		$password.attr('type', 'password');
	}
});