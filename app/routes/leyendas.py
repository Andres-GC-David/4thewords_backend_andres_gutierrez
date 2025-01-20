import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
from sqlmodel import Session, select
from app.database.connection import get_db
from app.models.models import Leyenda, Categoria, Provincia, Canton, Distrito
from fastapi.responses import FileResponse
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from typing import Optional, List
from fastapi import Query

router = APIRouter()
IMAGENES_DIR = os.path.join(os.path.dirname(__file__), "../../imagenes")

@router.get("/leyendas")
def obtener_leyendas(db: Session = Depends(get_db)):
    leyendas = db.exec(select(Leyenda)).all()
    if not leyendas:
        raise HTTPException(status_code=404, detail="Leyendas no encontradas")
    
    leyendas_con_fechas = []
    for leyenda in leyendas:
        leyenda_dict = leyenda.dict()
        fecha_de_leyenda = leyenda.fecha_de_leyenda
        fecha_actual = date.today()
        diferencia = relativedelta(fecha_actual, fecha_de_leyenda)

        if diferencia.years > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.years} años"
        elif diferencia.months > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.months} meses"
        elif diferencia.days > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.days} días"
        else:
            leyenda_dict["fecha_de_leyenda"] = "hoy"

        leyenda_dict["provincia"] = db.get(Provincia, leyenda.provincia).nombre
        leyenda_dict["canton"] = db.get(Canton, leyenda.canton).nombre
        leyenda_dict["distrito"] = db.get(Distrito, leyenda.distrito).nombre
        leyenda_dict["categoria"] = db.get(Categoria, leyenda.categoria).nombre

        leyendas_con_fechas.append(leyenda_dict)

    return leyendas_con_fechas

@router.get("/leyendas/filtrar")
def filtrar_leyendas(nombre: Optional[str] = None, provincias: Optional[List[int]] = Query(None), cantones: Optional[List[int]] = Query(None), distritos: Optional[List[int]] = Query(None), categorias: Optional[List[int]] = Query(None), db: Session = Depends(get_db),):
    query = db.query(Leyenda)
    if nombre:
        query = query.filter(Leyenda.nombre.ilike(f"%{nombre}%"))

    if provincias:
        query = query.filter(Leyenda.provincia.in_(provincias))

    if cantones:
        query = query.filter(Leyenda.canton.in_(cantones))

    if distritos:
        query = query.filter(Leyenda.distrito.in_(distritos))

    if categorias:
        query = query.filter(Leyenda.categoria.in_(categorias))

    leyendas = query.all()

    if not leyendas:
        raise HTTPException(
            status_code=404, detail="No se encontraron leyendas con los filtros aplicados."
        )

    return leyendas

@router.get("/leyendas/{leyenda_id}")
def obtener_leyenda(leyenda_id: int, db: Session = Depends(get_db)):
    leyenda = db.get(Leyenda, leyenda_id)  
    if not leyenda:
        raise HTTPException(status_code=404, detail="Leyenda no encontrada")

    leyenda_dict = leyenda.dict()
    fecha_de_leyenda = leyenda.fecha_de_leyenda
    fecha_actual = date.today()
    diferencia = relativedelta(fecha_actual, fecha_de_leyenda)

    if diferencia.years > 0:
        leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.years} años"
    elif diferencia.months > 0:
        leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.months} meses"
    elif diferencia.days > 0:
        leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.days} días"
    else:
        leyenda_dict["fecha_de_leyenda"] = "hoy"

    leyenda_dict["provincia"] = db.get(Provincia, leyenda.provincia).nombre
    leyenda_dict["canton"] = db.get(Canton, leyenda.canton).nombre
    leyenda_dict["distrito"] = db.get(Distrito, leyenda.distrito).nombre
    leyenda_dict["categoria"] = db.get(Categoria, leyenda.categoria).nombre

    return leyenda_dict

