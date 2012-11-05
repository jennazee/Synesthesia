$('document').ready(function(){

	var colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'black', 'gray'];

	$.each(colors, function(i, v) {
		$('#color-list').append('<li><input type="checkbox" name="color" value="'+v+'">'+v+'</input></li>');
	});

	$.getJSON('/fonts', function(data){
		$.each(data, function(i, v){
			$('#font-select').append('<option name="font">'+v+'</option>')
		})
	})
});
