# Flujo de trabajo de traducción

El ejemplo utiliza catálogos de GNU gettext:

- `locale/messages.pot` es la plantilla con los textos extraídos del código fuente.
- `locale/<idioma>/LC_MESSAGES/messages.po` contiene las traducciones de un idioma.
- `messages.mo` es el catálogo compilado que utiliza la aplicación.

El formato gettext es compatible con muchas plataformas de traducción en línea, como [Crowdin](https://crowdin.com/) y [Transifex](https://www.transifex.com/). También puedes editar los archivos `.po` con programas específicos, como [Poedit](https://poedit.net/).

Para una explicación más detallada sobre cómo traducir aplicaciones con gettext, consulta la [guía de Lokalise](https://lokalise.com/blog/translating-apps-with-gettext-comprehensive-tutorial/). Es un enlace a una guía útil, no un anuncio.

El proyecto de ejemplo incluye tareas de [Poe the Poet](https://poethepoet.natn.io/) para automatizar los pasos repetitivos. Ejecútalas desde el directorio `example/`. Son especialmente útiles cuando la aplicación tiene varios idiomas: actualizan o compilan todos los catálogos existentes de una vez, sin repetir los comandos para cada idioma.

Antes de ejecutar las tareas, instala [GNU gettext](https://www.gnu.org/software/gettext/) y [Poe the Poet](https://poethepoet.natn.io/). Si aún no tienes Poe, instálalo así:

```console
uv tool install poethepoet
```

Estas son las definiciones de tareas de `example/pyproject.toml`:

```toml
[tool.poe.tasks]
run = "streamlit run app.py"
xgettext.shell = "xgettext -d messages -o ./locale/messages.pot *.py --from-code=UTF-8 --no-location"
msgfmt = "find ./locale -name \\*.po -execdir msgfmt messages.po -o messages.mo \\;"
msgmerge.shell = "find locale -name '*.po' -exec msgmerge -U {} locale/messages.pot \\; && find locale -name '*.po~' -delete"
```

`xgettext` reúne las cadenas de los archivos Python en una plantilla común. `msgmerge` actualiza todos los catálogos `.po` existentes con esa plantilla y elimina los archivos de copia de seguridad; `msgfmt` compila cada catálogo `.po` en un archivo `.mo`. Estos comandos forman parte de GNU gettext, mientras que Poe solo ejecuta las tareas configuradas.

## 1. Marca el texto que se debe traducir

Envuelve las cadenas visibles para el usuario con `gettext` (normalmente importado como `_`). Para las formas singular y plural, usa `ngettext`. Por ejemplo:

```python
st.write(_("Squirrel application"))
ngettext("One squirrel", "%(num)d squirrels", count)
```

## 2. Extrae las cadenas del código

Después de añadir o modificar cadenas traducibles, genera la plantilla de mensajes:

```console
poe xgettext
```

La tarea ejecuta `xgettext` sobre los archivos Python del directorio `example/` y actualiza `locale/messages.pot`.

## 3. Actualiza los catálogos y traduce

Combina la plantilla más reciente con todos los catálogos `.po` existentes:

```console
poe msgmerge
```

Abre cada archivo `locale/<idioma>/LC_MESSAGES/messages.po` y traduce los valores `msgstr`. No cambies marcadores como `%(num)d`. Para los mensajes en plural, traduce todas las formas `msgstr[n]` que requiera el idioma.

Al actualizar un catálogo, `msgmerge` puede marcar una entrada como `fuzzy` si el texto original ha cambiado, pero se parece al anterior. La traducción existente se conserva como sugerencia, aunque puede que ya no sea adecuada. Revísala y elimina la marca `fuzzy`: `msgfmt` omite estas entradas, por lo que la aplicación no podrá utilizarlas.

La tarea actualiza los catálogos existentes. Para añadir un idioma, primero crea su archivo `.po`.

## 4. Compila las traducciones y comprueba el resultado

Compila los catálogos traducidos en archivos `.mo`:

```console
poe msgfmt
```

Inicia el ejemplo y comprueba las traducciones en la aplicación:

```console
poe run
```

Cuando cambien las cadenas del código, vuelve a ejecutar `poe xgettext` y `poe msgmerge`, traduce las entradas nuevas o modificadas y compila de nuevo los catálogos.
