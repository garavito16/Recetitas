from flask import flash
from recetitas.config.mysqlconnection import connectToMySQL
import re

NAME_REGEX = re.compile(r'^[a-zA-Z ]{3,50}$')
DESCRIPCION_REGEX = re.compile(r'^[a-zA-Z ]{3,200}$')
INSTRUCTIONS_REGEX = re.compile(r'^[a-zA-Z ]{3,2000}$')
FECHA_REGEX = re.compile(r'^[1-2]{1}[9|0|1]{1}[0-9]{2}[-][0-1]{1}[0-9]{1}[-][0-3]{1}[0-9]{1}$')

class Receta:
    name_db = "db_recetitas"
    def __init__(self,id,nombre,tiempo,descripcion,instrucciones,fecha,usuario_id,creador,created_at):
        self.id = id
        self.nombre = nombre
        self.tiempo = tiempo
        self.descripcion = descripcion
        self.instrucciones = instrucciones
        self.fecha = fecha
        self.usuario_id = usuario_id
        self.creador = creador
        self.created_at = created_at

    @classmethod
    def getAllReceta(cls):
        query = '''
                    select re.*, (CASE WHEN (re.tiempo = 'Y') THEN 'YES' ELSE 'NO' END) AS tiempito,CONCAT(us.first_name," ",us.last_name) AS usuario from recetas re
                    INNER JOIN usuarios us ON us.id = re.usuario_id
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query)
        recetas = []
        for aux in resultado:
            receta = Receta(aux["id"],aux["nombre"],aux["tiempito"],aux["descripcion"],aux["instrucciones"],aux["fecha"],aux["usuario_id"],aux["usuario"],aux["created_at"])
            recetas.append(receta)
        return recetas

    @classmethod
    def getRecetaXid(cls,data):
        query = '''
                    select re.*, (CASE WHEN (re.tiempo = 'Y') THEN 'YES' ELSE 'NO' END) AS tiempito, CONCAT(us.first_name," ",us.last_name) AS usuario from recetas re
                    INNER JOIN usuarios us ON us.id = re.usuario_id
                    where re.id = %(id)s
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        if(len(resultado)>0):
            receta = Receta(resultado[0]["id"],resultado[0]["nombre"],resultado[0]["tiempito"],resultado[0]["descripcion"],resultado[0]["instrucciones"],resultado[0]["fecha"],resultado[0]["usuario_id"],resultado[0]["usuario"],resultado[0]["created_at"])
            return receta
        return None

    @classmethod
    def addReceta(cls,receta):
        query = '''
                    INSERT INTO recetas (nombre,tiempo,descripcion,instrucciones,fecha,usuario_id,created_at)
                    VALUES (%(nombre)s,%(tiempo)s,%(descripcion)s,%(instrucciones)s,%(fecha)s,%(usuario_id)s,now())
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,receta)
        return resultado

    @classmethod
    def updateReceta(cls,receta):
        query = '''
                    UPDATE recetas SET nombre = %(nombre)s,tiempo=%(tiempo)s,descripcion=%(descripcion)s,
                    instrucciones=%(instrucciones)s,fecha=%(fecha)s,updated_at = now()
                    WHERE id = %(id)s
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,receta)
        return resultado

    @classmethod
    def deleteReceta(cls,receta):
        query = '''
                    DELETE FROM recetas WHERE id = %(id)s
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,receta)
        return resultado

    @classmethod
    def verifyData(cls,data):
        is_valid = True
        if not NAME_REGEX.match(data["nombre"]):
            is_valid=False
            flash("El nombre de la receta debe tener mas de 3 caracteres","receta")
        if not DESCRIPCION_REGEX.match(data["descripcion"]):
            is_valid=False
            flash("La descripcion de la receta debe tener mas de 3 caracteres","receta")
        if not INSTRUCTIONS_REGEX.match(data["instrucciones"]):
            is_valid=False
            flash("Las instrucciones de la receta debe tener mas de 3 caracteres","receta")
        if not FECHA_REGEX.match(data["fecha"]):
            is_valid=False
            flash("La fecha de la receta es incorrecta","receta")
        return is_valid