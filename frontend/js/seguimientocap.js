// Array para almacenar los datos de capacitaciones
var capacitaciones = [];

// Función para agregar capacitación
function agregarCapacitacion() {
  // Obtener los valores del formulario
  var fecha = document.getElementById("fecha").value;
  var apellido = document.getElementById("apellido").value;
  var nombre = document.getElementById("nombre").value;
  var capacitacion = document.getElementById("capacitacion").value;
  var sector = document.getElementById("sector").value;
  var email = document.getElementById("email").value;

  // Validar que no haya campos vacíos
  if (!fecha || !apellido || !nombre || !capacitacion || !sector || !email) {
    alert("Por favor, complete todos los campos.");
    return;
  }

  // Crear un objeto con los datos de la capacitación
  var nuevaCapacitacion = {
    fecha: fecha,
    apellido: apellido,
    nombre: nombre,
    capacitacion: capacitacion,
    sector: sector,
    email: email
  };

  // Agregar el objeto al array de capacitaciones
  capacitaciones.push(nuevaCapacitacion);

  // Actualizar la tabla con los datos
  actualizarTabla();

  // Limpiar los campos del formulario después de agregar la capacitación
  document.getElementById("fecha").value = "";
  document.getElementById("apellido").value = "";
  document.getElementById("nombre").value = "";
  document.getElementById("capacitacion").value = "";
  document.getElementById("sector").value = "";
  document.getElementById("email").value = "";
}

// Función para actualizar la tabla con los datos de capacitaciones
function actualizarTabla() {
  var tabla = document.getElementById("tablaCapacitaciones");
  tabla.innerHTML = ""; // Limpiar la tabla antes de actualizar

  // Recorrer el array de capacitaciones y agregar filas a la tabla
  for (var i = 0; i < capacitaciones.length; i++) {
    var fila = "<tr><td>" + capacitaciones[i].fecha + "</td><td>" + capacitaciones[i].apellido + "</td><td>" + capacitaciones[i].nombre + "</td><td>" + capacitaciones[i].capacitacion + "</td><td>" + capacitaciones[i].sector + "</td><td>" + capacitaciones[i].email + "</td><td><button class='btn btn-warning btn-sm' onclick='actualizarCapacitacion(" + i + ")'>Actualizar</button> <button class='btn btn-danger btn-sm' onclick='eliminarCapacitacion(" + i + ")'>Eliminar</button></td></tr>";
    tabla.innerHTML += fila;
  }
}

// Función para actualizar capacitación
function actualizarCapacitacion(index) {
  // Llenar el formulario con los datos de la capacitación seleccionada
  document.getElementById("fecha").value = capacitaciones[index].fecha;
  document.getElementById("apellido").value = capacitaciones[index].apellido;
  document.getElementById("nombre").value = capacitaciones[index].nombre;
  document.getElementById("capacitacion").value = capacitaciones[index].capacitacion;
  document.getElementById("sector").value = capacitaciones[index].sector;
  document.getElementById("email").value = capacitaciones[index].email;

  // Eliminar la capacitación seleccionada del array
  capacitaciones.splice(index, 1);

  // Actualizar la tabla con los datos actualizados
  actualizarTabla();
}


// Función para eliminar capacitación con SweetAlert
function eliminarCapacitacion(index) {
    // Mostrar un mensaje de confirmación personalizado con SweetAlert
    Swal.fire({
      title: '¿Estás seguro?',
      text: "Esta acción eliminará la capacitación. ¿Deseas continuar?",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        // Eliminar la capacitación seleccionada del array
        capacitaciones.splice(index, 1);
  
        // Actualizar la tabla después de eliminar
        actualizarTabla();
  
        // Mostrar una alerta de éxito con SweetAlert
        Swal.fire(
          'Eliminado',
          'La capacitación ha sido eliminada.',
          'success'
        );
      }
    });
  }
  