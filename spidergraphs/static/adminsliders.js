//TODO doens't work on new ones added with the add-row
django.jQuery(document).ready(function(){
    django.jQuery('.field-applied, .field-specialized, .field-intellectual, .field-broad, .field-civic, .field-weight').find('input').each(function(){
        django.jQuery(this).after('<div class="slider-vertical" style="height:100px;margin: 10px;"></div>');
    });
	django.jQuery( ".slider-vertical" ).each(function(){
        django.jQuery(this).slider({
		    orientation: "vertical",
		    range: "min",
		    min: 0,
		    max: 100,
		    value: django.jQuery(this).parents('td').find('input').val()*100,
		    slide: function( event, ui ) {
                django.jQuery(this).parents('td').find('input').val(ui.value/100);
		    }
	    });
    });
});
