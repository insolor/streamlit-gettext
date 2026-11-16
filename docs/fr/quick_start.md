# Démarrage rapide

Créez une petite application avec des textes sources en anglais, des traductions en français, un sélecteur de langue et des messages au pluriel tenant compte du contexte.

## 1. Installer les outils

Utilisez Python 3.11 ou une version ultérieure. Dans un terminal, créez un projet et installez les paquets Python :

```sh
mkdir localized-app
cd localized-app
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit streamlit-gettext poethepoet
```

Ces commandes utilisent Bash sous Linux ou macOS. Sous Windows, suivez tout le guide dans WSL, y compris la création de l’environnement virtuel, afin que `poe` et les tâches shell utilisent le même environnement Linux.

Installez GNU gettext séparément : il fournit `xgettext` et `msgfmt`. Par exemple, sous Ubuntu ou Debian :

```sh
sudo apt-get install gettext
```

Sous macOS avec Homebrew :

```sh
brew install gettext
```

Pour les autres systèmes, consultez les [instructions d’installation de GNU gettext](https://www.gnu.org/software/gettext/). Exécutez les commandes suivantes depuis `localized-app/`, avec l’environnement virtuel activé.

## 2. Créer le module de traduction

Enregistrez le code suivant dans `i18n.py`, à côté de `app.py`. Ce module fait partie de votre application ; la bibliothèque ne l’installe pas.

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

Le chemin du catalogue est relatif à `i18n.py` et ne dépend donc pas du répertoire de travail. Le domaine par défaut est `messages`, qui correspond à `messages.po` et `messages.mo`.

## 3. Créer l’application

Enregistrez ce code dans `app.py` :

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

`gettext` traduit un message. `ngettext` choisit une forme de pluriel. Grâce à son argument de contexte, `pgettext` distingue « Open » en tant qu’action de « Open » en tant qu’état. `npgettext` combine contexte et choix du pluriel.

Choisissez `auto` pour suivre la langue du navigateur, ou un code de langue pour la remplacer. Passer `None` rétablit la détection du navigateur. Les préférences manuelles sont stockées séparément pour chaque session Streamlit. Les textes sources de cet exemple sont en anglais : `en` utilise donc les messages d’origine en l’absence de catalogue anglais.

## 4. Extraire et traduire les messages

Créez un fichier `pyproject.toml` à la racine du projet avec ces tâches, ou ajoutez cette section à un fichier existant :

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

[Poe the Poet](https://poethepoet.natn.io/) exécute les commandes enregistrées dans ce fichier. Les options ne sont saisies qu’une fois ; ensuite, de courts noms de tâches suffisent. GNU gettext doit toujours être installé séparément.

`xgettext` reconnaît Python grâce à l’extension `.py`, prend en compte l’encodage du code Python et reconnaît `_`, `gettext` et `ngettext` par défaut. Les appels avec contexte nécessitent les options `--keyword` supplémentaires.

Options d’extraction :

| Option | Rôle |
|---|---|
| `--keyword=pgettext:1c,2` | L’argument 1 est le contexte (`c`), l’argument 2 est le message. |
| `--keyword=npgettext:1c,2,3` | L’argument 1 est le contexte ; les arguments 2 et 3 sont les messages au singulier et au pluriel. |
| `--no-location` | Omettre les positions dans le code source pour limiter les changements lorsque le code est déplacé. |
| `--output=locale/messages.pot` | Écrire le modèle commun de messages dans ce fichier. |
| `app.py` | Fichier source à analyser ; ajoutez d’autres fichiers à mesure que l’application grandit. |

`init_po` accepte un argument positionnel obligatoire indiquant la langue. La tâche crée `locale/<language>/LC_MESSAGES` et transmet la langue à `msginit`. Utilisez `poe init_po fr` pour le français ou `poe init_po ja` pour le japonais, sans modifier les tâches lors de l’ajout de langues.

`update_po` et `compile_mo` utilisent `find` pour traiter tous les fichiers `.po` sous `locale/`. La première tâche met à jour les catalogues à partir du modèle commun sans créer de sauvegardes ; la seconde vérifie les paramètres de formatage et crée un `.mo` à côté de chaque `.po`. `${po%.po}` retire le suffixe `.po` avant d’ajouter `.mo`. `for po do` traite les chemins transmis par `find`, et `|| exit` propage les erreurs de gettext. Avec `-exec … +`, `find` renvoie aussi un code d’erreur si un lot échoue, ce qui permet à Poe et à la CI de détecter le problème. Les chemins sont entre guillemets pour accepter les noms de répertoires contenant des espaces.

Ces tâches nécessitent un shell POSIX et `find`, disponibles sous Linux et macOS. Sous Windows, suivez le guide dans WSL.

Créez le répertoire commun des catalogues et extrayez les messages :

```sh
mkdir -p locale
poe extract_pot
```

Créez le fichier `.po` à partir du modèle :

```sh
poe init_po fr
```

Cette tâche lance `msginit` : `--input` désigne le modèle, `--output-file` le nouveau catalogue, `--locale=fr` la langue, et `--no-translator` désactive les questions interactives sur le traducteur. La commande crée des entrées aux traductions vides et initialise l’en-tête, notamment `Language` et `Plural-Forms`.

Exécutez `poe init_po <language>` une fois par nouvelle langue. Les commandes suivantes `poe update_po` et `poe compile_mo` traitent toutes les langues ajoutées ensemble.

Vous pouvez remplir les traductions avec un éditeur spécialisé comme [Poedit](https://poedit.com/), qui propose une interface pour les messages et les formes de pluriel. De nombreux services en ligne, dont [Crowdin](https://support.crowdin.com/developer/configuration-file/#gettext-project) et [Transifex](https://help.transifex.com/en/articles/6220794-gettext-po), prennent en charge `.po` nativement, sans conversion.

Vous pouvez configurer une intégration au dépôt pour envoyer les messages sources mis à jour et récupérer les traductions, par exemple avec [l’intégration GitHub de Crowdin](https://support.crowdin.com/github-integration/) ou [celle de Transifex](https://help.transifex.com/en/articles/6265125-github-installation-and-configuration). Après réception des fichiers `.po` mis à jour, exécutez `poe compile_mo` pour que l’application utilise les nouvelles traductions.

Ouvrez `locale/fr/LC_MESSAGES/messages.po` et remplissez `msgstr` et `msgstr[n]`. Dans l’en-tête de métadonnées (`msgid ""`), définissez UTF-8 comme encodage et enregistrez le fichier dans cet encodage :

```po
"Content-Type: text/plain; charset=UTF-8\n"
```

Conservez les autres champs d’en-tête générés, notamment `Plural-Forms`. Les entrées traduites doivent ressembler à ceci :

```po
msgid "File manager"
msgstr "Gestionnaire de fichiers"

msgid "Number of files"
msgstr "Nombre de fichiers"

#, python-format
msgid "%(num)d file"
msgid_plural "%(num)d files"
msgstr[0] "%(num)d fichier"
msgstr[1] "%(num)d fichiers"

msgctxt "action"
msgid "Open"
msgstr "Ouvrir"

msgctxt "state"
msgid "Open"
msgstr "Ouvert"

#, python-format
msgctxt "download"
msgid "Download %(num)d file"
msgid_plural "Download %(num)d files"
msgstr[0] "Télécharger %(num)d fichier"
msgstr[1] "Télécharger %(num)d fichiers"
```

`.pot` est le modèle extrait, `.po` la traduction modifiable et `.mo` le catalogue compilé chargé par l’application. `msgctxt` doit correspondre au contexte de l’appel Python. Gardez `%(num)d` inchangé et traduisez toutes les formes de pluriel nécessaires à la langue. Le français en possède deux ; d’autres langues peuvent demander un autre nombre et une expression `Plural-Forms` différente.

## 5. Compiler et lancer

```sh
poe compile_mo
```

Votre projet possède maintenant cette structure :

```text
localized-app/
├── app.py
├── i18n.py
├── pyproject.toml
└── locale/
    ├── messages.pot
    └── fr/
        └── LC_MESSAGES/
            ├── messages.po
            └── messages.mo
```

Lancez l’application :

```sh
python -m streamlit run app.py
```

Choisissez `fr` : le titre doit devenir « Gestionnaire de fichiers ». Déplacez le curseur sur 1, 2 et 5 pour voir « 1 fichier », « 2 fichiers » et « 5 fichiers ». Le bouton affiche « Ouvrir », tandis que l’état affiche « Ouvert ». Choisissez `en` pour revenir aux textes anglais, ou `auto` pour utiliser la langue du navigateur.

Si un message reste en anglais, vérifiez la langue sélectionnée, l’emplacement du catalogue, le domaine et la recompilation du `.mo` après modification du `.po`. `msgfmt` ignore les entrées marquées `fuzzy` : vérifiez leur traduction et retirez ce marqueur avant la compilation. Redémarrez Streamlit après recompilation pour vider le cache des traductions.

## Maintenir les traductions à jour

Après avoir modifié les messages sources, extrayez-les à nouveau et mettez à jour les catalogues :

```sh
poe extract_pot
poe update_po
```

Traduisez les entrées nouvelles ou modifiées, vérifiez les marqueurs `fuzzy`, lancez `poe compile_mo`, puis redémarrez l’application. Consultez le [processus de traduction](translation_workflow.md) pour les tâches de l’exemple du dépôt et la [référence API](api.md) pour les interfaces de la bibliothèque.
