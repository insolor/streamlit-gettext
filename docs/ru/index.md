# Документация streamlit-gettext

`streamlit-gettext` помогает добавлять переводы в приложения на Streamlit. Библиотека учитывает языковые предпочтения браузера и показывает пользователю подходящий перевод.

Проект ещё развивается, поэтому документация и возможности библиотеки могут меняться.

## Что умеет библиотека

- **Переводить текст:** Помечайте строки для перевода с помощью `gettext` — обычно её импортируют под коротким именем `_`.
- **Учитывать число объектов:** Функция `ngettext` выбирает нужную форму сообщения: например, «1 белка» или «5 белок».
- **Выбирать язык:** Библиотека может учитывать языковые предпочтения браузера.

## Простой пример

Вот как подключить функции перевода в приложении Streamlit:

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

Вызов `_()` помечает текст, который нужно перевести. `ngettext()` подбирает форму сообщения в зависимости от числа белок, а ползунок позволяет менять это число.

Это только пример кода, а не пошаговая инструкция по настройке. Чтобы запустить локализованное приложение, понадобятся ещё файлы переводов и конфигурация проекта.

## Переключение языка вручную

В этом варианте пользователь сам выбирает язык в меню. Выбор передаётся в `set_preferred_languages()`, и приложение показывает перевод на этом языке:

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

## Попробовать приложение

Посмотрите, как это работает, в [демонстрационном приложении на Streamlit](https://st-gettext-example.streamlit.app/).

Исходный код приложения доступен в [каталоге с примером](https://github.com/insolor/streamlit-gettext/tree/main/example).

## Справочник API

С описанием функций и других интерфейсов библиотеки можно ознакомиться в [справочнике API](api.md).
