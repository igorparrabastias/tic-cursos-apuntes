"""
Hook de MkDocs que integra TODOS los notebooks de notebook/ sin tocarlos:

  1. on_config  -> copia notebook/ dentro de pages/notebook/ (gitignored) para
                   que mkdocs-jupyter los descubra y renderice, y arma la
                   navegación lateral "Notebooks (ejecutables)" agrupada por
                   carpeta (sin listarlos a mano en mkdocs.yml).
  2. on_page_content -> inyecta el botón "Abrir en Colab" arriba de cada
                   notebook renderizado. Cero ediciones dentro de los .ipynb.

Las URLs de Colab/GitHub apuntan a notebook/<...> en master (su ubicación real
en el repo); la copia en pages/ es solo para el build y no se commitea.
"""
import os
import json
import glob
import shutil

REPO = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(REPO, "notebook")
DST = os.path.join(REPO, "pages", "notebook")
GH = "igorparrabastias/tic-cursos-apuntes"
BRANCH = "master"


def _titulo(slug):
    return slug.replace("-", " ").replace("_", " ").strip().capitalize()


def on_config(config):
    # Copia fresca de los notebooks dentro de docs_dir para que mkdocs-jupyter
    # los descubra (solo escanea docs_dir). pages/notebook/ está en .gitignore.
    if os.path.isdir(DST):
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)

    # Descarta notebooks vacíos o con JSON inválido (romperían mkdocs-jupyter).
    descartados = []
    for p in glob.glob(os.path.join(DST, "**", "*.ipynb"), recursive=True):
        try:
            with open(p, encoding="utf-8") as fh:
                json.load(fh)
        except Exception:
            os.remove(p)
            descartados.append(os.path.relpath(p, DST))
    if descartados:
        print("nb_hook: notebooks omitidos (vacíos/corruptos): " + ", ".join(descartados))

    # Navegación agrupada por carpeta de primer nivel.
    grupos = {}
    for p in sorted(glob.glob(os.path.join(DST, "**", "*.ipynb"), recursive=True)):
        uri = os.path.relpath(p, os.path.join(REPO, "pages")).replace(os.sep, "/")
        partes = uri.split("/")          # notebook / carpeta / [...] / archivo.ipynb
        carpeta = partes[1] if len(partes) > 2 else "(raíz)"
        nombre = os.path.splitext(partes[-1])[0]
        grupos.setdefault(carpeta, []).append({_titulo(nombre): uri})

    seccion = [{_titulo(c): grupos[c]} for c in sorted(grupos)]
    if seccion:
        config["nav"].append({"Notebooks (ejecutables)": seccion})
    return config


def on_page_content(html, page, config, files):
    src = page.file.src_uri
    if not src.endswith(".ipynb"):
        return html
    # src es 'notebook/<...>.ipynb' (o 'demo/slicing.ipynb'); ambos existen en master.
    colab = f"https://colab.research.google.com/github/{GH}/blob/{BRANCH}/{src}"
    github = f"https://github.com/{GH}/blob/{BRANCH}/{src}"
    boton = (
        '<p>'
        f'<a class="md-button md-button--primary" target="_blank" href="{colab}">'
        '▶ Abrir en Colab</a> '
        f'<a class="md-button" target="_blank" href="{github}">Ver en GitHub</a>'
        '</p>'
    )
    return boton + html
