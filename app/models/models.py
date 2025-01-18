from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional   
from datetime import date

class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    leyendas: List["Leyenda"] = Relationship(back_populates="categoria_relacion")   


class Provincia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    cantones: List["Canton"] = Relationship(back_populates="provincia_relacion")

class Canton(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    provincia: int = Field(foreign_key="provincia.id")
    distritos: List["Distrito"] = Relationship(back_populates="canton_relacion")
    provincia_relacion: "Provincia" = Relationship(back_populates="cantones")
    
class Distrito(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    canton: int = Field(foreign_key="canton.id")
    canton_relacion: "Canton" = Relationship(back_populates="distritos")


class Leyenda(SQLModel, table=True):
    __tablename__ = "leyendas"
    id: Optional[int] = Field(default=None, primary_key=True)
    imagen: str = Field(max_length=500)
    nombre: str = Field(max_length=100)
    descripcion: str
    fecha_de_leyenda: date
    categoria: int = Field(foreign_key="categoria.id")
    provincia: int = Field(foreign_key="provincia.id")
    canton: int = Field(foreign_key="canton.id")
    distrito: int = Field(foreign_key="distrito.id")
    categoria_relacion: Categoria = Relationship(back_populates="leyendas")
    provincia_relacion: Provincia = Relationship()
    canton_relacion: Canton = Relationship()
    distrito_relacion: Distrito = Relationship()
