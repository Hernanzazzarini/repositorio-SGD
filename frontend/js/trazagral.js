function consultarPorLote() {
    // Mostrar la sección de datos del lote
    document.querySelector(".datos-lote").style.display = "block";
}

function limpiarFormulario() {
    // Limpiar el formulario y ocultar los datos
    document.getElementById("consultaForm").reset();
    document.querySelector(".datos-lote").style.display = "none";
}

function exportarExcel() {
    // Lógica para exportar a Excel (puedes agregar la funcionalidad necesaria aquí)
    alert("Exportando a Excel...");
}

function imprimir() {
    // Lógica para imprimir (puedes agregar la funcionalidad necesaria aquí)
    alert("Imprimiendo...");
}
