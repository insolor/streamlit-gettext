# Швидкий старт

Створимо невеликий застосунок з англійським вихідним текстом, українським перекладом, вибором мови та повідомленнями з контекстом і формами числа.

## 1. Установіть інструменти

Потрібен Python 3.11 або новіший. У терміналі створіть проєкт і встановіть пакети Python:

```sh
mkdir localized-app
cd localized-app
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit streamlit-gettext poethepoet
```

These shell commands use Bash on Linux or macOS. On Windows, run the entire guide inside WSL, including virtual environment setup, so `poe` and the shell tasks use the same Linux environment.

Окремо встановіть GNU gettext: він містить `xgettext` і `msgfmt`. Наприклад, в Ubuntu або Debian:

```sh
sudo apt-get install gettext
```

У macOS з Homebrew:

```sh
brew install gettext
```

Для інших систем дивіться [інструкції зі встановлення GNU gettext](https://www.gnu.org/software/gettext/). Усі подальші команди виконуйте з `localized-app/` з активованим віртуальним середовищем.

## 2. Створіть модуль перекладу

Збережіть наведений код у `i18n.py` поруч із `app.py`. Цей модуль належить вашому застосунку; бібліотека не встановлює його автоматично.

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

Шлях до каталогу перекладів визначається відносно `i18n.py`, тому не залежить від робочого каталогу. Типовий домен — `messages`, йому відповідають файли `messages.po` і `messages.mo`.

## 3. Створіть застосунок

Збережіть цей код у `app.py`:

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

`gettext` перекладає окреме повідомлення. `ngettext` вибирає форму числа. `pgettext` за допомогою аргументу контексту розрізняє «Open» як дію та «Open» як стан. `npgettext` поєднує контекст і вибір форми числа.

Виберіть `auto`, щоб використовувати мову браузера, або код мови, щоб задати її вручну. Передавання `None` відновлює визначення мови браузера. Ручний вибір зберігається окремо для кожної сесії Streamlit. Вихідні тексти цього прикладу англійські: якщо англійського каталогу немає, `en` використовує оригінальні повідомлення.

## 4. Витягніть і перекладіть повідомлення

Створіть `pyproject.toml` у корені проєкту з такими завданнями або додайте секцію до наявного файлу:

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

[Poe the Poet](https://poethepoet.natn.io/) виконує команди з цього файлу. Параметри потрібно записати один раз, а потім достатньо коротких назв завдань. GNU gettext усе одно потрібно встановити окремо.

`xgettext` визначає Python за розширенням `.py`, враховує кодування Python-коду й типово розпізнає `_`, `gettext` і `ngettext`. Для викликів із контекстом потрібні додаткові параметри `--keyword`.

Параметри витягування:

| Параметр | Призначення |
|---|---|
| `--keyword=pgettext:1c,2` | Аргумент 1 — контекст (`c`), аргумент 2 — повідомлення. |
| `--keyword=npgettext:1c,2,3` | Аргумент 1 — контекст, аргументи 2 і 3 — повідомлення в однині та множині. |
| `--no-location` | Не записувати позиції у вихідному коді, щоб переміщення коду не створювало зайвих змін. |
| `--output=locale/messages.pot` | Зберегти спільний шаблон повідомлень у цей файл. |
| `app.py` | Вихідний файл для аналізу; додавайте інші файли в міру розвитку застосунку. |

`init_po` приймає обов’язковий позиційний аргумент мови. Завдання створює `locale/<language>/LC_MESSAGES` і передає мову до `msginit`. Для української виконайте `poe init_po uk`, для японської — `poe init_po ja`: додавання мов не потребує зміни завдань.

`update_po` і `compile_mo` за допомогою `find` обробляють усі `.po` у `locale/`. Перше завдання оновлює каталоги зі спільного шаблону без резервних файлів; друге перевіряє заповнювачі форматування та створює `.mo` поруч із кожним `.po`. `${po%.po}` прибирає суфікс `.po` перед додаванням `.mo`. Цикл `for po do` обробляє шляхи, передані `find`, а `|| exit` передає помилки gettext назовні. З `-exec … +` команда `find` також завершується з помилкою, якщо обробка групи файлів не вдалася. Це дає змогу Poe та CI виявити збій. Шляхи взято в лапки для підтримки назв каталогів із пробілами.

These shell tasks require a POSIX shell and `find`, available on Linux and macOS. On Windows, run the guide inside WSL.

Створіть спільний каталог і витягніть повідомлення:

```sh
mkdir -p locale
poe extract_pot
```

Створіть файл `.po` із шаблону:

```sh
poe init_po uk
```

Завдання запускає `msginit`: `--input` задає шаблон, `--output-file` — новий каталог перекладів, `--locale=uk` — мову, а `--no-translator` вимикає інтерактивний запит даних перекладача. Команда створює записи з порожніми перекладами й заповнює заголовок, зокрема `Language` і `Plural-Forms`.

Виконайте `poe init_po <language>` один раз для кожної нової мови. Подальші виклики `poe update_po` і `poe compile_mo` обробляють усі додані мови разом.

Для заповнення перекладів можна використовувати спеціалізований редактор, наприклад [Poedit](https://poedit.com/), з інтерфейсом для повідомлень і форм числа. Багато онлайн-сервісів, зокрема [Crowdin](https://support.crowdin.com/developer/configuration-file/#gettext-project) і [Transifex](https://help.transifex.com/en/articles/6220794-gettext-po), підтримують `.po` безпосередньо, без перетворення в інший формат.

Можна налаштувати інтеграцію з репозиторієм для передавання оновлених вихідних повідомлень та отримання готових перекладів, наприклад через [інтеграцію Crowdin із GitHub](https://support.crowdin.com/github-integration/) або [інтеграцію Transifex із GitHub](https://help.transifex.com/en/articles/6265125-github-installation-and-configuration). Після отримання оновлених `.po` виконайте `poe compile_mo`, щоб застосунок використовував нові переклади.

Відкрийте `locale/uk/LC_MESSAGES/messages.po` та заповніть `msgstr` і `msgstr[n]`. У службовому заголовку (`msgid ""`) установіть кодування UTF-8 і збережіть файл у цьому кодуванні:

```po
"Content-Type: text/plain; charset=UTF-8\n"
```

Залиште інші згенеровані поля заголовка, зокрема `Plural-Forms`, без змін. Перекладені записи матимуть такий вигляд:

```po
msgid "File manager"
msgstr "Файловий менеджер"

msgid "Number of files"
msgstr "Кількість файлів"

#, python-format
msgid "%(num)d file"
msgid_plural "%(num)d files"
msgstr[0] "%(num)d файл"
msgstr[1] "%(num)d файли"
msgstr[2] "%(num)d файлів"

msgctxt "action"
msgid "Open"
msgstr "Відкрити"

msgctxt "state"
msgid "Open"
msgstr "Відкрито"

#, python-format
msgctxt "download"
msgid "Download %(num)d file"
msgid_plural "Download %(num)d files"
msgstr[0] "Завантажити %(num)d файл"
msgstr[1] "Завантажити %(num)d файли"
msgstr[2] "Завантажити %(num)d файлів"
```

`.pot` — витягнутий шаблон, `.po` — редагований переклад, `.mo` — скомпільований каталог, який завантажує застосунок. `msgctxt` має відповідати контексту у виклику Python. Не змінюйте `%(num)d` і перекладіть усі форми числа, потрібні для мови. В українській їх три; інші мови можуть потребувати іншої кількості та іншого виразу `Plural-Forms`.

## 5. Скомпілюйте та запустіть

```sh
poe compile_mo
```

Тепер проєкт має таку структуру:

```text
localized-app/
├── app.py
├── i18n.py
├── pyproject.toml
└── locale/
    ├── messages.pot
    └── uk/
        └── LC_MESSAGES/
            ├── messages.po
            └── messages.mo
```

Запустіть застосунок:

```sh
python -m streamlit run app.py
```

Виберіть `uk`: заголовок має змінитися на «Файловий менеджер». Установіть повзунок у положення 1, 2 і 5, щоб побачити «1 файл», «2 файли» та «5 файлів». На кнопці буде «Відкрити», а в рядку стану — «Відкрито». Виберіть `en`, щоб повернутися до англійського тексту, або `auto`, щоб використовувати мову браузера.

Якщо повідомлення лишилося англійським, перевірте вибрану мову, розташування каталогу, домен і чи було перекомпільовано `.mo` після редагування `.po`. `msgfmt` пропускає записи з позначкою `fuzzy`: перевірте переклад і приберіть позначку перед компіляцією. Після перекомпіляції перезапустіть Streamlit, щоб очистити кеш перекладів.

## Оновлення перекладів

Після зміни вихідних повідомлень витягніть їх знову й оновіть каталоги:

```sh
poe extract_pot
poe update_po
```

Перекладіть нові та змінені записи, перевірте позначки `fuzzy`, виконайте `poe compile_mo` і перезапустіть застосунок. Завдання прикладу з репозиторію описані в [процесі перекладу](translation_workflow.md), а інтерфейси бібліотеки — у [довіднику API](api.md).
