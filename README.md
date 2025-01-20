# Leyendas Ticas - Backend

**Leyendas Ticas** es una API desarrollada con **FastAPI** que permite la gestion de leyendas costarricenses, este backend ofrece endpoints para la creacion, edicion, eliminacion y filtrado de leyendas, asi como la gestion de categorias, provincias, cantones y distritos.

---

## Caracteristicas

- **CRUD Completo:** Crear, leer, actualizar y eliminar leyendas.
- **Filtros Avanzados:** Filtrar leyendas por provincia, canton, distrito y categoria.
- **Conversion de Fechas:** Convierte fechas en valores relativos como "hace 2 años".

---

## Tecnologias Utilizadas

- **FastAPI:** Framework para construir APIs rapidas y eficientes.
- **SQLModel:** ORM para gestion de base de datos.
- **Uvicorn:** Servidor ASGI para ejecutar la aplicacion.

---

## Requisitos Previos

Antes de comenzar, asegurese de tener instalado lo siguiente:

1. **Python 3.10+**
2. **Git**: Para clonar el repositorio.

## Verifique que estan instalados ejecutando estos comandos en la terminal
python --version
git --version

## Se procede a clonar el repositorio con el siguinte comando
git clone https://github.com/Andres-GC-David/4thewords_backend_andres_gutierrez.git

## Una vez clonado se debe de pasar al directorio del proyecto
cd 4thewords_backend_andres_gutierrez

## En el directorio se deben de instalar las dependencias con el siguiente comando
pip install -r requirements.txt


## Se debe de copiar e ingresar la informacion del archivo .env
cp .env.example .env


## Para ejecutar el proyecto se debe de ejecutar el archivo run.py para asegurarse que FastAPI use el puerti 8080
Se puede ingresar este comando: python run.py
O bien buscar el archivo que se encuentra en la raiz y darle a ejecutar
