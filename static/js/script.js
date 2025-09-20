document.addEventListener("DOMContentLoaded", function () {
  // Menú
  const btnMenu = document.getElementById("btnMenu");
  if (btnMenu) {
    btnMenu.addEventListener("click", function () {
      let elemento = document.getElementById("navbar");
      if (elemento.classList.contains("navbar")) {
        elemento.classList.remove("navbar");
        elemento.classList.add("no_navbar");
      } else {
        elemento.classList.remove("no_navbar");
        elemento.classList.add("navbar");
      }
    });
  }

  const btnMenu2 = document.getElementById("btnMenu2");
  if (btnMenu2) {
    btnMenu2.addEventListener("click", function () {
      let elemento = document.getElementById("navbar2");
      if (elemento.classList.contains("navbar2")) {
        elemento.classList.remove("navbar2");
        elemento.classList.add("no_navbar2");
      } else {
        elemento.classList.remove("no_navbar2");
        elemento.classList.add("navbar2");
      }
    });
  }

  // Mostrar instrucciones receta
  window.mostrarInstrucciones = function (elemento) {
    document.querySelectorAll(".receta .instrucciones").forEach((el) => {
      if (el !== elemento.querySelector(".instrucciones")) {
        el.classList.add("oculto");
      }
    });
    const actual = elemento.querySelector(".instrucciones");
    actual.classList.toggle("oculto");
  };

  // Carrusel
  let imagenes = [
    {
      url: "/static/imagenes/lasaña.jpg",
      nombre: "",
      descripcion:
        "De la cocina a tu mesa: experiencias culinarias que despiertan los sentidos.",
    },
    {
      url: "/static/imagenes/plato.webp",
      nombre: "",
      descripcion:
        "Sabores que conquistan tu paladar: platos únicos preparados con pasión y frescura.",
    },
    {
      url: "/static/imagenes/comida.jpg",
      nombre: "",
      descripcion:
        "Explora nuestra selección gastronómica: tradición, creatividad y mucho sabor en cada bocado.",
    },
  ];

  let atras = document.getElementById("atras");
  let adelante = document.getElementById("adelante");
  let imagen = document.getElementById("img");
  let puntos = document.getElementById("puntos");
  let texto = document.getElementById("texto");
  let actual = 0;
  let intervaloCarrusel = null;

  function mostrarCarrusel() {
    imagen.innerHTML = `<img class="img" src="${imagenes[actual].url}" alt="logo pagina" loading="lazy">`;
    texto.innerHTML = `
      <h3>${imagenes[actual].nombre}</h3>
      <p>${imagenes[actual].descripcion}</p>
    `;
    posicionCarrusel();
  }

  function posicionCarrusel() {
    puntos.innerHTML = "";
    for (let i = 0; i < imagenes.length; i++) {
      puntos.innerHTML += `<span class="${
        i === actual ? "bold" : ""
      }">● </span>`;
    }
  }

  function avanzarCarrusel() {
    actual = (actual + 1) % imagenes.length;
    mostrarCarrusel();
  }

  if (atras && adelante && imagen && texto && puntos) {
    atras.addEventListener("click", function () {
      actual = (actual - 1 + imagenes.length) % imagenes.length;
      mostrarCarrusel();
      reiniciarIntervalo();
    });

    adelante.addEventListener("click", function () {
      avanzarCarrusel();
      reiniciarIntervalo();
    });

    // Inicializa carrusel
    mostrarCarrusel();

    // Carrusel automático cada 3 segundos
    intervaloCarrusel = setInterval(avanzarCarrusel, 3000);

    // Reinicia el intervalo si el usuario interactúa
    function reiniciarIntervalo() {
      clearInterval(intervaloCarrusel);
      intervaloCarrusel = setInterval(avanzarCarrusel, 3000);
    }
  }
});

window.addEventListener("scroll", function () {
  var header = document.querySelector(".header");
  header.classList.toggle("abajo", window.scrollY > 0);
});



  // Corazon
  
  const btnCorazon = document.getElementById("btnCorazon");
  if (btnCorazon) {
    btnCorazon.addEventListener("click", function () {
      let elemento = document.getElementById("navcoro");
      if (elemento.classList.contains("navcoro")) {
        elemento.classList.remove("navcoro");
        elemento.classList.add("no_navcoro");
      } else {
        elemento.classList.remove("no_navcoro");
        elemento.classList.add("navcoro");
      }
    });
  }
