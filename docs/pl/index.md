# streamlit-gettext

`streamlit-gettext` to rozszerzenie do Streamlit, które ułatwia dodawanie tłumaczeń do aplikacji. Biblioteka uwzględnia preferencje językowe przeglądarki i wyświetla użytkownikowi odpowiednie tłumaczenie.

Projekt jest nadal rozwijany, dlatego dokumentacja i dostępne funkcje mogą się zmieniać.

## Co potrafi biblioteka?

- **Tłumaczy tekst.** Oznaczaj ciągi do tłumaczenia za pomocą `gettext`, zwykle importowanej pod krótką nazwą `_`.
- **Obsługuje liczbę mnogą.** Funkcja `ngettext` wybiera odpowiednią formę komunikatu w zależności od liczby.
- **Wybiera język.** Biblioteka może uwzględniać preferencje językowe przeglądarki.

## Prosty przykład

Oto jak użyć funkcji tłumaczących w aplikacji Streamlit:

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

Wywołanie `_()` oznacza tekst do przetłumaczenia. `ngettext()` dobiera formę komunikatu do liczby wiewiórek, a suwak pozwala zmieniać ich liczbę.

To tylko przykład kodu, a nie pełna instrukcja konfiguracji. Do uruchomienia zlokalizowanej aplikacji potrzebne są również pliki tłumaczeń i konfiguracja projektu.

## Ręczna zmiana języka

W tej wersji użytkownik sam wybiera język z menu. Wybrany język jest przekazywany do `set_preferred_languages()`, dzięki czemu aplikacja wyświetla odpowiednie tłumaczenie:

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

## Wypróbuj aplikację

Zobacz, jak to działa, w [demonstracyjnej aplikacji Streamlit](https://st-gettext-example.streamlit.app/).

Kod źródłowy znajdziesz w [katalogu z przykładem](https://github.com/insolor/streamlit-gettext/tree/main/example).

## Dokumentacja API

Opis funkcji i pozostałych interfejsów biblioteki znajdziesz w [dokumentacji API](api.md).
