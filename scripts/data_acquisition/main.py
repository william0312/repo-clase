#!/usr/bin/env python3
"""Adquisición de datos del proyecto Rock al Parque (TDSP, fase 1).

Descarga las versiones congeladas del corpus desde Google Drive, verifica su
integridad con SHA-256 y deja los datos listos para el análisis.

Uso:
    python scripts/data_acquisition/main.py --data-dir data/raw
    python scripts/data_acquisition/main.py --data-dir data/raw --solo corpus_completo
    python scripts/data_acquisition/main.py --data-dir data/raw --resumen

Requiere: pandas, openpyxl y gdown (pip install gdown openpyxl pandas).
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

ARCHIVOS: dict[str, dict] = {
    "corpus_completo": {
        "id": "1wAh0zboUuq1AQ_-A7NVvWN8X5h1A-rbH",
        "archivo": "dataframe_df.xlsx",
        "sha256": "e0075809db4894bd5c6557b4d8de30c979b86428e5042c96cb026119634bc55d",
        "descripcion": "Corpus completo de comentarios de YouTube (2023-2025)",
    },
    "corpus_etiquetado": {
        "id": "1Xe9XxJW93jfWweA9qXQwHlZYdJQFY4L7",
        "archivo": "Con_etiqueta.xlsx",
        "sha256": "68c543f762a188bca7210a83a5d437701749183b1c7f42e0b79c907fe0e8d54d",
        "descripcion": "Muestra etiquetada manualmente (P/NEU/N)",
    },
    "corpus_sin_etiqueta": {
        "id": "1BLCuOk0lnWqnVmhGolS4PFaVqqB2KJp6",
        "archivo": "Sin_etiqueta.xlsx",
        "sha256": "98160918dadbf3867e12c4c2d15198cb954448c3a90a45687b74e4f83476a151",
        "descripcion": "Comentarios sin etiqueta humana",
    },
    "tass_2020": {
        "id": "1TKa9fcyz4Lt511h14c6Avt_BEsNYfZsC",
        "archivo": "Task1-train-dev.zip",
        "sha256": "359388d8108b79bd35b02ed5b4cb442935e5e87c992e3db0db5f19af189e99bf",
        "descripcion": "Corpus TASS 2020 (train/dev, TSV por país)",
        "descomprimir_en": "tass",
    },
}


def sha256_archivo(ruta: Path) -> str:
    """Devuelve el SHA-256 de un archivo, leído por bloques."""
    h = hashlib.sha256()
    with ruta.open("rb") as f:
        for bloque in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloque)
    return h.hexdigest()


def descargar(file_id: str, destino: Path) -> None:
    """Descarga un archivo de Google Drive verificando el tamaño final."""
    try:
        import gdown
    except ImportError:
        sys.exit(
            "Falta gdown. Instálalo con: pip install gdown\n"
            "Alternativa: descarga manual desde Google Drive y coloca el archivo en "
            f"{destino}"
        )

    destino.parent.mkdir(parents=True, exist_ok=True)
    gdown.download(f"https://drive.google.com/uc?id={file_id}", str(destino), quiet=False)
    if not destino.exists() or destino.stat().st_size == 0:
        sys.exit(f"No se pudo descargar {destino.name}. Revisa la cuota de Drive o el enlace.")


def descomprimir(archivo: Path, destino: Path) -> None:
    """Descomprime un ZIP dentro de `destino` si aún no tiene contenido."""
    if destino.exists() and any(destino.iterdir()):
        return
    destino.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archivo) as z:
        z.extractall(destino)


def obtener(nombre: str, data_dir: Path, forzar: bool = False) -> Path:
    """Garantiza que un insumo exista en disco; lo descarga si falta."""
    meta = ARCHIVOS[nombre]
    ruta = data_dir / meta["archivo"]

    if forzar or not ruta.exists():
        print(f"[descarga] {nombre}: {meta['descripcion']}")
        descargar(meta["id"], ruta)
    else:
        print(f"[ok] {ruta.name} ya está disponible")

    esperado = meta.get("sha256")
    if esperado:
        obtenido = sha256_archivo(ruta)
        estado = "OK" if obtenido == esperado else "NO COINCIDE"
        print(f"  sha256 {estado}: {obtenido}")
        if obtenido != esperado:
            sys.exit(
                f"El archivo {ruta.name} no coincide con la versión congelada. "
                "Bórralo y vuelve a descargarlo."
            )

    if meta.get("descomprimir_en"):
        descomprimir(ruta, data_dir / meta["descomprimir_en"])

    return ruta


def cargar_tass(data_dir: Path):
    """Consolida los TSV de TASS 2020 en un DataFrame (id, texto, polaridad, split, pais)."""
    import pandas as pd

    base = data_dir / "tass"
    registros = []
    for tsv in sorted(base.glob("*/*.tsv")):
        df = pd.read_csv(
            tsv, sep="\t", header=None, names=["id", "texto", "polaridad"],
            dtype={"id": str}, encoding="utf-8",
        )
        df["split"] = tsv.parent.name
        df["pais"] = tsv.stem
        registros.append(df)

    if not registros:
        sys.exit(f"No se encontraron TSV de TASS en {base}")
    return pd.concat(registros, ignore_index=True)


def resumen(data_dir: Path) -> None:
    """Imprime dimensiones y distribución de los corpus cargados."""
    import pandas as pd

    completo = pd.read_excel(data_dir / "dataframe_df.xlsx")
    etiquetado = pd.read_excel(data_dir / "Con_etiqueta.xlsx")
    tass = cargar_tass(data_dir)

    print("\n=== Corpus completo ===")
    print(f"Filas: {len(completo)} | Columnas: {completo.shape[1]}")
    print("Por edición:")
    print(completo["Año_Edición"].value_counts().sort_index().to_string())

    print("\n=== Muestra etiquetada ===")
    print(f"Filas: {len(etiquetado)}")
    print(etiquetado["categoria"].value_counts().to_string())

    print("\n=== TASS 2020 ===")
    print(f"Filas: {len(tass)}")
    print(tass["polaridad"].value_counts().to_string())


def main() -> None:
    parser = argparse.ArgumentParser(description="Descarga y verifica los corpus del proyecto.")
    parser.add_argument("--data-dir", default="data/raw", type=Path,
                        help="Directorio destino de los datos (por defecto: data/raw)")
    parser.add_argument("--solo", nargs="*", choices=list(ARCHIVOS),
                        help="Descargar únicamente estos insumos")
    parser.add_argument("--forzar", action="store_true",
                        help="Volver a descargar aunque el archivo exista")
    parser.add_argument("--resumen", action="store_true",
                        help="Cargar los corpus e imprimir un resumen")
    args = parser.parse_args()

    args.data_dir.mkdir(parents=True, exist_ok=True)
    seleccion = args.solo or list(ARCHIVOS)

    for nombre in seleccion:
        obtener(nombre, args.data_dir, forzar=args.forzar)

    print(f"\nDatos disponibles en: {args.data_dir.resolve()}")
    if args.resumen:
        resumen(args.data_dir)


if __name__ == "__main__":
    main()
