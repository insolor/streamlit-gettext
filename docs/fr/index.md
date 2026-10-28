# Documentation de streamlit-gettext

`streamlit-gettext` est une extension pour Streamlit qui facilite la localisation des applications. La bibliothèque tient compte des préférences linguistiques du navigateur et affiche la traduction adaptée à chaque utilisateur.

Si l’application ne lit la langue du navigateur qu’une seule fois au démarrage, cette valeur risque d’être réutilisée pour tout le monde : chaque utilisateur verra alors la langue de la première personne à avoir ouvert l’application. `streamlit-gettext` évite ce problème en vérifiant la langue du navigateur de l’utilisateur à chaque traduction. Ainsi, une même application peut s’afficher dans des langues différentes selon les utilisateurs.

Le projet est encore en développement ; la documentation et les fonctionnalités peuvent donc évoluer.

## Que permet la bibliothèque ?

- **Traduire du texte.** Marquez les chaînes à traduire avec `gettext`, généralement importée sous le nom `_`.
- **Gérer le singulier et le pluriel.** Utilisez `ngettext` pour choisir la forme du message en fonction de la quantité.
- **Choisir la langue.** La bibliothèque peut tenir compte des préférences linguistiques du navigateur.

## Exemple simple

Voici comment utiliser les fonctions de traduction dans une application Streamlit :

```python
import streamlit as st
from i18n import gettext as _
from i18n import ngettext

st.write(_("Squirrel application"))

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

L’appel `_()` marque le texte à traduire. `ngettext()` choisit la forme du message selon le nombre d’écureuils, et le curseur permet de modifier cette quantité.

Il s’agit uniquement d’un exemple de code, pas d’un guide complet de configuration. Pour exécuter une application localisée, il faut également les fichiers de traduction et la configuration du projet.

## Changer de langue manuellement

Dans cette version, l’utilisateur choisit la langue dans un menu. La sélection est transmise à `set_preferred_languages()` afin que l’application affiche la traduction correspondante :

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

st.write(_("Squirrel application"))

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

## Essayer l’application

Découvrez le résultat dans l’[application de démonstration Streamlit](https://st-gettext-example.streamlit.app/).

Le code source est disponible dans le [répertoire de l’exemple](https://github.com/insolor/streamlit-gettext/tree/main/example).

## Référence de l’API

Consultez la [référence de l’API](api.md) pour en savoir plus sur les fonctions et les autres interfaces de la bibliothèque.
