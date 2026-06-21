# HANDOFF — estado del proyecto y cómo continuar

> Documento para retomar el trabajo desde otro equipo/sesión. Última actualización: 2026-06-21.

## Qué es esto

Repo de **apuntes de TIC** que se publica como sitio **MkDocs Material** en GitHub Pages:
**https://igorparrabastias.github.io/tic-cursos-apuntes/**

El deploy es automático: cada `push` a `master` dispara `.github/workflows/deploy.yml`
(instala `mkdocs-material mkdocs-callouts mkdocs-jupyter`, hace `mkdocs build` y publica con Pages).

Dos piezas principales:
1. **El documento "Fundamentos del PLN y la IA (1950–hoy)"**, dividido en una **serie de 4 páginas**.
2. **El curso de Python**: ~260 notebooks `.ipynb` integrados al sitio con botón "Abrir en Colab".

## Estado actual (hecho y publicado ✅)

- Documento PLN/IA reescrito, compactado y **partido en serie de 4 páginas** + landing.
- Era LLM ampliada con secciones nuevas (cómo funcionan hoy, agentes, infra/chips, multimodalidad, evaluación) + página nueva de investigación/futuro.
- Notebooks del curso integrados y renderizados en el sitio, con botón Colab, sin tocar los `.ipynb`.
- Índices que navegan (anclas estilo MkDocs verificadas, 0 rotas). Fórmulas en ASCII (sin LaTeX). Iconos por nivel (🏠👾📌) y chistes en callouts.
- Todo verificado en vivo (HTTP 200). Último commit relevante: `45d020a`.

## Arquitectura del build del documento (IMPORTANTE)

El documento **no se edita a mano** en `pages/`. Se **genera** desde `_revision/`:

```
_revision/
  src/00..08-*.md      # secciones ORIGINALES (antes de reescribir)
  out/00..13-*.md       # secciones FUENTE actuales (esto es lo que se edita)
  assemble.js           # ensambla out/*.md -> las páginas en pages/
  gen-headers.js        # genera ilustraciones IA -> pages/assets/img/
  ORIGINAL.md           # respaldo del doc monolítico original
```

### Cómo regenerar las páginas del doc
```bash
cd _revision
node assemble.js          # reescribe pages/fundamento-*.md y pages/fundamentos-*.md
```
`assemble.js` define:
- `PARTS`: qué secciones `out/*.md` van en cada una de las 4 páginas.
- `MID`/`END`: chistes (callouts `> [!TIP]`) por sección.
- `MEDIA`: imágenes y diagramas SVG por sección.
- `addIcons`/`buildTOC`/`slug`: iconos por nivel e índice con anclas idénticas a las de MkDocs.

**Las 4 páginas generadas** (en `pages/`):
- `fundamento-del-pln-y-la-ia.md` — landing (intro + línea de tiempo + enlaces a las 4 partes)
- `fundamentos-1-origenes.md` — 1950–1979
- `fundamentos-2-estadistica-redes.md` — 1980–2000s
- `fundamentos-3-era-llm.md` — 2013–2026 (incluye LLM hoy, agentes, infra/chips, multimodal/eval)
- `fundamentos-4-investigacion-futuro.md` — investigación reciente y futuro

El `nav` de estas páginas está en `mkdocs.yml`.

## Integración de los notebooks (`nb_hook.py`)

Un único hook de MkDocs (`nb_hook.py`, referenciado en `mkdocs.yml` bajo `hooks:`):
1. Copia `notebook/` → `pages/notebook/` (gitignored) en cada build para que `mkdocs-jupyter` los descubra.
2. Descarta automáticamente notebooks vacíos/corruptos (hay 3 en `arboles/`: `arbol-de-decision`, `arbol-de-van-emde-boas`, `arbol-de-merkle`).
3. Arma la sección de navegación "Notebooks (ejecutables)" agrupada por carpeta.
4. Inyecta el botón **"Abrir en Colab"** (+ "Ver en GitHub") arriba de cada notebook.

No hay que editar ningún `.ipynb`. La fuente real de los notebooks es `notebook/` (raíz del repo).

## Imágenes

Generadas por `_revision/gen-headers.js` con la API de OpenAI, modelo **`gpt-image-1-mini`** (el barato — usar SIEMPRE ese).
- Estilo acordado: **vaporwave / Blade Runner**, figurativo y reconocible (personas, computadoras, robots). El texto en la imagen no importa.
- Lección aprendida: las imágenes malas anteriores fueron por **prompts abstractos**, no por el modelo. El prompt actual en `gen-headers.js` (`LOOK` + sujeto figurativo) sí funciona.
- Probar estilo barato: `node gen-headers.js test` (3 imágenes). Generar todo: `node gen-headers.js`.
- Requiere `OPENAI_API_KEY` en el entorno. En el PC original está en `/media/nomikos/home/dev/env-openclaw` (NO está en el repo; cada equipo usa su propia clave): `set -a && . env-openclaw && set +a`.

## Build y previsualización local

```bash
pip install mkdocs-material mkdocs-callouts mkdocs-jupyter
mkdocs build --site-dir _site      # build completo (4 págs + ~260 notebooks, ~30s)
mkdocs serve                        # previsualización en http://127.0.0.1:8000
```
`mkdocs.yml` usa `use_directory_urls: false` (URLs `.html` planas) para que las rutas relativas de `<img>` resuelvan igual en local, GitHub y Pages.

## Pendiente / decisiones abiertas

1. **Imágenes**: actualmente hay una MEZCLA — la mayoría son del estilo viejo y solo 3 (1950, 1990, 2018) son Blade Runner (pruebas). Falta decidir si **regenerar todas** al estilo Blade Runner (`node gen-headers.js`, ~$0.7–0.9 con la Mini) para unificar. El usuario dijo "olvida las imágenes" de momento.
2. **3 notebooks corruptos** en `arboles/` están vacíos (0 bytes): regenerarlos o eliminarlos.

## Reglas de trabajo con este usuario (Igor)

- Prefiere implementaciones **robustas** y que se **confirme el objetivo** antes de editar mucho.
- Muy sensible al **gasto**: en imágenes, usar siempre el modelo más barato y mostrar un test antes de generar lotes.
- Quiere que el doc sea **divertido de leer** (chistes visibles, imágenes con sentido).
- No matar servicios que esté usando sin avisar.
