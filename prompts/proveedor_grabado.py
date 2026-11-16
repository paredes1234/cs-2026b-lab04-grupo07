"""Proveedor de promptfoo que NO llama a ningún modelo: devuelve la respuesta grabada."""
import os
import pathlib

def _carpeta(options):
    nombre = ((options or {}).get("config") or {}).get("carpeta", "grabaciones")
    candidatos = [
        pathlib.Path.cwd() / nombre,
        pathlib.Path(__file__).parent / "criterios" / nombre,
    ]
    for c in candidatos:
        if c.is_dir():
            return c
    return candidatos[0]

def call_api(prompt, options, context):
    contexto = context or {}
    
    # Obtener id_caso (ej. "H1")
    id_caso = (contexto.get("vars") or {}).get("id")
    if not id_caso:
        return {"error": "No se pudo determinar el id del caso"}
        
    # Limpiar la versión extraña que manda Promptfoo
    prompt_obj = contexto.get("prompt") or {}
    raw_version = str(prompt_obj.get("label") or prompt_obj.get("id") or "v1")
    version = raw_version.split("://")[-1].split(":")[0].replace(".txt", "").strip()
    
    carpeta_base = _carpeta(options)
    
    # Rutas candidatas
    ruta_con_version = carpeta_base / version / f"{id_caso}.txt"
    ruta_sin_version = carpeta_base / f"{id_caso}.txt"
    
    # Intentar leer cualquiera de las dos
    if ruta_con_version.is_file():
        return {"output": ruta_con_version.read_text(encoding="utf-8-sig")}
    elif ruta_sin_version.is_file():
        return {"output": ruta_sin_version.read_text(encoding="utf-8-sig")}
    else:
        # Si falla, devuelve un error detallado mostrando exactamente dónde buscó
        return {
            "error": f"Faltan los TXT. Por favor ponlos en:\n1) {ruta_con_version}\n o en \n2) {ruta_sin_version}"
        }