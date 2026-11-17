# Schnellstart

Erstellen Sie eine kleine App mit englischen Ausgangstexten, deutschen Übersetzungen, einer Sprachauswahl und kontextabhängigen Pluralmeldungen.

## 1. Werkzeuge installieren

Sie benötigen Python 3.11 oder neuer. Erstellen Sie im Terminal ein Projekt und installieren Sie die Python-Pakete:

```sh
mkdir localized-app
cd localized-app
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit streamlit-gettext poethepoet
```

Diese Shell-Befehle verwenden Bash unter Linux oder macOS. Unter Windows führen Sie die gesamte Anleitung einschließlich der Einrichtung der virtuellen Umgebung in WSL aus, damit `poe` und die Shell-Aufgaben dieselbe Linux-Umgebung verwenden.

Installieren Sie GNU gettext separat. Es stellt `xgettext` und `msgfmt` bereit. Unter Ubuntu oder Debian beispielsweise:

```sh
sudo apt-get install gettext
```

Unter macOS mit Homebrew:

```sh
brew install gettext
```

Für andere Systeme siehe die [Installationshinweise zu GNU gettext](https://www.gnu.org/software/gettext/). Führen Sie die weiteren Befehle bei aktivierter virtueller Umgebung aus dem Verzeichnis `localized-app/` aus.

## 2. Übersetzungsmodul erstellen

Speichern Sie den folgenden Code als `i18n.py` neben `app.py`. Dieses Modul gehört zu Ihrer App und wird nicht von der Bibliothek installiert.

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

Der Katalogpfad ist relativ zu `i18n.py` und hängt daher nicht vom Arbeitsverzeichnis ab. Die Standarddomäne ist `messages`; ihr entsprechen `messages.po` und `messages.mo`.

## 3. App erstellen

Speichern Sie diesen Code als `app.py`:

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

`gettext` übersetzt eine einzelne Meldung. `ngettext` wählt eine Pluralform. `pgettext` unterscheidet über den Kontext zwischen „Open“ als Aktion und „Open“ als Zustand. `npgettext` kombiniert Kontext und Pluralauswahl.

Wählen Sie `auto`, um die Browsersprache zu verwenden, oder einen Sprachcode, um sie zu überschreiben. Mit `None` wird die Browsererkennung wiederhergestellt. Die manuelle Auswahl wird für jede Streamlit-Sitzung getrennt gespeichert. Die Ausgangstexte dieses Beispiels sind Englisch: Bei `en` werden ohne englischen Katalog die Originalmeldungen verwendet.

## 4. Meldungen extrahieren und übersetzen

Erstellen Sie im Projektverzeichnis eine `pyproject.toml` mit diesen Aufgaben oder ergänzen Sie eine vorhandene Datei um diesen Abschnitt:

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

[Poe the Poet](https://poethepoet.natn.io/) führt die in dieser Datei gespeicherten Befehle aus. Die Optionen werden einmal eingetragen; anschließend genügen kurze Aufgabennamen. GNU gettext muss weiterhin separat installiert sein.

`xgettext` erkennt Python an der Erweiterung `.py`, berücksichtigt die Kodierung des Python-Quelltexts und erkennt `_`, `gettext` und `ngettext` standardmäßig. Für Aufrufe mit Kontext sind zusätzliche `--keyword`-Optionen erforderlich.

Die Extraktionsoptionen:

| Option | Zweck |
|---|---|
| `--keyword=pgettext:1c,2` | Argument 1 ist der Kontext (`c`), Argument 2 die Meldung. |
| `--keyword=npgettext:1c,2,3` | Argument 1 ist der Kontext; Argumente 2 und 3 sind Singular- und Pluralmeldung. |
| `--no-location` | Quelltextpositionen im Katalog weglassen, damit verschobener Code weniger Änderungen erzeugt. |
| `--output=locale/messages.pot` | Die gemeinsame Meldungsvorlage in diese Datei schreiben. |
| `app.py` | Die zu durchsuchende Quelldatei; ergänzen Sie weitere Dateien, wenn die App wächst. |

`init_po` erwartet die Sprache als erforderliches Positionsargument. Die Aufgabe erstellt `locale/<language>/LC_MESSAGES` und übergibt die Sprache an `msginit`. Verwenden Sie `poe init_po de` für Deutsch oder `poe init_po ja` für Japanisch. Beim Hinzufügen von Sprachen müssen die Aufgaben nicht geändert werden.

`update_po` und `compile_mo` verarbeiten mit `find` alle `.po`-Dateien unter `locale/`. Die erste Aufgabe aktualisiert alle Kataloge anhand der gemeinsamen Vorlage ohne Sicherungsdateien. Die zweite prüft Formatplatzhalter und erstellt neben jeder `.po` eine `.mo`. `${po%.po}` entfernt die Endung `.po`, bevor `.mo` angehängt wird. `for po do` verarbeitet die von `find` übergebenen Pfade; `|| exit` gibt gettext-Fehler weiter. Bei `-exec … +` liefert auch `find` einen Fehlerstatus, wenn die Verarbeitung einer Gruppe fehlschlägt. So können Poe und CI den Fehler erkennen. Pfade stehen in Anführungszeichen, damit Verzeichnisnamen mit Leerzeichen funktionieren.

Diese Shell-Aufgaben benötigen eine POSIX-Shell und `find`, verfügbar unter Linux und macOS. Unter Windows führen Sie die Anleitung in WSL aus.

Erstellen Sie das gemeinsame Katalogverzeichnis und extrahieren Sie die Meldungen:

```sh
mkdir -p locale
poe extract_pot
```

Erstellen Sie die `.po`-Datei aus der Vorlage:

```sh
poe init_po de
```

Diese Aufgabe führt `msginit` aus: `--input` wählt die Vorlage, `--output-file` den neuen Übersetzungskatalog, `--locale=de` die Sprache. `--no-translator` deaktiviert interaktive Abfragen zu Übersetzerdaten. Der Befehl erstellt Einträge mit leeren Übersetzungen und initialisiert den Kopf einschließlich `Language` und `Plural-Forms`.

Führen Sie `poe init_po <language>` einmal je neuer Sprache aus. Spätere Aufrufe von `poe update_po` und `poe compile_mo` verarbeiten alle hinzugefügten Sprachen gemeinsam.

Sie können Übersetzungen mit einem speziellen Editor wie [Poedit](https://poedit.com/) ausfüllen, der eine Oberfläche für Meldungen und Pluralformen bietet. Viele Online-Übersetzungsdienste, darunter [Crowdin](https://support.crowdin.com/developer/configuration-file/#gettext-project) und [Transifex](https://help.transifex.com/en/articles/6220794-gettext-po), unterstützen `.po` nativ, ohne Konvertierung in ein anderes Format.

Über eine Repository-Integration lassen sich aktualisierte Ausgangsmeldungen übertragen und fertige Übersetzungen zurückholen, etwa mit der [GitHub-Integration von Crowdin](https://support.crowdin.com/github-integration/) oder der [GitHub-Integration von Transifex](https://help.transifex.com/en/articles/6265125-github-installation-and-configuration). Führen Sie nach dem Empfang aktualisierter `.po`-Dateien `poe compile_mo` aus, damit die App die neuen Übersetzungen verwendet.

Öffnen Sie `locale/de/LC_MESSAGES/messages.po` und füllen Sie `msgstr` und `msgstr[n]` aus. Stellen Sie im Metadatenkopf (`msgid ""`) UTF-8 als Zeichensatz ein und speichern Sie die Datei in dieser Kodierung:

```po
"Content-Type: text/plain; charset=UTF-8\n"
```

Behalten Sie die übrigen generierten Kopffelder einschließlich `Plural-Forms` bei. Die übersetzten Einträge sollten so aussehen:

```po
msgid "File manager"
msgstr "Dateimanager"

msgid "Number of files"
msgstr "Anzahl der Dateien"

#, python-format
msgid "%(num)d file"
msgid_plural "%(num)d files"
msgstr[0] "%(num)d Datei"
msgstr[1] "%(num)d Dateien"

msgctxt "action"
msgid "Open"
msgstr "Öffnen"

msgctxt "state"
msgid "Open"
msgstr "Geöffnet"

#, python-format
msgctxt "download"
msgid "Download %(num)d file"
msgid_plural "Download %(num)d files"
msgstr[0] "%(num)d Datei herunterladen"
msgstr[1] "%(num)d Dateien herunterladen"
```

`.pot` ist die extrahierte Vorlage, `.po` die bearbeitbare Übersetzung und `.mo` der kompilierte Katalog, den die App lädt. `msgctxt` muss dem Kontext im Python-Aufruf entsprechen. Lassen Sie `%(num)d` unverändert und übersetzen Sie alle für die Sprache erforderlichen Pluralformen. Deutsch hat zwei Formen; andere Sprachen können eine andere Anzahl und einen anderen `Plural-Forms`-Ausdruck benötigen.

## 5. Kompilieren und starten

```sh
poe compile_mo
```

Ihr Projekt hat nun diese Struktur:

```text
localized-app/
├── app.py
├── i18n.py
├── pyproject.toml
└── locale/
    ├── messages.pot
    └── de/
        └── LC_MESSAGES/
            ├── messages.po
            └── messages.mo
```

Starten Sie die App:

```sh
python -m streamlit run app.py
```

Wählen Sie `de`: Der Titel sollte „Dateimanager“ lauten. Stellen Sie den Schieberegler auf 1, 2 und 5, um „1 Datei“, „2 Dateien“ und „5 Dateien“ zu sehen. Die Schaltfläche zeigt „Öffnen“, der Zustand „Geöffnet“. Mit `en` kehren Sie zum englischen Ausgangstext zurück, mit `auto` zur Browsersprache.

Bleibt eine Meldung Englisch, prüfen Sie die ausgewählte Sprache, den Katalogpfad, die Domäne und ob die `.mo` nach dem Bearbeiten der `.po` neu kompiliert wurde. `msgfmt` überspringt als `fuzzy` markierte Einträge. Prüfen Sie die Übersetzung und entfernen Sie die Markierung vor dem Kompilieren. Starten Sie Streamlit nach dem Neukompilieren neu, um zwischengespeicherte Übersetzungen zu löschen.

## Übersetzungen aktuell halten

Extrahieren Sie nach Änderungen an Ausgangsmeldungen diese erneut und aktualisieren Sie die Übersetzungskataloge:

```sh
poe extract_pot
poe update_po
```

Übersetzen Sie neue oder geänderte Einträge, prüfen Sie `fuzzy`-Markierungen, führen Sie `poe compile_mo` aus und starten Sie die App neu. Der [Übersetzungsablauf](translation_workflow.md) beschreibt die Aufgaben des Repository-Beispiels, die [API-Referenz](api.md) die Schnittstellen der Bibliothek.
