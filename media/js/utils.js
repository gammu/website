/**
 * Initializes mirror selection.
 */
window.addEvent('domready',function(){  
    /* Mirror selection by js */
    $$('form#mirrorselect select').addEvent('change', function (e) {
        e.stop();
        $('mirrorselect').submit();
    });
    /* Hide submit button */
    $$('form#mirrorselect input').setStyle('visibility', 'hidden');
});  
