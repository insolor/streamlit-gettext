# streamlit-gettext-Dokumentation

`streamlit-gettext` ist eine Erweiterung für Streamlit, mit der sich Anwendungen leichter lokalisieren lassen. Die Bibliothek berücksichtigt die Spracheinstellungen des Browsers und zeigt die passende Übersetzung an.

Das Projekt befindet sich noch in der Entwicklung. Die Dokumentation und die verfügbaren Funktionen können sich daher ändern.

## Was kann die Bibliothek?

- **Texte übersetzen.** Markiere zu übersetzende Zeichenketten mit `gettext`, das üblicherweise unter dem Kurznamen `_` importiert wird.
- **Einzahl und Mehrzahl behandeln.** Mit `ngettext` wird abhängig von der Anzahl die passende Nachrichtenform ausgewählt.
- **Sprache auswählen.** Die Bibliothek kann die Spracheinstellungen des Browsers berücksichtigen.

## Einfaches Beispiel

So verwendest du die Übersetzungsfunktionen in einer Streamlit-Anwendung:

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

Der Aufruf `_()` kennzeichnet Text, der übersetzt werden soll. `ngettext()` wählt je nach Anzahl der Eichhörnchen die passende Nachrichtenform aus. Mit dem Schieberegler lässt sich die Anzahl ändern.

Dies ist nur ein Codebeispiel und keine vollständige Einrichtungsanleitung. Für eine lokalisierte Anwendung werden zusätzlich Übersetzungsdateien und eine Projektkonfiguration benötigt.

## Sprache manuell wechseln

In dieser Variante wählt der Benutzer die Sprache selbst über ein Menü aus. Die Auswahl wird an `set_preferred_languages()` übergeben, damit die Anwendung die entsprechende Übersetzung verwendet:

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

## Anwendung ausprobieren

Probiere die [Streamlit-Demoanwendung](https://st-gettext-example.streamlit.app/) aus.

Der Quellcode befindet sich im [Beispielverzeichnis](https://github.com/insolor/streamlit-gettext/tree/main/example).

## API-Referenz

Eine Beschreibung der Funktionen und weiteren Schnittstellen findest du in der [API-Referenz](api.md).
