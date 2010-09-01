/**
 * Initializes mirror selection.
 */
$(document).ready(function(){
    /* Mirror selection by js */
    $('form#mirrorselect select').change(function () {
        $('form#mirrorselect').submit();
        return true;
    });
    /* Hide submit button */
    $('form#mirrorselect input').addClass('jshidden');
});

/* Flattr */
(function() {
    var s = document.createElement('script'), t = document.getElementsByTagName('script')[0];

    s.type = 'text/javascript';
    s.async = true;
    s.src = 'http://api.flattr.com/js/0.5.0/load.js?mode=auto';

    t.parentNode.insertBefore(s, t);
})();

