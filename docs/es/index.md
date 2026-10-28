# Documentación de streamlit-gettext

`streamlit-gettext` es una extensión para Streamlit que facilita la localización de aplicaciones. La biblioteca tiene en cuenta las preferencias de idioma del navegador y muestra al usuario la traducción correspondiente.

El proyecto sigue en desarrollo, por lo que la documentación y las funciones disponibles pueden cambiar.

## ¿Qué permite hacer?

- **Traducir texto.** Marca las cadenas que quieras traducir con `gettext`, que normalmente se importa con el nombre corto `_`.
- **Gestionar el singular y el plural.** Usa `ngettext` para elegir la forma adecuada del mensaje según la cantidad.
- **Elegir el idioma.** La biblioteca puede tener en cuenta las preferencias de idioma del navegador.

## Ejemplo sencillo

Así se usan las funciones de traducción en una aplicación de Streamlit:

```python
import streamlit as st
from i18n import gettext as _
from i18n import ngettext

st.write(_("Some text"))

squirrels = st.slider(_("How many squirrels to show?"), 1, 100, 1)

st.write(
    ngettext(
        "There's %(num)d squirrel:",
        "There're %(num)d squirrels:",
        squirrels,
    )
    % {"num": squirrels},
)

st.write("🐿️" * squirrels)
```

La llamada `_()` marca el texto que se traducirá. `ngettext()` elige la forma del mensaje según el número de ardillas, y el control deslizante permite cambiar esa cantidad.

Este es solo un ejemplo de código, no una guía completa de configuración. Para ejecutar una aplicación localizada también se necesitan los archivos de traducción y la configuración del proyecto.

## Cambiar el idioma manualmente

En esta versión, el usuario elige el idioma en un menú. La selección se pasa a `set_preferred_languages()` para que la aplicación muestre la traducción correspondiente:

```python
import streamlit as st
from i18n import get_available_languages, ngettext, set_preferred_languages
from i18n import gettext as _

language = st.segmented_control(
    "Language",
    options=get_available_languages(),
    label_visibility="collapsed",
    required=True,
)
if language:
    set_preferred_languages([language])

st.write(_("Some text"))

squirrels = st.slider(_("How many squirrels to show?"), 1, 100, 1)

st.write(
    ngettext(
        "There's %(num)d squirrel:",
        "There're %(num)d squirrels:",
        squirrels,
    )
    % {"num": squirrels},
)

st.write("🐿️" * squirrels)
```

## Probar la aplicación

Comprueba cómo funciona en la [aplicación de demostración en Streamlit](https://st-gettext-example.streamlit.app/).

El código fuente está disponible en el [directorio del ejemplo](https://github.com/insolor/streamlit-gettext/tree/main/example).

## Referencia de la API

Consulta la [referencia de la API](api.md) para ver la descripción de las funciones y otras interfaces de la biblioteca.
