# Szybki start

Utwórz niewielką aplikację z angielskimi tekstami źródłowymi, polskimi tłumaczeniami, wyborem języka oraz komunikatami uwzględniającymi kontekst i formy liczby mnogiej.

## 1. Zainstaluj narzędzia

Potrzebujesz Pythona 3.11 lub nowszego. W terminalu utwórz projekt i zainstaluj pakiety Pythona:

```sh
mkdir localized-app
cd localized-app
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit streamlit-gettext poethepoet
```

Te polecenia używają powłoki Bash w systemie Linux lub macOS. W Windows wykonaj cały przewodnik w WSL, łącznie z konfiguracją środowiska wirtualnego, aby `poe` i zadania powłoki korzystały z tego samego środowiska Linux.

Osobno zainstaluj GNU gettext, który udostępnia `xgettext` i `msgfmt`. Na przykład w Ubuntu lub Debianie:

```sh
sudo apt-get install gettext
```

W macOS z Homebrew:

```sh
brew install gettext
```

Dla innych systemów zobacz [instrukcje instalacji GNU gettext](https://www.gnu.org/software/gettext/). Pozostałe polecenia wykonuj z katalogu `localized-app/` przy aktywnym środowisku wirtualnym.

## 2. Utwórz moduł tłumaczeń

Zapisz poniższy kod jako `i18n.py` obok `app.py`. Ten moduł jest częścią Twojej aplikacji; biblioteka go nie instaluje.

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

Ścieżka katalogu tłumaczeń jest określana względem `i18n.py`, więc nie zależy od katalogu roboczego. Domyślna domena to `messages`, której odpowiadają pliki `messages.po` i `messages.mo`.

## 3. Utwórz aplikację

Zapisz ten kod jako `app.py`:

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

`gettext` tłumaczy pojedynczy komunikat. `ngettext` wybiera formę liczby mnogiej. Dzięki argumentowi kontekstu `pgettext` odróżnia „Open” jako czynność od „Open” jako stanu. `npgettext` łączy kontekst z wyborem formy liczby.

Wybierz `auto`, aby używać języka przeglądarki, lub kod języka, aby go zastąpić. Przekazanie `None` przywraca wykrywanie języka przeglądarki. Ręczny wybór jest przechowywany osobno dla każdej sesji Streamlit. Teksty źródłowe w tym przykładzie są angielskie, dlatego `en` używa oryginalnych komunikatów, gdy nie ma angielskiego katalogu.

## 4. Wyodrębnij i przetłumacz komunikaty

Utwórz w głównym katalogu projektu plik `pyproject.toml` z poniższymi zadaniami lub dodaj tę sekcję do istniejącego pliku:

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

[Poe the Poet](https://poethepoet.natn.io/) uruchamia polecenia zapisane w tym pliku. Opcje wpisujesz raz, a potem wystarczą krótkie nazwy zadań. GNU gettext nadal musi być zainstalowany osobno.

`xgettext` rozpoznaje Pythona po rozszerzeniu `.py`, uwzględnia kodowanie kodu Pythona i domyślnie rozpoznaje `_`, `gettext` oraz `ngettext`. Wywołania z kontekstem wymagają dodatkowych opcji `--keyword`.

Opcje wyodrębniania:

| Opcja | Przeznaczenie |
|---|---|
| `--keyword=pgettext:1c,2` | Argument 1 to kontekst (`c`), argument 2 to komunikat. |
| `--keyword=npgettext:1c,2,3` | Argument 1 to kontekst, a argumenty 2 i 3 to komunikaty w liczbie pojedynczej i mnogiej. |
| `--no-location` | Pomija pozycje w kodzie źródłowym, ograniczając zmiany katalogu przy przenoszeniu kodu. |
| `--output=locale/messages.pot` | Zapisuje wspólny szablon komunikatów w tym pliku. |
| `app.py` | Analizowany plik źródłowy; w miarę rozwoju aplikacji dopisz kolejne pliki. |

`init_po` przyjmuje wymagany argument pozycyjny z językiem. Zadanie tworzy `locale/<language>/LC_MESSAGES` i przekazuje język do `msginit`. Uruchom `poe init_po pl` dla polskiego lub `poe init_po ja` dla japońskiego. Dodawanie języków nie wymaga zmiany zadań.

`update_po` i `compile_mo` używają `find`, aby przetworzyć wszystkie pliki `.po` w `locale/`. Pierwsze zadanie aktualizuje katalogi ze wspólnego szablonu bez kopii zapasowych; drugie sprawdza znaczniki formatowania i tworzy `.mo` obok każdego `.po`. `${po%.po}` usuwa końcówkę `.po` przed dodaniem `.mo`. Pętla `for po do` przetwarza ścieżki przekazane przez `find`, a `|| exit` przekazuje błędy gettext dalej. Przy `-exec … +` także `find` zwraca błąd, jeśli przetwarzanie grupy plików się nie powiedzie. Dzięki temu Poe i CI wykrywają awarię. Ścieżki są w cudzysłowach, aby obsługiwać nazwy katalogów ze spacjami.

Te zadania wymagają powłoki POSIX i `find`, dostępnych w systemach Linux i macOS. W Windows wykonaj przewodnik w WSL.

Utwórz wspólny katalog i wyodrębnij komunikaty:

```sh
mkdir -p locale
poe extract_pot
```

Utwórz plik `.po` z szablonu:

```sh
poe init_po pl
```

Zadanie uruchamia `msginit`: `--input` wskazuje szablon, `--output-file` nowy katalog tłumaczeń, `--locale=pl` język, a `--no-translator` wyłącza interaktywne pytania o dane tłumacza. Polecenie tworzy wpisy z pustymi tłumaczeniami i inicjalizuje nagłówek, w tym `Language` i `Plural-Forms`.

Uruchom `poe init_po <language>` raz dla każdego nowego języka. Kolejne wywołania `poe update_po` i `poe compile_mo` przetwarzają wszystkie dodane języki razem.

Tłumaczenia możesz uzupełniać w specjalnym edytorze, takim jak [Poedit](https://poedit.com/), który oferuje interfejs do komunikatów i form liczby mnogiej. Wiele serwisów internetowych, w tym [Crowdin](https://support.crowdin.com/developer/configuration-file/#gettext-project) i [Transifex](https://help.transifex.com/en/articles/6220794-gettext-po), obsługuje `.po` natywnie, bez konwersji do innego formatu.

Możesz skonfigurować integrację z repozytorium, aby przesyłać zaktualizowane komunikaty źródłowe i odbierać gotowe tłumaczenia, na przykład przez [integrację Crowdin z GitHub](https://support.crowdin.com/github-integration/) lub [integrację Transifex z GitHub](https://help.transifex.com/en/articles/6265125-github-installation-and-configuration). Po otrzymaniu nowych plików `.po` uruchom `poe compile_mo`, aby aplikacja używała aktualnych tłumaczeń.

Otwórz `locale/pl/LC_MESSAGES/messages.po` i uzupełnij `msgstr` oraz `msgstr[n]`. W nagłówku metadanych (`msgid ""`) ustaw kodowanie UTF-8 i zapisz plik w tym kodowaniu:

```po
"Content-Type: text/plain; charset=UTF-8\n"
```

Zachowaj pozostałe wygenerowane pola nagłówka, w tym `Plural-Forms`. Przetłumaczone wpisy powinny wyglądać tak:

```po
msgid "File manager"
msgstr "Menedżer plików"

msgid "Number of files"
msgstr "Liczba plików"

#, python-format
msgid "%(num)d file"
msgid_plural "%(num)d files"
msgstr[0] "%(num)d plik"
msgstr[1] "%(num)d pliki"
msgstr[2] "%(num)d plików"

msgctxt "action"
msgid "Open"
msgstr "Otwórz"

msgctxt "state"
msgid "Open"
msgstr "Otwarty"

#, python-format
msgctxt "download"
msgid "Download %(num)d file"
msgid_plural "Download %(num)d files"
msgstr[0] "Pobierz %(num)d plik"
msgstr[1] "Pobierz %(num)d pliki"
msgstr[2] "Pobierz %(num)d plików"
```

`.pot` to wyodrębniony szablon, `.po` to edytowalne tłumaczenie, a `.mo` to skompilowany katalog wczytywany przez aplikację. `msgctxt` musi odpowiadać kontekstowi w wywołaniu Pythona. Nie zmieniaj `%(num)d` i przetłumacz wszystkie formy liczby wymagane w danym języku. Polski ma trzy formy; inne języki mogą wymagać innej liczby form i innego wyrażenia `Plural-Forms`.

## 5. Skompiluj i uruchom

```sh
poe compile_mo
```

Projekt ma teraz następującą strukturę:

```text
localized-app/
├── app.py
├── i18n.py
├── pyproject.toml
└── locale/
    ├── messages.pot
    └── pl/
        └── LC_MESSAGES/
            ├── messages.po
            └── messages.mo
```

Uruchom aplikację:

```sh
python -m streamlit run app.py
```

Wybierz `pl`: tytuł powinien zmienić się na „Menedżer plików”. Ustaw suwak na 1, 2 i 5, aby zobaczyć „1 plik”, „2 pliki” i „5 plików”. Przycisk pokazuje „Otwórz”, a stan „Otwarty”. Wybierz `en`, aby wrócić do tekstu angielskiego, lub `auto`, aby używać języka przeglądarki.

Jeśli komunikat nadal jest angielski, sprawdź wybrany język, położenie katalogu, domenę i czy plik `.mo` został ponownie skompilowany po edycji `.po`. `msgfmt` pomija wpisy oznaczone jako `fuzzy`: sprawdź tłumaczenie i usuń oznaczenie przed kompilacją. Po ponownej kompilacji uruchom Streamlit ponownie, aby wyczyścić pamięć podręczną tłumaczeń.

## Aktualizowanie tłumaczeń

Po zmianie komunikatów źródłowych ponownie je wyodrębnij i zaktualizuj katalogi:

```sh
poe extract_pot
poe update_po
```

Przetłumacz nowe lub zmienione wpisy, sprawdź oznaczenia `fuzzy`, uruchom `poe compile_mo` i ponownie uruchom aplikację. Zobacz [proces tłumaczenia](translation_workflow.md), aby poznać zadania przykładu w repozytorium, lub [dokumentację API](api.md), aby poznać interfejsy biblioteki.
