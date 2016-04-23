$(document).ready(function() {
	$('#output').hide()
	$('#gobtn').click(function (){
	    $.post('/search', {"zipcode": $('#zipcode').val(), "age": $('#age').val()}, 
			   function(data){
				   // $("#result").html(JSON.stringify(data));
				   var res = JSON.parse(data);
				   $('#plot').html(res['plot_div'])
				   eval($(res['script']).text())
				   $('#output').show()
			   });
	});
})
