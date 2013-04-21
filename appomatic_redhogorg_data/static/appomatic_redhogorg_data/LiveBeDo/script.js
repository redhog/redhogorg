$(document).ready(function () {
  function setCookie(c_name, value, exdays) {
    var exdate=new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
    document.cookie=c_name + "=" + c_value;
  }

  function getCookie(c_name) {
    var c_value = document.cookie;
    var c_start = c_value.indexOf(" " + c_name + "=");
    if (c_start == -1) {
      c_start = c_value.indexOf(c_name + "=");
    }
    if (c_start == -1) {
      c_value = null;
    } else {
      c_start = c_value.indexOf("=", c_start) + 1;
      var c_end = c_value.indexOf(";", c_start);
      if (c_end == -1) {
        c_end = c_value.length;
      }
      c_value = unescape(c_value.substring(c_start,c_end));
    }
    return c_value;
  }

  function animate(animationsList, callback) {
    var animations = callback;
    if (typeof animations == 'undefined') animations = function () {};

    $.each(animationsList.reverse(), function () {
      var listItem = this;
      var animationsTmp = animations;
      animations = function () {
        listItem.node.animate(listItem.properties, listItem.duration, listItem.easing, animationsTmp);
      }
    });

    animations();
  }

  if (getCookie("redhogorg_intro")) {
    animate([
      {node: $(".intro"), properties: {'opacity': 1.0}, duration:1000, easing:'linear'},
      {node: $(".intro"), properties: {'opacity': 0.0}, duration:500, easing:'linear'},
    ],
    function () {
      $(".intro").hide();
    });
    return;
  }
  setCookie("redhogorg_intro", 1);

  animate([
    {node: $(".intro .seq0"), properties: {'opacity': 1.0}, duration:500, easing:'linear'},
    {node: $(".intro .seq0"), properties: {'opacity': 0.0}, duration:500, easing:'linear'},
    {node: $(".intro .seq1"), properties: {'opacity': 1.0}, duration:500, easing:'linear'},
    {node: $(".intro .seq1"), properties: {'opacity': 0.0}, duration:500, easing:'linear'},
    {node: $(".intro .seq2"), properties: {'opacity': 1.0}, duration:500, easing:'linear'},
    {node: $(".intro .seq2"), properties: {'opacity': 0.0}, duration:500, easing:'linear'},
    {node: $(".intro .seq3"), properties: {'opacity': 1.0}, duration:500, easing:'linear'},
    {node: $(".intro .seq3"), properties: {'opacity': 0.0}, duration:500, easing:'linear'},
    {node: $(".intro .seq4"), properties: {'opacity': 1.0}, duration:500, easing:'linear'},
    {node: $(".intro .seq4"), properties: {'opacity': 0.0}, duration:500, easing:'linear'},
    {node: $(".intro .seq5"), properties: {'opacity': 1.0}, duration:500, easing:'linear'},
    {node: $(".intro .seq5"), properties: {'opacity': 0.0}, duration:500, easing:'linear'},
    {node: $(".intro"), properties: {'opacity': 0.0}, duration:500, easing:'linear'},
  ],
  function () {
    $(".intro").hide();
  });

});
