# Processus de traduction

L’exemple utilise les catalogues GNU gettext :

- `locale/messages.pot` est le modèle contenant les textes extraits du code source.
- `locale/<langue>/LC_MESSAGES/messages.po` contient les traductions d’une langue.
- `messages.mo` est le catalogue compilé utilisé par l’application.

Le format gettext est pris en charge par de nombreuses plateformes de traduction en ligne, notamment [Crowdin](https://crowdin.com/) et [Transifex](https://www.transifex.com/). Vous pouvez aussi modifier les fichiers `.po` avec un logiciel dédié comme [Poedit](https://poedit.net/).

Pour un guide plus détaillé sur la traduction d’applications avec gettext, consultez le [tutoriel de Lokalise](https://lokalise.com/blog/translating-apps-with-gettext-comprehensive-tutorial/). Il s’agit d’un lien vers un guide utile, pas d’une publicité.

Le projet d’exemple définit des tâches [Poe the Poet](https://poethepoet.natn.io/) pour automatiser les opérations répétitives. Lancez-les depuis le répertoire `example/`. Elles sont particulièrement pratiques lorsque l’application prend en charge plusieurs langues : elles mettent à jour ou compilent tous les catalogues existants en une seule fois.

Avant de lancer ces tâches, installez [GNU gettext](https://www.gnu.org/software/gettext/) et [Poe the Poet](https://poethepoet.natn.io/). Si Poe n’est pas encore installé, utilisez :

```console
uv tool install poethepoet
```

Voici les définitions de tâches utilisées dans `example/pyproject.toml` :

```toml
[tool.poe.tasks]
run = "streamlit run app.py"
xgettext.shell = "xgettext -d messages -o ./locale/messages.pot *.py --from-code=UTF-8 --no-location"
msgfmt = "find ./locale -name \\*.po -execdir msgfmt messages.po -o messages.mo \\;"
msgmerge.shell = "find locale -name '*.po' -exec msgmerge -U {} locale/messages.pot \\; && find locale -name '*.po~' -delete"
```

`xgettext` extrait les chaînes des fichiers Python pour créer un modèle commun. `msgmerge` met à jour tous les catalogues `.po` existants à partir de ce modèle et supprime les fichiers de sauvegarde ; `msgfmt` compile chaque catalogue `.po` en fichier `.mo`. Ces commandes font partie de GNU gettext ; Poe ne fait qu’exécuter les tâches configurées.

## 1. Marquer le texte à traduire

Entourez les chaînes destinées aux utilisateurs avec `gettext` (généralement importée sous le nom `_`). Pour le singulier et le pluriel, utilisez `ngettext`. Par exemple :

```python
st.write(_("Some text"))
ngettext("One squirrel", "%(num)d squirrels", count)
```

## 2. Extraire les chaînes du code

Après avoir ajouté ou modifié des chaînes traduisibles, générez le modèle de messages :

```console
poe xgettext
```

Cette tâche exécute `xgettext` sur les fichiers Python du répertoire `example/` et met à jour `locale/messages.pot`.

## 3. Mettre à jour les catalogues et traduire

Fusionnez le modèle le plus récent dans tous les catalogues `.po` existants :

```console
poe msgmerge
```

Ouvrez chaque fichier `locale/<langue>/LC_MESSAGES/messages.po` et traduisez les valeurs `msgstr`. Ne modifiez pas les paramètres tels que `%(num)d`. Pour les messages au pluriel, traduisez toutes les formes `msgstr[n]` nécessaires dans cette langue.

Lors de la mise à jour d’un catalogue, `msgmerge` peut marquer une entrée comme `fuzzy` si le texte source a changé tout en ressemblant à l’ancien. L’ancienne traduction est conservée comme suggestion, mais elle peut ne plus convenir. Vérifiez-la et retirez le marqueur `fuzzy` : `msgfmt` ignore ces entrées, qui ne seront donc pas disponibles dans l’application.

La tâche met à jour les catalogues existants. Pour ajouter une langue, créez d’abord son fichier `.po`.

## 4. Compiler les traductions et vérifier le résultat

Compilez les catalogues traduits en fichiers `.mo` :

```console
poe msgfmt
```

Lancez l’exemple et vérifiez les traductions dans l’application :

```console
poe run
```

Lorsque les chaînes source changent, relancez `poe xgettext` et `poe msgmerge`, traduisez les nouvelles entrées ou celles qui ont changé, puis recompilez les catalogues.
