$(function () {
  $(".language").click(function () {
    var $language = $(".language");
    var position = $language.position();
    var width = $language.outerWidth();
    var height = $language.outerHeight();
    $(".languages")
      .toggle()
      .css({
        left: position.left + width - $(".languages").outerWidth(),
        top: position.top + height,
      });
  });
  $(document).mouseup(function (e) {
    var languages = $(".languages");
    var language = $(".language");

    if (language.is(e.target) || language.has(e.target).length > 0) {
      return;
    } else if (
      !languages.is(e.target) &&
      languages.has(e.target).length === 0
    ) {
      languages.hide();
    }
  });
  $("a.shot").colorbox({
    rel: "gal",
    maxWidth: "100%",
    maxHeight: "100%",
    width: "100%",
    height: "100%",
    current: "{current}/{total}",
  });
});
