function validarRegistro() {
    var apellido = document.getElementById("apellido").value;
    var nombre = document.getElementById("nombre").value;
    var email = document.getElementById("email").value;
    // Add more variables for other input fields

    var mensajeApellido = document.getElementById("mensajeApellido");
    var mensajeNombre = document.getElementById("mensajeNombre");
    var mensajeEmail = document.getElementById("mensajeEmail");
    // Add more variables for other error message elements

    var mensajeValidacion = document.getElementById("mensajeValidacion");
    var exitoMensaje = document.getElementById("exitoMensaje");

    // Limpiar todos los mensajes de validación
    mensajeApellido.innerHTML = "";
    mensajeNombre.innerHTML = "";
    mensajeEmail.innerHTML = "";
    // Clear messages for other fields
    mensajeValidacion.innerHTML = "";
    exitoMensaje.style.display = "none";

    // Verificar si los campos están vacíos y mostrar mensajes debajo de cada label
    if (apellido.trim() === "") {
        mensajeApellido.innerHTML = "Por favor, complete este campo.";
    }

    if (nombre.trim() === "") {
        mensajeNombre.innerHTML = "Por favor, complete este campo.";
    }

    if (email.trim() === "") {
        mensajeEmail.innerHTML = "Por favor, complete este campo.";
    }

    // Puedes agregar más validaciones según tus requisitos, por ejemplo, validar el formato del correo electrónico
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email) && email.trim() !== "") {
        mensajeEmail.innerHTML = "Ingrese un correo electrónico válido.";
    }

    // Add more validation logic for other fields

    // Si hay algún mensaje de validación, detener el proceso y mostrar el mensaje general
    if (
        mensajeApellido.innerHTML !== "" ||
        mensajeNombre.innerHTML !== "" ||
        mensajeEmail.innerHTML !== ""
        // Add more conditions for other fields
    ) {
        return;
    }

    // Mostrar el mensaje de éxito
    exitoMensaje.innerHTML = "Registro exitoso, Formulario enviado.";
    exitoMensaje.style.display = "block";
}
