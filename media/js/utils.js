if (top != self) {
    top.location.replace(location);
}

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