@router.get("/leyendasEdicion/{leyenda_id}")
def obtener_leyenda_edicion(leyenda_id: int, db: Session = Depends(get_db)):
    leyenda = db.get(Leyenda, leyenda_id)
    if not leyenda:
        raise HTTPException(status_code=404, detail="Leyenda no encontrada")
    return leyenda

@router.post("/leyendas")
async def crear_leyenda(
    imagen: UploadFile = Form(...),
    nombre: str = Form(...),
    descripcion: str = Form(...),
    fecha_de_leyenda: date = Form(...),
    categoria: int = Form(...),
    provincia: int = Form(...),
    canton: int = Form(...),
    distrito: int = Form(...),
    db: Session = Depends(get_db)
    ):
    
    if not db.get(Categoria, categoria):
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    if not db.get(Provincia, provincia):
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    
    if not db.get(Canton, canton):
        raise HTTPException(status_code=404, detail="Cantón no encontrado")
    
    if not db.get(Distrito, distrito):
        raise HTTPException(status_code=404, detail="Distrito no encontrado")
    
    if imagen.filename == "":
        raise HTTPException(status_code=400, detail="No se proporcionó una imagen")
    
    if imagen.content_type not in ["image/jpeg", "image/jpg, image/png, image/gif, image/webp"]:
        raise HTTPException(status_code=400, detail="Formato de imagen no válido")
    
    if nombre and len(nombre) > 100:
        raise HTTPException(status_code=400, detail="El nombre de la leyenda no puede tener más de 100 caracteres")
    
    if fecha_de_leyenda and fecha_de_leyenda > date.today():    
        raise HTTPException(status_code=400, detail="La fecha de la leyenda no puede ser mayor a la fecha actual")
    
    imagen_path = os.path.join(IMAGENES_DIR, imagen.filename)
    with open(imagen_path, "wb") as buffer:
        buffer.write(await imagen.read())
    
    nueva_leyenda = Leyenda(
        imagen=f"/imagenes/{imagen.filename}",
        nombre=nombre,
        descripcion=descripcion,
        fecha_de_leyenda=fecha_de_leyenda,
        categoria=categoria,
        provincia=provincia,
        canton=canton,
        distrito=distrito
    )
    db.add(nueva_leyenda)
    db.commit()
    db.refresh(nueva_leyenda)
    return nueva_leyenda

