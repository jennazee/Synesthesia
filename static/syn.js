$('document').ready(function(){

	var colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'black', 'grey', 'brown'];

	$.each(colors, function(i, v) {
		$('#color-list').append('<li><input type="checkbox" name="color" value="'+v+'">'+v+'</input></li>');
	});

	$.getJSON('/fonts', function(data){
		$.each(data, function(i, v){
			$('#font-select').append('<option value="'+v+'">'+v+'</option>')
		})
	})

	//adapted from http://stackoverflow.com/questions/4459379/preview-an-image-before-it-is-uploaded
 	$('#pic-up').change(function(){
 		if (this.files && this.files[0]) {
            if (!(this.files[0].type === "image/jpeg" || this.files[0].type === "image/jpg" || this.files[0].type === "image/png")) {
                $('#prev-box').addClass('hidden');
                alert("That type of file isn't supported. Please try a different image.")
            }
            else {
                var reader = new FileReader();
                reader.onload = function (e) {
                    $('#preview').attr('src', e.target.result)
                    $('#prev-box').removeClass('hidden');
                };
                reader.readAsDataURL(this.files[0]);
            }
        }
 	});

 	$('#parameterbox').submit(function() {
        if ($('#pic-up').val() === '') {
            alert('You must upload an image!')
            return false
        }
        if ($("input:checked").length === 0) {
            alert('You choose some colors for your image!')
            return false
        }
 		var fd = new FormData();
    	fd.append('photo', $('#pic-up')[0].files[0]);
    	$.each($('#parameterbox').serializeArray(), function(i, v){
    		fd.append(v.name, v.value)
    	})
        $('#swirl').removeClass('hidden')
        $('#creation-wrapper').addClass('hidden');
	    $.ajax({
	       	url: "/upload",
	       	type: "POST",
	      	data: fd,
	  	    processData: false,
	     	contentType: false,
	    	success: function(data) {
                $('#swirl').addClass('hidden')
	       		$('#word-pic-prev').attr('src', data)
	          	$('#creation-wrapper').removeClass('hidden');
	          	set_clickable()
	       	}
	    });
        return false;
    });

 	var set_clickable = function(){
	    $('#word-pic-prev').click(function(){
	    	var pic_id = $(this).attr('src').split('/')[1]
	    	window.location.href='download/'+pic_id
	    })
	}

	$('#p-pol').click(function(){
		$('#p-policy').removeClass('hidden')
	})

	$('#pp-close').click(function(){
		$('#p-policy').addClass('hidden')
	})

    	
        
});
