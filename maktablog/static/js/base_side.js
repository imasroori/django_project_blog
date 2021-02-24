$(document).ready(function(){

  var menu = $(".menu");
  var hamburger = $(".hamburger");
  var line = $(".line");
  var menuOpen;

  function openMenu(){
    menu.css("right", "0px");
    line.css("background", "#FFF");
    menuOpen = true;
  }

  function closeMenu(){
    menu.css("right", "-320px");
    line.css("background", "#BCAD90");
    menuOpen = false;
  }

  function toggleMenu(){
    if (menuOpen) {
      closeMenu();
    } else {
      openMenu();
    }
  }

  hamburger.on({
    mouseenter: function(){
      openMenu();
    }
  });

  menu.on({
    mouseleave: function(){
      closeMenu();
    }

  });

  hamburger.on({
    click: function(){
      toggleMenu();
    }
  })



});