@router.put("/leyendas/{leyenda_id}")
def actualizar_leyenda(leyenda_id: int, leyenda: Leyenda, db: Session = Depends(get_db)):
    leyenda_db = db.get(Leyenda, leyenda_id)
    if not leyenda_db:
        raise HTTPException(status_code=404, detail="Leyenda no encontrada")
    
    if not db.get(Categoria, leyenda.categoria):
        raise HTTPException(status_code=404, detail="Categoriia no encontrada")
    
    if not db.get(Provincia, leyenda.provincia):
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    
    if not db.get(Canton, leyenda.canton):
        raise HTTPException(status_code=404, detail="Canton no encontrado")
    
    if not db.get(Distrito, leyenda.distrito):
        raise HTTPException(status_code=404, detail="Distrito no encontrado")
    
    if leyenda.nombre and len(leyenda.nombre) > 100:
        raise HTTPException(status_code=400, detail="El nombre de la leyenda no puede tener más de 100 caracteres")
    
    if leyenda.fecha_de_leyenda:
        if isinstance(leyenda.fecha_de_leyenda, str):
            try:
                leyenda.fecha_de_leyenda = datetime.strptime(leyenda.fecha_de_leyenda, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de fecha inválido")
        if leyenda.fecha_de_leyenda > date.today():
            raise HTTPException(status_code=400, detail="La fecha de la leyenda no puede ser mayor a la fecha actual")
    
    nueva_leyenda = leyenda.dict(exclude_unset=True)
    
    if not nueva_leyenda:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")
    
    nueva_leyenda.pop("imagen", None)
    
    for key, value in nueva_leyenda.items():
        setattr(leyenda_db, key, value)
    db.add(leyenda_db)
    db.commit()
    db.refresh(leyenda_db)
    return leyenda_db

@router.delete("/leyendas/{leyenda_id}")    
def eliminar_leyenda(leyenda_id: int, db: Session = Depends(get_db)):
    leyenda_db = db.get(Leyenda, leyenda_id)
    if not leyenda_db:
        raise HTTPException(status_code=404, detail="Leyenda no encontrada")
    
    imagen_path = os.path.join(IMAGENES_DIR, os.path.basename(leyenda_db.imagen))
    if os.path.exists(imagen_path):
        os.remove(imagen_path)
    
    db.delete(leyenda_db)
    db.commit()
    return {"message": "Leyenda eliminada"}

@router.get("/provincias")
def obtener_provincias(db: Session = Depends(get_db)):
    provincias = db.query(Provincia).all()
    if not provincias:
        raise HTTPException(status_code=404, detail="Provincias no encontradas")
    return provincias

@router.get("/categorias")
def obtener_categorias(db: Session = Depends(get_db)):
    categorias = db.query(Categoria).all()
    if not categorias:
        raise HTTPException(status_code=404, detail="Categorias no encontradas")
    return categorias

@router.get("/cantones")
def obtener_cantones(db: Session = Depends(get_db)):
    cantones = db.query(Canton).all()
    if not cantones:
        raise HTTPException(status_code=404, detail="Cantones no encontrados")
    return cantones

@router.get("/provincias/{provincia_id}/cantones")
def obtener_cantones(provincia_id: int, db: Session = Depends(get_db)):
    cantones = db.query(Canton).filter(Canton.provincia == provincia_id).all()
    if not cantones:
        raise HTTPException(status_code=404, detail="No se encontraron Cantones asociados a esta Provincia")
    return cantones

@router.get("/distritos")
def obtener_distritos(db: Session = Depends(get_db)):
    distritos = db.query(Distrito).all()
    if not distritos:
        raise HTTPException(status_code=404, detail="Distritos no encontrados")
    return distritos

@router.get("/cantones/{canton_id}/distritos")
def obtener_distritos(canton_id: int, db: Session = Depends(get_db)):
    distritos = db.query(Distrito).filter(Distrito.canton == canton_id).all()
    if not distritos:
        raise HTTPException(status_code=404, detail="No se encontraron Distritos asociados a este Canton")
    return distritos

@router.get("/leyendas/provincias/{provincia_id}")
def obtener_leyendas_por_provincia(provincia_id: int, db: Session = Depends(get_db)):
    leyendas = db.query(Leyenda).filter(Leyenda.provincia == provincia_id).all()
    if not leyendas:
        raise HTTPException(status_code=404, detail="No se encontraron leyendas asociadas a esta Provincia")
    
    leyendas_en_provincias = []
    for leyenda in leyendas:
        leyenda_dict = leyenda.dict()
        fecha_de_leyenda = leyenda.fecha_de_leyenda
        fecha_actual = date.today()
        diferencia = relativedelta(fecha_actual, fecha_de_leyenda)

        if diferencia.years > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.years} años"
        elif diferencia.months > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.months} meses"
        elif diferencia.days > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.days} días"
        else:
            leyenda_dict["fecha_de_leyenda"] = "hoy"

        leyenda_dict["provincia"] = db.get(Provincia, leyenda.provincia).nombre
        leyenda_dict["canton"] = db.get(Canton, leyenda.canton).nombre
        leyenda_dict["distrito"] = db.get(Distrito, leyenda.distrito).nombre
        leyenda_dict["categoria"] = db.get(Categoria, leyenda.categoria).nombre

        leyendas_en_provincias.append(leyenda_dict)

    return leyendas_en_provincias


