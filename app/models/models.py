from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Categoria(Base):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    leyendas = relationship("Leyenda", back_populates="categoria_relacion")


class Provincia(Base):
    __tablename__ = 'provincia'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    cantones = relationship("Canton", back_populates="provincia_relacion")


class Canton(Base):
    __tablename__ = 'canton'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    provincia_id = Column(Integer, ForeignKey('provincia.id'), nullable=False)
    distritos = relationship("Distrito", back_populates="canton_relacion")
    provincia_relacion = relationship("Provincia", back_populates="cantones")


class Distrito(Base):
    __tablename__ = 'distrito'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    canton_id = Column(Integer, ForeignKey('canton.id'), nullable=False)
    canton_relacion = relationship("Canton", back_populates="distritos")


class Leyenda(Base):
    __tablename__ = 'leyendas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    imagen = Column(String(500), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_de_leyenda = Column(Date, nullable=False)
    categoria = Column(Integer, ForeignKey('categoria.id'), nullable=False)
    provincia = Column(Integer, ForeignKey('provincia.id'), nullable=False)
    canton = Column(Integer, ForeignKey('canton.id'), nullable=False)
    distrito = Column(Integer, ForeignKey('distrito.id'), nullable=False)
    categoria_relacion = relationship("Categoria", back_populates="leyendas")
    provincia_relacion = relationship("Provincia")
    canton_relacion = relationship("Canton")
    distrito_relacion = relationship("Distrito")
