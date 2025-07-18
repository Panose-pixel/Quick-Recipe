document.getElementById("btnMenu").addEventListener("click",
    function () {
      
      let elemento = document.getElementById("navbar");
      if (elemento.classList.contains("navbar")) {
        elemento.classList.remove("navbar");
        elemento.classList.add("no_navbar");
      } else {
        elemento.classList.remove("no_navbar");
        elemento.classList.add("navbar");
      }
  
    });
    document.getElementById("btnMenu2").addEventListener("click",
    function () {
      
      let elemento = document.getElementById("navbar2");
      if (elemento.classList.contains("navbar2")) {
        elemento.classList.remove("navbar2");
        elemento.classList.add("no_navbar2");
      } else {
        elemento.classList.remove("no_navbar2");
        elemento.classList.add("navbar2");
      }
  
    });


  function mostrarInstrucciones(elemento) {
    // Oculta todas las instrucciones
    document.querySelectorAll(".receta .instrucciones").forEach(el => {
      if (el !== elemento.querySelector('.instrucciones')) {
        el.classList.add("oculto");
      }
    });

    // Alterna la actual
    const actual = elemento.querySelector(".instrucciones");
    actual.classList.toggle("oculto");
  }
