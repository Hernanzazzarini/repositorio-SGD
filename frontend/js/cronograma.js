function agregarTarea() {
    var tarea = document.getElementById('tarea').value;
    var fechaVencimiento = document.getElementById('fechaVencimiento').value;
    var responsable = document.getElementById('responsable').value;
    var estado = document.getElementById('estado').value;

    var fila = `<tr>
                    <td>${Date.now()}</td>
                    <td>${tarea}</td>
                    <td>${fechaVencimiento}</td>
                    <td>${responsable}</td>
                    <td>${estado}</td>
                    <td>
                        <button type="button" class="btn btn-info btn-sm" onclick="actualizarTarea(this)">Actualizar</button>
                        <button type="button" class="btn btn-danger btn-sm" onclick="eliminarTarea(this)">Eliminar</button>
                    </td>
                </tr>`;

    document.getElementById('listaTareas').innerHTML += fila;
    document.getElementById('formularioTarea').reset();
}

function actualizarTarea(btn) {
    var fila = btn.parentNode.parentNode;
    var tarea = fila.cells[1].textContent;
    var fechaVencimiento = fila.cells[2].textContent;
    var responsable = fila.cells[3].textContent;
    var estado = fila.cells[4].textContent;

    document.getElementById('tarea').value = tarea;
    document.getElementById('fechaVencimiento').value = fechaVencimiento;
    document.getElementById('responsable').value = responsable;
    document.getElementById('estado').value = estado;

    // Cambia el botón "Agregar Tarea" a "Guardar Cambios"
    var botonAgregar = document.querySelector('#formularioTarea button');
    botonAgregar.textContent = 'Guardar Cambios';

    // Cambia la función del botón a "guardarCambiosTarea"
    botonAgregar.onclick = function () {
        guardarCambiosTarea(fila);
    };
}

function guardarCambiosTarea(fila) {
    var tarea = document.getElementById('tarea').value;
    var fechaVencimiento = document.getElementById('fechaVencimiento').value;
    var responsable = document.getElementById('responsable').value;
    var estado = document.getElementById('estado').value;

    // Actualiza los valores de la fila
    fila.cells[1].textContent = tarea;
    fila.cells[2].textContent = fechaVencimiento;
    fila.cells[3].textContent = responsable;
    fila.cells[4].textContent = estado;

    // Restaura el botón y su función original
    var botonAgregar = document.querySelector('#formularioTarea button');
    botonAgregar.textContent = 'Agregar Tarea';
    botonAgregar.onclick = agregarTarea;

    // Limpiar los inputs después de actualizar la tarea
    document.getElementById('formularioTarea').reset();
}

function eliminarTarea(btn) {
    var fila = btn.parentNode.parentNode;
    fila.parentNode.removeChild(fila);

}




document.addEventListener("DOMContentLoaded", function () {
    // Obtener la fecha actual
    var fechaActual = new Date();
  
    // Formatear la fecha según lo deseado (puedes personalizar este formato)
    var fechaFormateada = fechaActual.toLocaleDateString('es', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
  
    // Actualizar el contenido del elemento con id "fechahoy"
    document.getElementById("fechahoy").textContent = "Fecha de hoy: " + fechaFormateada;
  });
  