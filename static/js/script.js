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
      url: "/static/imagenes/image.png",
      nombre: "",
      descripcion:
        "Sabores que conquistan tu paladar: platos únicos preparados con pasión y frescura.",
    },
    {
      url: "/static/imagenes/image.webp",
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
  // Corazon: hay varios botones repetidos en el loop, usar selector por clase
  const corazones = document.querySelectorAll('.btnCorazon');
  if (corazones && corazones.length) {
    corazones.forEach((btn) => {
      btn.addEventListener('click', function (e) {
        // el div que contiene la clase navcoro/no_navcoro está dentro del botón
        // o inmediatamente en el formulario; buscamos primero dentro del botón
        let elemento = btn.querySelector('.navcoro, .no_navcoro');
        if (!elemento) {
          // fallback: buscar en el formulario padre
          const form = btn.closest('form');
          if (form) elemento = form.querySelector('.navcoro, .no_navcoro');
        }
        if (!elemento) return; // nada que alternar

        if (elemento.classList.contains('navcoro')) {
          elemento.classList.remove('navcoro');
          elemento.classList.add('no_navcoro');
        } else {
          elemento.classList.remove('no_navcoro');
          elemento.classList.add('navcoro');
        }

        // Nota: el botón es de tipo submit en la plantilla. Si quieres que la
        // acción sea solo visual (sin enviar el formulario), descomenta la
        // siguiente línea:
        // e.preventDefault();
      });
    });
  }

function mostrarModal(elemento) {
  const id = elemento.closest(".item-receta").getAttribute("data-modal");
  const modal = document.querySelector(`.ventana-modal[data-modal="${id}"]`);
  const cerrarModal = modal.querySelector(".cerrar-modal");


  modal.classList.add("modal--show");


  cerrarModal.addEventListener("click", function (e) {
    e.preventDefault();
    modal.classList.remove("modal--show");
  });

  window.addEventListener("click", function (e) {
    if (e.target === modal) {
      modal.classList.remove("modal--show");
    }
  });
}


// Manejo del botón responsivo btnMenu3: abre/cierra navbar3
const btnMenu3 = document.getElementById('btnMenu3');
const navbar3 = document.getElementById('navbar3');
if (btnMenu3 && navbar3) {
  btnMenu3.addEventListener('click', function (e) {
    // evitar que el click burbujee al listener global de document
    e.stopPropagation();
    if (navbar3.classList.contains('navbar3')) {
      navbar3.classList.remove('navbar3');
      navbar3.classList.add('no_navbar3');
    } else {
      navbar3.classList.remove('no_navbar3');
      navbar3.classList.add('navbar3');
    }
  });
}


document.addEventListener('click', function (e) {
  const menu = document.getElementById('navbar3');
  const btn  = document.getElementById('btnMenu3');
  if (!menu || !btn) return;

  const abierto       = menu.classList.contains('navbar3');
  const clickEnMenu   = menu.contains(e.target);
  const clickEnBoton  = btn.contains(e.target);  

  if (abierto && !clickEnMenu && !clickEnBoton) {
    menu.classList.remove('navbar3');
    menu.classList.add('no_navbar3'); 
  }
});

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    const menu = document.getElementById('navbar3');
    if (menu && menu.classList.contains('navbar3')) {
      menu.classList.remove('navbar3');
      menu.classList.add('no_navbar3');
    }
  }
});
