USE dbolega;
CREATE TABLE IF NOT EXISTS personal (
  id_legajo INT AUTO_INCREMENT PRIMARY KEY,
  apellido VARCHAR(50)NOT NULL,
  nombre VARCHAR(50)NOT NULL,
  email VARCHAR(100)NOT NULL,
  id_sector INT NOT NULL,
  FOREIGN KEY (id_sector) REFERENCES sector(id_sector)
);

CREATE TABLE IF NOT EXISTS sector (
  id_sector INT AUTO_INCREMENT PRIMARY KEY,  
  sector VARCHAR(50)NOT NULL
);  
CREATE TABLE IF NOT EXISTS capacitaciones (
  id_capacitacion INT AUTO_INCREMENT PRIMARY KEY,
  nombre_capacitacion VARCHAR(100)NOT NULL
);

CREATE TABLE IF NOT EXISTS personal_capacitaciones (
  id_legajo INT NOT NULL,
  id_capacitacion INT NOT NULL,
  fecha_tomada DATE NOT NULL,
  PRIMARY KEY (id_legajo, id_capacitacion),
  FOREIGN KEY (id_legajo) REFERENCES personal(id_legajo),
  FOREIGN KEY (id_capacitacion) REFERENCES capacitaciones(id_capacitacion)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,  
    nombre_completo VARCHAR(100),
    correo_electronico VARCHAR(100)
   
);
CREATE TABLE tareas (
    id_tarea INT AUTO_INCREMENT PRIMARY KEY,
    tarea VARCHAR(255),
    fecha_vencimiento DATE,
    estado VARCHAR(50),
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Tabla para Calibres
CREATE TABLE IF NOT EXISTS calibres (
    id_calibre INT AUTO_INCREMENT PRIMARY KEY,
    nombre_calibre VARCHAR(255) -- Cambié el nombre de la columna para hacerla más descriptiva
);

-- Tabla para Segregación
CREATE TABLE IF NOT EXISTS segregacion (
    id_segregacion INT AUTO_INCREMENT PRIMARY KEY,
    tipo_segregacion VARCHAR(255), -- Cambié el nombre de la columna para hacerla más descriptiva
    descripcion_segregacion VARCHAR(255) -- Añadí "descripcion_" para hacer el nombre más claro
);

-- Tabla para Transportes
CREATE TABLE IF NOT EXISTS transportes (
    id_transporte INT AUTO_INCREMENT PRIMARY KEY,
    nombre_transporte VARCHAR(255), -- Cambié el nombre de la columna para hacerla más descriptiva
    telefono_transporte VARCHAR(30),
    email_transporte VARCHAR(100),
    localidad_transporte VARCHAR(100),
    nombre_chofer VARCHAR(255), -- Cambié el nombre de la columna para hacerla más descriptiva
    codigo_postal VARCHAR(255)
   
);

-- Tabla para Cargas
CREATE TABLE IF NOT EXISTS cargas (
    id_carga INT AUTO_INCREMENT PRIMARY KEY,
    lote VARCHAR(255),
    fecha_carga DATE,
    cantidad INT,
    kilos_transporte DECIMAL(10, 2),
	destino VARCHAR(255),
    id_transporte INT,
    FOREIGN KEY (id_transporte) REFERENCES transportes(id_transporte)
);

-- Tabla para Producción
CREATE TABLE IF NOT EXISTS produccion (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_calibre INT,
    id_segregacion INT,
    lote VARCHAR(255),
    fecha_inicio DATE,
    hora_inicio TIME,
    fecha_final DATE,
    hora_final TIME,
    envases VARCHAR(255),
    kilos DECIMAL(10, 2),
    deposito VARCHAR(255),
    rack VARCHAR(255),
    stock INT,
    reclamo VARCHAR(255),
    FOREIGN KEY (id_calibre) REFERENCES calibres(id_calibre),
    FOREIGN KEY (id_segregacion) REFERENCES segregacion(id_segregacion)
   
);
-- Tabla intermedia para relacionar Producción con Cargas
CREATE TABLE IF NOT EXISTS produccion_cargas (
    id_produccion_carga INT AUTO_INCREMENT PRIMARY KEY,
    id_produccion INT,
    id_carga INT,
    FOREIGN KEY (id_produccion) REFERENCES produccion(id_registro),
    FOREIGN KEY (id_carga) REFERENCES cargas(id_carga)
);






