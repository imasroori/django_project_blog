$(document).ready(function(){

  var menu = $(".menu");
  var hamburger = $(".hamburger");
  var menuOpen;

  function openMenu(){
    menu.css("right", "0px");
    menuOpen = true;
  }

  function closeMenu(){
    menu.css("right", "-200px");
    menuOpen = false;
  }

//  function toggleMenu(){
//    if (menuOpen) {
//      closeMenu();
//    } else {
//      openMenu();
//    }
//  }

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

var toggler = document.getElementsByClassName("caret");
var i;

for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".nested").classList.toggle("active");
    this.classList.toggle("caret-down");
  });
}

});