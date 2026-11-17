# Inicio rápido

Crea una pequeña aplicación con textos originales en inglés, traducciones al español, un selector de idioma y mensajes con contexto y formas plurales.

## 1. Instala las herramientas

Usa Python 3.11 o posterior. En una terminal, crea un proyecto e instala los paquetes de Python:

```sh
mkdir localized-app
cd localized-app
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit streamlit-gettext poethepoet
```

Estos comandos usan Bash en Linux o macOS. En Windows, sigue toda la guía dentro de WSL, incluida la configuración del entorno virtual, para que `poe` y las tareas de shell usen el mismo entorno Linux.

Instala GNU gettext por separado; proporciona `xgettext` y `msgfmt`. Por ejemplo, en Ubuntu o Debian:

```sh
sudo apt-get install gettext
```

En macOS con Homebrew:

```sh
brew install gettext
```

Para otros sistemas, consulta las [instrucciones de instalación de GNU gettext](https://www.gnu.org/software/gettext/). Ejecuta los demás comandos desde `localized-app/` con el entorno virtual activado.

## 2. Crea el módulo de traducción

Guarda el siguiente código como `i18n.py`, junto a `app.py`. Este módulo pertenece a tu aplicación; la biblioteca no lo instala.

```python
from pathlib import Path

from streamlit_gettext import GettextWrapper

wrapper = GettextWrapper(Path(__file__).parent / "locale")

gettext = wrapper.gettext
ngettext = wrapper.ngettext
pgettext = wrapper.pgettext
npgettext = wrapper.npgettext
get_available_languages = wrapper.get_available_languages
set_preferred_languages = wrapper.set_preferred_languages
```

La ruta del catálogo es relativa a `i18n.py`, por lo que no depende del directorio de trabajo. El dominio predeterminado es `messages`, correspondiente a `messages.po` y `messages.mo`.

## 3. Crea la aplicación

Guarda este código como `app.py`:

```python
import streamlit as st
from i18n import (
    get_available_languages,
    ngettext,
    npgettext,
    pgettext,
    set_preferred_languages,
)
from i18n import gettext as _

language = st.selectbox(
    "Language",
    options=["auto", *get_available_languages()],
    format_func=lambda code: "Browser language" if code == "auto" else code,
)
set_preferred_languages(None if language == "auto" else [language])

st.title(_("File manager"))
count = st.slider(_("Number of files"), 1, 30, 1)
st.write(ngettext("%(num)d file", "%(num)d files", count) % {"num": count})

st.button(pgettext("action", "Open"))
st.write(pgettext("state", "Open"))
st.write(
    npgettext(
        "download",
        "Download %(num)d file",
        "Download %(num)d files",
        count,
    )
    % {"num": count}
)
```

`gettext` traduce un mensaje. `ngettext` elige una forma plural. `pgettext` distingue la acción «Open» del estado «Open» mediante el argumento de contexto. `npgettext` combina el contexto con la selección de plural.

Selecciona `auto` para usar el idioma del navegador, o un código de idioma para sustituirlo. Pasar `None` restaura la detección del navegador. La selección manual se guarda por separado para cada sesión de Streamlit. Los textos originales de este ejemplo están en inglés, de modo que `en` usa los mensajes originales si no hay catálogo inglés.

## 4. Extrae y traduce los mensajes

Crea `pyproject.toml` en la raíz del proyecto con estas tareas, o añade la sección a un archivo existente:

```toml
[tool.poe.tasks]
extract_pot = """
xgettext
    --keyword=pgettext:1c,2
    --keyword=npgettext:1c,2,3
    --no-location
    --output=locale/messages.pot
    app.py
"""

[tool.poe.tasks.update_po]
shell = """
find locale -type f -name '*.po' -exec sh -c '
    for po do
        msgmerge --update --backup=none "$po" locale/messages.pot || exit
    done
' sh {} +
"""

[tool.poe.tasks.compile_mo]
shell = """
find locale -type f -name '*.po' -exec sh -c '
    for po do
        msgfmt --check-format "$po" -o "${po%.po}.mo" || exit
    done
' sh {} +
"""

[tool.poe.tasks.init_po]
shell = """
mkdir -p "locale/${language}/LC_MESSAGES" &&
msginit --input=locale/messages.pot --output-file="locale/${language}/LC_MESSAGES/messages.po" --locale="${language}" --no-translator
"""
args = [{ name = "language", positional = true, required = true }]
```

[Poe the Poet](https://poethepoet.natn.io/) ejecuta los comandos guardados en este archivo. Las opciones se escriben una sola vez; después basta con nombres de tareas cortos. GNU gettext sigue requiriendo una instalación independiente.

`xgettext` detecta Python por la extensión `.py`, respeta la codificación del código Python y reconoce `_`, `gettext` y `ngettext` de forma predeterminada. Las llamadas con contexto necesitan las opciones adicionales `--keyword`.

Opciones de extracción:

| Opción | Función |
|---|---|
| `--keyword=pgettext:1c,2` | El argumento 1 es el contexto (`c`); el 2 es el mensaje. |
| `--keyword=npgettext:1c,2,3` | El argumento 1 es el contexto; el 2 y el 3 son los mensajes singular y plural. |
| `--no-location` | Omitir las ubicaciones del código fuente para reducir los cambios al mover código. |
| `--output=locale/messages.pot` | Escribir la plantilla compartida de mensajes en este archivo. |
| `app.py` | Archivo fuente que se analiza; añade otros archivos a medida que crezca la aplicación. |

`init_po` acepta un argumento posicional obligatorio con el idioma. Crea `locale/<language>/LC_MESSAGES` y pasa el idioma a `msginit`. Ejecuta `poe init_po es` para español o `poe init_po ja` para japonés; no necesitas modificar las tareas al añadir idiomas.

`update_po` y `compile_mo` usan `find` para procesar todos los archivos `.po` de `locale/`. La primera actualiza los catálogos desde la plantilla compartida sin copias de seguridad; la segunda comprueba los marcadores de formato y crea un `.mo` junto a cada `.po`. `${po%.po}` elimina el sufijo `.po` antes de añadir `.mo`. `for po do` procesa las rutas que pasa `find`, y `|| exit` propaga cualquier error de gettext. Con `-exec … +`, `find` también devuelve un error si falla un lote, lo que permite detectarlo en Poe y CI. Las rutas están entre comillas para admitir directorios con espacios.

Estas tareas requieren un shell POSIX y `find`, disponibles en Linux y macOS. En Windows, sigue la guía dentro de WSL.

Crea el directorio común de catálogos y extrae los mensajes:

```sh
mkdir -p locale
poe extract_pot
```

Crea el archivo `.po` a partir de la plantilla:

```sh
poe init_po es
```

Esta tarea ejecuta `msginit`: `--input` selecciona la plantilla, `--output-file` el nuevo catálogo, `--locale=es` el idioma y `--no-translator` desactiva las preguntas interactivas sobre el traductor. El comando crea entradas con traducciones vacías e inicializa la cabecera, incluidos `Language` y `Plural-Forms`.

Ejecuta `poe init_po <language>` una vez por idioma nuevo. Las siguientes ejecuciones de `poe update_po` y `poe compile_mo` procesarán todos los idiomas añadidos.

Puedes completar las traducciones con un editor especializado como [Poedit](https://poedit.com/), que ofrece una interfaz para mensajes y formas plurales. Muchos servicios en línea, incluidos [Crowdin](https://support.crowdin.com/developer/configuration-file/#gettext-project) y [Transifex](https://help.transifex.com/en/articles/6220794-gettext-po), admiten `.po` de forma nativa, sin convertirlo a otro formato.

Puedes configurar una integración con el repositorio para enviar los mensajes originales actualizados y recibir las traducciones, por ejemplo mediante la [integración de Crowdin con GitHub](https://support.crowdin.com/github-integration/) o la [integración de Transifex con GitHub](https://help.transifex.com/en/articles/6265125-github-installation-and-configuration). Tras recibir los `.po` actualizados, ejecuta `poe compile_mo` para que la aplicación utilice las nuevas traducciones.

Abre `locale/es/LC_MESSAGES/messages.po` y rellena `msgstr` y `msgstr[n]`. En la cabecera de metadatos (`msgid ""`), establece UTF-8 como codificación y guarda el archivo con esa codificación:

```po
"Content-Type: text/plain; charset=UTF-8\n"
```

Conserva los demás campos generados de la cabecera, incluido `Plural-Forms`. Las entradas traducidas deberían quedar así:

```po
msgid "File manager"
msgstr "Administrador de archivos"

msgid "Number of files"
msgstr "Número de archivos"

#, python-format
msgid "%(num)d file"
msgid_plural "%(num)d files"
msgstr[0] "%(num)d archivo"
msgstr[1] "%(num)d archivos"

msgctxt "action"
msgid "Open"
msgstr "Abrir"

msgctxt "state"
msgid "Open"
msgstr "Abierto"

#, python-format
msgctxt "download"
msgid "Download %(num)d file"
msgid_plural "Download %(num)d files"
msgstr[0] "Descargar %(num)d archivo"
msgstr[1] "Descargar %(num)d archivos"
```

`.pot` es la plantilla extraída, `.po` la traducción editable y `.mo` el catálogo compilado que carga la aplicación. `msgctxt` debe coincidir con el contexto de la llamada Python. Mantén `%(num)d` sin cambios y traduce todas las formas plurales necesarias para el idioma. El español tiene dos; otros idiomas pueden requerir otro número y otra expresión `Plural-Forms`.

## 5. Compila y ejecuta

```sh
poe compile_mo
```

Ahora el proyecto tiene esta estructura:

```text
localized-app/
├── app.py
├── i18n.py
├── pyproject.toml
└── locale/
    ├── messages.pot
    └── es/
        └── LC_MESSAGES/
            ├── messages.po
            └── messages.mo
```

Inicia la aplicación:

```sh
python -m streamlit run app.py
```

Selecciona `es`: el título debería cambiar a «Administrador de archivos». Coloca el control deslizante en 1, 2 y 5 para ver «1 archivo», «2 archivos» y «5 archivos». El botón muestra «Abrir» y el estado «Abierto». Selecciona `en` para volver al texto inglés, o `auto` para usar el idioma del navegador.

Si un mensaje sigue en inglés, comprueba el idioma seleccionado, la ubicación del catálogo, el dominio y si se recompiló el `.mo` después de editar el `.po`. `msgfmt` omite las entradas marcadas como `fuzzy`: revisa la traducción y elimina la marca antes de compilar. Reinicia Streamlit después de recompilar para vaciar la caché de traducciones.

## Mantén las traducciones actualizadas

Después de cambiar los mensajes originales, vuelve a extraerlos y actualiza los catálogos:

```sh
poe extract_pot
poe update_po
```

Traduce las entradas nuevas o modificadas, revisa las marcas `fuzzy`, ejecuta `poe compile_mo` y reinicia la aplicación. Consulta el [flujo de traducción](translation_workflow.md) para las tareas del ejemplo del repositorio, o la [referencia de la API](api.md) para las interfaces de la biblioteca.
