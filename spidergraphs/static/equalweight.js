django.jQuery(document).ready(function(){
    function roundNumber(number, digits) {
        var multiple = Math.pow(10, digits);
        var rndedNum = Math.round(number * multiple) / multiple;
        return rndedNum;
    }
    django.jQuery('.equalizelink').each(function(){
        django.jQuery(this).click(function(e){
            e.preventDefault();
            fields = django.jQuery.makeArray(django.jQuery(this).parents('.inline-group').find('td.field-weight input'));
            //There's an extra one selected every time, so get rid of it.
            fields.pop();
            newWeight = roundNumber(1 / fields.length, 3);
            for(var i=0;i<fields.length;i++){
                django.jQuery(fields[i]).val(newWeight);
            };
        });
    });
});
