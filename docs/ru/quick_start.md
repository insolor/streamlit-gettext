# Быстрый старт

Создадим небольшое приложение с английским исходным текстом, русским переводом, выбором языка и переводами с контекстом и формами числа.

## 1. Установите инструменты

Нужен Python 3.11 или новее. Создайте проект и установите Python-пакеты:

```sh
mkdir localized-app
cd localized-app
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit streamlit-gettext poethepoet
```

Эти команды рассчитаны на Bash в Linux или macOS. В Windows выполняйте всё руководство внутри WSL, включая настройку виртуального окружения, чтобы `poe` и shell-задачи использовали одну среду Linux.

Отдельно установите GNU gettext: в него входят команды `xgettext` и `msgfmt`. Например, в Ubuntu или Debian:

```sh
sudo apt-get install gettext
```

В macOS с Homebrew:

```sh
brew install gettext
```

Для других систем см. [инструкции GNU gettext](https://www.gnu.org/software/gettext/). Все дальнейшие команды выполняйте из `localized-app/` с активированным виртуальным окружением.

## 2. Создайте модуль перевода

Сохраните следующий код в `i18n.py` рядом с `app.py`. Этот модуль — часть вашего приложения, библиотека не создаёт его автоматически.

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

Путь к каталогу вычисляется относительно `i18n.py` и не зависит от рабочего каталога. Домен по умолчанию — `messages`, ему соответствуют файлы `messages.po` и `messages.mo`.

## 3. Создайте приложение

Сохраните код в `app.py`:

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

`gettext` переводит отдельное сообщение, а `ngettext` выбирает форму числа. `pgettext` различает действие «Открыть» и состояние «Открыто» с помощью аргумента контекста. `npgettext` объединяет контекст и выбор формы числа.

Выберите `auto`, чтобы использовать язык браузера, или код языка, чтобы задать его вручную. Передача `None` возвращает автоматическое определение. Ручной выбор хранится отдельно для каждой сессии Streamlit. Исходный текст этого примера английский: при выборе `en` без английского каталога используются исходные сообщения.

## 4. Извлеките и переведите сообщения

Создайте `pyproject.toml` в корне проекта с такими задачами или добавьте секцию в существующий файл:

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

[Poe the Poet](https://poethepoet.natn.io/) запускает команды из этого файла. Параметры нужно записать один раз, а затем достаточно коротких имён задач. GNU gettext по-прежнему должен быть установлен отдельно.

`xgettext` определяет Python по расширению `.py`, учитывает кодировку Python-исходника и по умолчанию распознаёт `_`, `gettext` и `ngettext`. Для переводов с контекстом нужны дополнительные параметры `--keyword`.

Параметры извлечения:

| Параметр | Назначение |
|---|---|
| `--keyword=pgettext:1c,2` | Аргумент 1 — контекст (`c`), аргумент 2 — сообщение. |
| `--keyword=npgettext:1c,2,3` | Аргумент 1 — контекст, аргументы 2 и 3 — обе формы сообщения. |
| `--no-location` | Не записывать позиции строк в каталоге, чтобы перемещение кода не создавало лишних изменений. |
| `--output=locale/messages.pot` | Сохранить общий шаблон сообщений в этот файл. |
| `app.py` | Файл для извлечения сообщений; добавьте сюда другие исходные файлы по мере роста приложения. |

В `init_po` язык передаётся обязательным позиционным аргументом. Задача создаёт `locale/<язык>/LC_MESSAGES` и передаёт язык в `msginit`. Для русского выполните `poe init_po ru`, для японского — `poe init_po ja`: при добавлении языков менять задачи не требуется.

`update_po` и `compile_mo` с помощью `find` обрабатывают все `.po` внутри `locale/`. Первая задача обновляет каталоги из общего шаблона без резервных файлов; вторая проверяет плейсхолдеры форматирования и создаёт `.mo` рядом с каждым `.po`. Выражение `${po%.po}` убирает суффикс `.po` перед добавлением `.mo`. Цикл `for po do` обрабатывает пути, переданные командой `find`, а `|| exit` передаёт ошибку gettext наружу. При `-exec … +` команда `find` тоже завершается с ошибкой, если обработка группы файлов не удалась: это позволяет Poe и CI обнаружить сбой. Пути заключены в кавычки для поддержки каталогов с пробелами.

Для этих задач нужны POSIX-оболочка и `find`, доступные в Linux и macOS. В Windows выполняйте руководство внутри WSL.

Создайте общий каталог и извлеките сообщения:

```sh
mkdir -p locale
poe extract_pot
```

Создайте `.po` из шаблона командой:

```sh
poe init_po ru
```

Задача запускает `msginit`: `--input` задаёт шаблон, `--output-file` — новый каталог перевода, `--locale=ru` — язык, а `--no-translator` отключает интерактивный запрос данных переводчика. Команда создаёт записи с пустыми переводами и заполняет заголовок, включая `Language` и `Plural-Forms`.

Выполните `poe init_po <язык>` один раз для каждого нового языка. Последующие вызовы `poe update_po` и `poe compile_mo` обрабатывают все добавленные языки вместе.

Для заполнения переводов можно использовать специализированный редактор, например [Poedit](https://poedit.com/): он позволяет работать с сообщениями и формами числа через интерфейс программы. Многие онлайн-сервисы перевода, включая [Crowdin](https://support.crowdin.com/developer/configuration-file/#gettext-project) и [Transifex](https://help.transifex.com/en/articles/6220794-gettext-po), поддерживают формат `.po` нативно, без преобразования в другой формат.

С такими сервисами можно настроить интеграцию с репозиторием: передавать обновлённые исходные сообщения и получать готовые переводы обратно, например через [интеграцию Crowdin с GitHub](https://support.crowdin.com/github-integration/) или [интеграцию Transifex с GitHub](https://help.transifex.com/en/articles/6265125-github-installation-and-configuration). После получения обновлённых `.po` выполните `poe compile_mo`, чтобы приложение использовало новые переводы.

Откройте `locale/ru/LC_MESSAGES/messages.po` и заполните `msgstr` и `msgstr[n]`. В служебном заголовке (`msgid ""`) установите кодировку UTF-8 и сохраните файл в этой кодировке:

```po
"Content-Type: text/plain; charset=UTF-8\n"
```

Остальные поля заголовка, включая `Plural-Forms`, оставьте сгенерированными. Записи после перевода будут выглядеть так:

```po
msgid "File manager"
msgstr "Файловый менеджер"

msgid "Number of files"
msgstr "Количество файлов"

#, python-format
msgid "%(num)d file"
msgid_plural "%(num)d files"
msgstr[0] "%(num)d файл"
msgstr[1] "%(num)d файла"
msgstr[2] "%(num)d файлов"

msgctxt "action"
msgid "Open"
msgstr "Открыть"

msgctxt "state"
msgid "Open"
msgstr "Открыто"

#, python-format
msgctxt "download"
msgid "Download %(num)d file"
msgid_plural "Download %(num)d files"
msgstr[0] "Скачать %(num)d файл"
msgstr[1] "Скачать %(num)d файла"
msgstr[2] "Скачать %(num)d файлов"
```

`.pot` — извлечённый шаблон, `.po` — редактируемый перевод, `.mo` — скомпилированный каталог, который загружает приложение. Значение `msgctxt` должно совпадать с контекстом в Python-коде. Сохраняйте `%(num)d` без изменений и переводите все формы числа, необходимые для языка. В русском их три; для других языков число форм и выражение `Plural-Forms` могут отличаться.

## 5. Скомпилируйте перевод и запустите приложение

```sh
poe compile_mo
```

Получится такая структура проекта:

```text
localized-app/
├── app.py
├── i18n.py
├── pyproject.toml
└── locale/
    ├── messages.pot
    └── ru/
        └── LC_MESSAGES/
            ├── messages.po
            └── messages.mo
```

Запустите приложение:

```sh
python -m streamlit run app.py
```

Выберите `ru`: заголовок станет «Файловый менеджер». Установите ползунок в положения 1, 2 и 5, чтобы увидеть «1 файл», «2 файла» и «5 файлов». На кнопке будет «Открыть», а в строке состояния — «Открыто». Выберите `en`, чтобы вернуться к английскому исходному тексту, или `auto`, чтобы использовать язык браузера.

Если сообщение осталось английским, проверьте выбранный язык, расположение каталога, домен и пересборку `.mo` после изменения `.po`. Записи с пометкой `fuzzy` пропускаются командой `msgfmt`: проверьте перевод и удалите флаг перед компиляцией. После пересборки каталогов перезапустите Streamlit, чтобы очистить кэш переводов.

## Обновление переводов

После изменения исходных сообщений заново извлеките их и обновите каталог перевода:

```sh
poe extract_pot
poe update_po
```

Переведите новые и изменённые записи, проверьте пометки `fuzzy`, выполните `poe compile_mo` и перезапустите приложение. Команды для примера из репозитория описаны в [процессе перевода](translation_workflow.md), а интерфейсы библиотеки — в [справочнике API](api.md).
