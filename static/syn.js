$('document').ready(function(){

	var colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'white', 'black', 'gray'];

	$.each(colors, function(i, v) {
		$('#color-list').append('<li><input type="checkbox" name="color" value="'+v+'">'+v+'</input></li>');
	});
});
