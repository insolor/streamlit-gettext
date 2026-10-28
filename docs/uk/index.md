# Документація streamlit-gettext

`streamlit-gettext` допомагає додавати переклади до застосунків на Streamlit. Бібліотека враховує мовні налаштування браузера й показує користувачеві відповідний переклад.

Проєкт ще розвивається, тому документація та можливості бібліотеки можуть змінюватися.

## Що вміє бібліотека

- **Перекладати текст:** Позначайте рядки для перекладу за допомогою `gettext` — зазвичай її імпортують під коротким ім’ям `_`.
- **Враховувати кількість об’єктів:** Функція `ngettext` вибирає потрібну форму повідомлення, наприклад для однієї чи кількох білок.
- **Вибирати мову:** Бібліотека може враховувати мовні налаштування браузера.

## Простий приклад

Ось як підключити функції перекладу в застосунку Streamlit:

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

Виклик `_()` позначає текст, який потрібно перекласти. `ngettext()` добирає форму повідомлення відповідно до кількості білок, а повзунок дає змогу змінювати їхню кількість.

Це лише приклад коду, а не покрокова інструкція з налаштування. Щоб запустити локалізований застосунок, знадобляться також файли перекладів і конфігурація проєкту.

## Перемикання мови вручну

У цьому варіанті користувач сам вибирає мову в меню. Вибір передається до `set_preferred_languages()`, і застосунок показує переклад цією мовою:

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

## Спробувати застосунок

Перевірте, як це працює, у [демонстраційному застосунку на Streamlit](https://st-gettext-example.streamlit.app/).

Вихідний код доступний у [каталозі з прикладом](https://github.com/insolor/streamlit-gettext/tree/main/example).

## Довідник API

Опис функцій та інших інтерфейсів бібліотеки наведено в [довіднику API](api.md).
