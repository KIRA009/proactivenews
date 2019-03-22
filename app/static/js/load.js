function animate() {
	setTimeout(function() {
		$('#box-rl').css('opacity', '0');
		$('#box-rl').addClass('close-up');
	}, 1000);
	setTimeout(function() {
		$('#box-rl').addClass('rl-orig');
		$('#box-ru').addClass('close-left');
		$('#box-ru').css('opacity', '0');
	}, 2000);
	setTimeout(function() {
		$('#box-ru').addClass('ru-orig');
		$('#box-lu').addClass('close-down');
		$('#box-lu').css('opacity', '0');
	}, 3000);
	setTimeout(function() {
		$('#box-lu').addClass('lu-orig');
		$('#box-rl').addClass('open-right');
		$('#box-rl').css('opacity', '1');
	}, 4000);
	setTimeout(function() {
		$('#box-ru').css('opacity', '1');
		$('#box-ru').addClass('open-top');
	}, 5000);
	setTimeout(function() {
		$('#box-lu').css('opacity', '1');
		$('#box-lu').addClass('open-left');
	}, 6000);
	$('#box-rl').removeClass('close-up').removeClass('rl-orig').removeClass('open-right');
	$('#box-ru').removeClass('close-left').removeClass('ru-orig').removeClass('open-top');
	$('#box-lu').removeClass('close-down').removeClass('lu-orig').removeClass('open-left');
}
$('#content').css('visibility', 'hidden');
document.onreadystatechange = function () {
  	state = document.readyState
	if (state == 'interactive') {
		$('body').addClass('h100');
	   	$('#load').css('visibility', 'visible');
	   	$('#content').css('visibility', 'hidden');
	   	animate();
	   	var an = setInterval(animate, 6100);
	}
	else if (state == 'complete') {
    	$('#load').remove();
    	$('#content').css('visibility', 'visible');
		$('body').removeClass('h100');
	}
}