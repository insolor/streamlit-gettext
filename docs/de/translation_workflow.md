# Übersetzungsablauf

Das Beispiel verwendet GNU-gettext-Kataloge:

- `locale/messages.pot` ist die Vorlage mit den aus dem Quellcode extrahierten Texten.
- `locale/<Sprache>/LC_MESSAGES/messages.po` enthält die Übersetzungen für eine Sprache.
- `messages.mo` ist der kompilierte Katalog, den die Anwendung verwendet.

Das gettext-Format wird von vielen Online-Übersetzungsplattformen unterstützt, zum Beispiel [Crowdin](https://crowdin.com/) und [Transifex](https://www.transifex.com/). `.po`-Dateien lassen sich auch mit speziellen Programmen wie [Poedit](https://poedit.net/) bearbeiten.

Eine ausführliche Anleitung zum Übersetzen von Anwendungen mit gettext findest du im [Lokalise-Tutorial](https://lokalise.com/blog/translating-apps-with-gettext-comprehensive-tutorial/). Das ist ein Link zu einer hilfreichen Anleitung und keine Werbung.

Das Beispielprojekt enthält [Poe-the-Poet](https://poethepoet.natn.io/)-Aufgaben, die wiederkehrende Schritte automatisieren. Führe sie im Verzeichnis `example/` aus. Sie sind besonders nützlich, wenn die Anwendung mehrere Sprachen unterstützt: Alle vorhandenen Sprachkataloge lassen sich damit gemeinsam aktualisieren oder kompilieren.

Installiere vor dem Ausführen der Aufgaben [GNU gettext](https://www.gnu.org/software/gettext/) und [Poe the Poet](https://poethepoet.natn.io/). Falls Poe noch nicht installiert ist, kannst du es so installieren:

```console
uv tool install poethepoet
```

Diese Aufgabendefinitionen werden in `example/pyproject.toml` verwendet:

```toml
[tool.poe.tasks]
run = "streamlit run app.py"
xgettext.shell = "xgettext -d messages -o ./locale/messages.pot *.py --from-code=UTF-8 --no-location"
msgfmt = "find ./locale -name \\*.po -execdir msgfmt messages.po -o messages.mo \\;"
msgmerge.shell = "find locale -name '*.po' -exec msgmerge -U {} locale/messages.pot \\; && find locale -name '*.po~' -delete"
```

`xgettext` sammelt die Zeichenketten aus den Python-Dateien in einer gemeinsamen Vorlage. `msgmerge` aktualisiert alle vorhandenen `.po`-Kataloge anhand dieser Vorlage und entfernt Sicherungskopien; `msgfmt` kompiliert jeden `.po`-Katalog in eine `.mo`-Datei. Diese Befehle gehören zu GNU gettext; Poe führt lediglich die konfigurierten Aufgaben aus.

## 1. Texte zur Übersetzung markieren

Umschließe benutzerseitig sichtbare Zeichenketten mit `gettext` (üblicherweise als `_` importiert). Für Einzahl und Mehrzahl verwendest du `ngettext`. Beispiel:

```python
st.write(_("Squirrel application"))
ngettext("One squirrel", "%(num)d squirrels", count)
```

## 2. Texte aus dem Code extrahieren

Erstelle nach dem Hinzufügen oder Ändern übersetzbarer Zeichenketten die Nachrichtenvorlage:

```console
poe xgettext
```

Die Aufgabe führt `xgettext` für die Python-Dateien im Verzeichnis `example/` aus und aktualisiert `locale/messages.pot`.

## 3. Kataloge aktualisieren und übersetzen

Führe die aktuelle Vorlage mit allen vorhandenen `.po`-Katalogen zusammen:

```console
poe msgmerge
```

Öffne jede Datei `locale/<Sprache>/LC_MESSAGES/messages.po` und übersetze die Werte in `msgstr`. Platzhalter wie `%(num)d` dürfen nicht geändert werden. Übersetze bei Pluralformen alle für die Sprache erforderlichen `msgstr[n]`-Formen.

Beim Aktualisieren eines Katalogs kann `msgmerge` einen Eintrag als `fuzzy` markieren, wenn sich der Ausgangstext geändert hat, dem alten Text aber noch ähnelt. Die bisherige Übersetzung bleibt als Vorschlag erhalten, ist möglicherweise jedoch nicht mehr passend. Prüfe sie und entferne die Markierung `fuzzy`: `msgfmt` überspringt solche Einträge, sodass die Anwendung sie nicht verwenden kann.

Die Aufgabe aktualisiert vorhandene Kataloge. Um eine Sprache hinzuzufügen, musst du zuerst die entsprechende `.po`-Datei anlegen.

## 4. Übersetzungen kompilieren und prüfen

Kompiliere die übersetzten Kataloge in `.mo`-Dateien:

```console
poe msgfmt
```

Starte das Beispiel und überprüfe die Übersetzungen in der Anwendung:

```console
poe run
```

Wenn sich die Ausgangstexte ändern, führe `poe xgettext` und `poe msgmerge` erneut aus, übersetze neue oder geänderte Einträge und kompiliere die Kataloge noch einmal.
