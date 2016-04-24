$(document).ready(function() {
	var providers = []
	$('#output').hide()
	var update_summary = function(zipcode, age, npi){
	    $.post('/search', {"zipcode": zipcode, "age": age,"npi":npi}, 
			   function(data){
				   var res = JSON.parse(data);
				   if (npi == "") {
					   $('#plan-provider-item').hide()
				   } else {
					   $('#plan-provider-item').show()
					   $('#plan-state-comp').html(res['state_comp'])
					   $('#plan-state-comp').addClass((res['state_comp'].indexOf("pricier") > -1)?"bad":"good");
				   }
				   $('#plot').html(res['plot_div'])
				   eval($(res['script']).text())
				   $('#plan-num').html(res['num_plans'])
				   $('#plan-national-comp').html(res['national_comp'])
				   $('#plan-national-comp').addClass((res['national_comp'].indexOf("pricier") > -1)?"bad":"good");
				   // console.log(res['num_plans'])
				   $('#output').show()
				   console.log(res['plans'])
				   
				   $('#plan-container').html(res['plans'])
			   });
	}
	$('#gobtn').click(function (){
		update_summary($('#zipcode').val(), $('#age').val(),"")
	});

    $( "#provider" ).autocomplete({
      source: function( request, response ) {
        $.post('/search_providers', {"zipcode": $('#zipcode').val(), "age": $('#age').val(), "q":request.term }, 
			   function(data){
				   response(data.result);
			   });
      },
      minLength: 3,
      select: function( event, ui ) {
		update_summary($('#zipcode').val(), $('#age').val(),ui.item.npi)
        return true;
      }
	  })
	  .autocomplete( "instance" )._renderItem = function( ul, item ) {
      return $( "<li class='autocomplete'>" )
        .append( "<a>" + item.label + "<br> <span class=desc>" + item.desc + "</span></a>" )
        .appendTo( ul );
    };;
})
