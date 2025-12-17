#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 22:15:17 2025

@author: pedronarvaezrosado
"""

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import psycopg2
import os

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # en producción puedes limitarlo
    allow_methods=["*"],        # INCLUYE OPTIONS
    allow_headers=["*"],        # INCLUYE X-API-KEY
)

DATABASE_URL = os.environ["DATABASE_URL"]
API_KEY = os.environ["API_KEY"]

class FormData(BaseModel):
    nombre: str
    correo: str | None = None
    celular: str | None = None
    mensaje: str | None = None

@app.post("/formulario")
def guardar_formulario(
    data: FormData,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO formularios (nombre, correo, celular, mensaje)
            VALUES (%s, %s, %s, %s)
        """, (data.nombre, data.correo, data.celular, data.mensaje))
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
