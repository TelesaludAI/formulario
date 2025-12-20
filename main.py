#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 22:15:17 2025

@author: pedronarvaezrosado
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ["DATABASE_URL"]

def get_connection():
    return psycopg2.connect(
        DATABASE_URL,
        cursor_factory=RealDictCursor
    )


from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel, EmailStr
import traceback

#from db import get_connection

app = FastAPI()

# 🔐 CORS (obligatorio para Anvil)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 API KEY
API_KEY = "clave_secreta_larga"


class FormData(BaseModel):
    id: str
    fecha: date
    municipio: str
    nombre: str
    cedula: int

    barrio: Optional[str] = None
    lider: Optional[str] = None
    correo: Optional[EmailStr] = None
    celular: Optional[int] = None
    fecha_cumpleanos: Optional[date] = None
    cargo: Optional[str] = None
    profesion: Optional[str] = None

    useremail: EmailStr
    fecha_registro: date
    hora_registro: time

    referenciado_por: Optional[str] = None
    sector: Optional[str] = None
    punto_votacion: Optional[str] = None
    mesa_votacion: Optional[int] = None
    lat_lon: Optional[str] = None
    etapa_campana: Optional[str] = None
    confirmacion_voto: Optional[str] = None


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.post("/formulario")
def guardar_formulario(
    data: FormData,
    x_api_key: str = Header(...)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API KEY inválida")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO registros_personas (
                id,
                fecha,
                municipio,
                nombre,
                cedula,
                barrio,
                lider,
                correo,
                celular,
                fecha_cumpleanos,
                cargo,
                profesion,
                useremail,
                fecha_registro,
                hora_registro,
                referenciado_por,
                sector,
                punto_votacion,
                mesa_votacion,
                lat_lon,
                etapa_campana,
                confirmacion_voto
            )
            VALUES (
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,
                %s,%s
            )
            """,
            (
                data.id,
                data.fecha,
                data.municipio,
                data.nombre,
                data.cedula,
                data.barrio,
                data.lider,
                data.correo,
                data.celular,
                data.fecha_cumpleanos,
                data.cargo,
                data.profesion,
                data.useremail,
                data.fecha_registro,
                data.hora_registro,
                data.referenciado_por,
                data.sector,
                data.punto_votacion,
                data.mesa_votacion,
                data.lat_lon,
                data.etapa_campana,
                data.confirmacion_voto
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        return {"ok": True}

    except Exception as e:
        print("ERROR EN /formulario")
        print(str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