@router.get("/leyendas/cantones/{canton_id}/provincias/{provincia_id}")    
def obtener_leyendas_por_canton(canton_id: int, provincia_id: int, db: Session = Depends(get_db)):
    leyendas = db.query(Leyenda).filter(Leyenda.canton == canton_id, Leyenda.provincia == provincia_id).all()
    if not leyendas:
        raise HTTPException(status_code=404, detail="No se encontraron leyendas asociadas a este Cantón")

    leyendas_en_cantones = []
    for leyenda in leyendas:
        leyenda_dict = leyenda.dict()
        fecha_de_leyenda = leyenda.fecha_de_leyenda
        fecha_actual = date.today()
        diferencia = relativedelta(fecha_actual, fecha_de_leyenda)

        if diferencia.years > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.years} años"
        elif diferencia.months > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.months} meses"
        elif diferencia.days > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.days} días"
        else:
            leyenda_dict["fecha_de_leyenda"] = "hoy"

        leyenda_dict["provincia"] = db.get(Provincia, leyenda.provincia).nombre
        leyenda_dict["canton"] = db.get(Canton, leyenda.canton).nombre
        leyenda_dict["distrito"] = db.get(Distrito, leyenda.distrito).nombre
        leyenda_dict["categoria"] = db.get(Categoria, leyenda.categoria).nombre

        leyendas_en_cantones.append(leyenda_dict)

    return leyendas_en_cantones

@router.get("/leyendas/distritos/{distrito_id}/cantones/{canton_id}")    
def obtener_leyendas_por_distrito(distrito_id: int, canton_id: int, db: Session = Depends(get_db)):
    leyendas = db.query(Leyenda).filter(Leyenda.distrito == distrito_id, Leyenda.canton == canton_id).all()
    if not leyendas:
        raise HTTPException(status_code=404, detail="No se encontraron leyendas asociadas a este Distrito y Cantón")
    
    leyendas_en_distritos = []
    for leyenda in leyendas:
        leyenda_dict = leyenda.dict()
        fecha_de_leyenda = leyenda.fecha_de_leyenda
        fecha_actual = date.today()
        diferencia = relativedelta(fecha_actual, fecha_de_leyenda)

        if diferencia.years > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.years} años"
        elif diferencia.months > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.months} meses"
        elif diferencia.days > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.days} días"
        else:
            leyenda_dict["fecha_de_leyenda"] = "hoy"

        leyenda_dict["provincia"] = db.get(Provincia, leyenda.provincia).nombre
        leyenda_dict["canton"] = db.get(Canton, leyenda.canton).nombre
        leyenda_dict["distrito"] = db.get(Distrito, leyenda.distrito).nombre
        leyenda_dict["categoria"] = db.get(Categoria, leyenda.categoria).nombre

        leyendas_en_distritos.append(leyenda_dict)

    return leyendas_en_distritos


@router.get("/leyendas/categorias/{categoria_id}")
def obtener_leyendas_por_categoria(categoria_id: int, db: Session = Depends(get_db)):
    leyendas = db.query(Leyenda).filter(
        Leyenda.categoria == categoria_id).all()
    if not leyendas:
        raise HTTPException(
            status_code=404, detail="No se encontraron leyendas asociadas a esta Categoria")

    leyendas_en_categorias = []
    for leyenda in leyendas:
        leyenda_dict = leyenda.dict()
        fecha_de_leyenda = leyenda.fecha_de_leyenda
        fecha_actual = date.today()
        diferencia = relativedelta(fecha_actual, fecha_de_leyenda)

        if diferencia.years > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.years} años"
        elif diferencia.months > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.months} meses"
        elif diferencia.days > 0:
            leyenda_dict["fecha_de_leyenda"] = f"hace {diferencia.days} días"
        else:
            leyenda_dict["fecha_de_leyenda"] = "hoy"

        leyenda_dict["provincia"] = db.get(Provincia, leyenda.provincia).nombre
        leyenda_dict["canton"] = db.get(Canton, leyenda.canton).nombre
        leyenda_dict["distrito"] = db.get(Distrito, leyenda.distrito).nombre
        leyenda_dict["categoria"] = db.get(Categoria, leyenda.categoria).nombre

        leyendas_en_categorias.append(leyenda_dict)

    return leyendas_en_categorias