create database 4thewords_prueba_andres_gutierrez;

use 4thewords_prueba_andres_gutierrez;

DROP TABLE IF EXISTS leyendas;
DROP TABLE IF EXISTS distrito;
DROP TABLE IF EXISTS canton;
DROP TABLE IF EXISTS provincia;
DROP TABLE IF EXISTS categoria;

create table categoria(
	id int auto_increment primary key,
    nombre varchar(100) not null
);

create table provincia(
	id int auto_increment primary key,
    nombre varchar(100) not null
);

create table canton(
	id int auto_increment primary key,
    nombre varchar(100) not null,
    provincia INT NOT NULL,
    FOREIGN KEY (provincia) REFERENCES provincia(id) ON UPDATE CASCADE
);

create table distrito(
	id int auto_increment primary key,
    nombre varchar(100) not null,
    canton INT NOT NULL,
    FOREIGN KEY (canton) REFERENCES canton(id) ON UPDATE CASCADE
);

create table leyendas(
    id int auto_increment primary key,
    imagen varchar (500) not null,
    nombre varchar (100) not null,
    descripcion text not null,
    fecha_de_leyenda date not null,
    provincia int not null,
    canton int not null,
    distrito int not null,
    categoria int not null,
    FOREIGN KEY (provincia) REFERENCES provincia(id) ON UPDATE CASCADE,
    FOREIGN KEY (canton) REFERENCES canton(id) ON UPDATE CASCADE,
    FOREIGN KEY (distrito) REFERENCES distrito(id) ON UPDATE CASCADE,
    FOREIGN KEY (categoria) REFERENCES categoria(id) ON UPDATE CASCADE
);

INSERT INTO categoria (nombre) VALUES ('Terror');
INSERT INTO categoria (nombre) VALUES ('Historia');
INSERT INTO categoria (nombre) VALUES ('Cultura');
INSERT INTO categoria (nombre) VALUES ('Mitos');
INSERT INTO categoria (nombre) VALUES ('Religión');

INSERT INTO provincia (nombre) VALUES ('San José');
INSERT INTO provincia (nombre) VALUES ('Cartago');
INSERT INTO provincia (nombre) VALUES ('Alajuela');
INSERT INTO provincia (nombre) VALUES ('Heredia');
INSERT INTO provincia (nombre) VALUES ('Guanacaste');
INSERT INTO provincia (nombre) VALUES ('Puntarenas');
INSERT INTO provincia (nombre) VALUES ('Limón');


INSERT INTO canton (nombre, provincia) VALUES ('Central', 1);
INSERT INTO canton (nombre, provincia) VALUES ('Paraíso', 2);
INSERT INTO canton (nombre, provincia) VALUES ('Desamparados', 1);
INSERT INTO canton (nombre, provincia) VALUES ('Grecia', 3);
INSERT INTO canton (nombre, provincia) VALUES ('Central', 2);
INSERT INTO canton (nombre, provincia) VALUES ('Central', 4);
INSERT INTO canton (nombre, provincia) VALUES ('Santa Cruz', 5);
INSERT INTO canton (nombre, provincia) VALUES ('Central', 6);
INSERT INTO canton (nombre, provincia) VALUES ('Pococí', 7);


INSERT INTO distrito (nombre, canton) VALUES ('Catedral', 1);
INSERT INTO distrito (nombre, canton) VALUES ('Dulce Nombre', 2);
INSERT INTO distrito (nombre, canton) VALUES ('San Rafael Abajo', 3);
INSERT INTO distrito (nombre, canton) VALUES ('San Roque', 4);
INSERT INTO distrito (nombre, canton) VALUES ('Oriental', 5);
INSERT INTO distrito (nombre, canton) VALUES ('San Francisco', 6);
INSERT INTO distrito (nombre, canton) VALUES ('Santa Cruz', 7);
INSERT INTO distrito (nombre, canton) VALUES ('Barranca', 8);
INSERT INTO distrito (nombre, canton) VALUES ('Cariari', 9);


INSERT INTO leyendas (imagen, nombre, descripcion, fecha_de_leyenda, provincia, canton, distrito, categoria)
VALUES ('/imagenes/elCadejoImagen.jpg', 'El Cadejo', 'Un perro espectral que protege a los viajeros nocturnos o castiga a los malvados.', '1917-12-25', 1, 1, 1, 1);

INSERT INTO leyendas (imagen, nombre, descripcion, fecha_de_leyenda, provincia, canton, distrito, categoria)
VALUES ('/imagenes/padreImagen.jpg', 'El Padre sin Cabeza', 'Un sacerdote decapitado que aparece en noches de tormenta.', '1955-04-09', 2, 2, 2, 1);

INSERT INTO leyendas (imagen, nombre, descripcion, fecha_de_leyenda, provincia, canton, distrito, categoria)
VALUES ('/imagenes/procesionImagen.jpg', 'La Procesión de los Muertos', 'Una procesión espectral que vaga por los caminos en la medianoche.', '1927-08-14', 1, 3, 3, 1);

INSERT INTO leyendas (imagen, nombre, descripcion, fecha_de_leyenda, provincia, canton, distrito, categoria)
VALUES ('/imagenes/lloronaImagen.jpg', 'La Llorona', 'El espíritu de una mujer que llora por sus hijos perdidos cerca de los ríos.', '1875-11-11', 3, 4, 4, 1);

INSERT INTO leyendas (imagen, nombre, descripcion, fecha_de_leyenda, provincia, canton, distrito, categoria)
VALUES ('/imagenes/ceguaImagen.jpg', 'La Cegua', 'Una hermosa mujer que se transforma en un monstruo para asustar a los hombres.', '1902-10-25', 2, 5, 5, 1);

INSERT INTO leyendas (imagen, nombre, descripcion, fecha_de_leyenda, provincia, canton, distrito, categoria)
VALUES ('/imagenes/carretaImagen.jpg', 'La Carreta sin Bueyes', 'Una carreta fantasmal que anuncia desgracias.', '1700-12-05', 4, 6, 6, 1);

INSERT INTO leyendas (imagen, nombre, descripcion, fecha_de_leyenda, provincia, canton, distrito, categoria)
VALUES ('/imagenes/esquipulasImagen.jpg', 'Santo Cristo de Esquipulas', 'La historia del Cristo Negro y sus milagros en Santa Cruz.', '1899-01-14', 5, 7, 7, 5);

INSERT INTO leyendas (imagen, nombre, descripcion, fecha_de_leyenda, provincia, canton, distrito, categoria)
VALUES ('/imagenes/virgenImagen.jpg', 'Virgen de los Ángeles', 'La aparición de la Virgen en Cartago y su representación milagrosa.', '1850-02-09', 2, 2, 2, 5);

INSERT INTO leyendas (imagen, nombre, descripcion, fecha_de_leyenda, provincia, canton, distrito, categoria)
VALUES ('/imagenes/pozoImagen.jpg', 'El Pozo de la Llorona', 'Un pozo donde se dice que la Llorona aparece para buscar a sus hijos.', '1950-06-23', 5, 7, 7, 1);

INSERT INTO leyendas (imagen, nombre, descripcion, fecha_de_leyenda, provincia, canton, distrito, categoria)
VALUES ('/imagenes/portonImagen.jpg', 'El Portón Negro', 'Un portón encantado que se abre y cierra solo para asustar a los transeúntes.', '1977-03-13', 6, 8, 8, 1);

