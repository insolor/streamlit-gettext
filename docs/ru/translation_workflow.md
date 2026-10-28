# Как работать с переводами

В примере используются файлы каталогов GNU gettext:

- `locale/messages.pot` — шаблон с текстами, извлечёнными из исходного кода.
- `locale/<язык>/LC_MESSAGES/messages.po` — переводы для конкретного языка.
- `messages.mo` — скомпилированный каталог, который использует приложение.

Формат gettext поддерживается многими онлайн-сервисами перевода, например [Crowdin](https://crowdin.com/) и [Transifex](https://www.transifex.com/). Для работы с файлами `.po` также есть специальные редакторы, например [Poedit](https://poedit.net/).

Подробное руководство по переводу приложений с помощью gettext есть в [статье Lokalise](https://lokalise.com/blog/translating-apps-with-gettext-comprehensive-tutorial/).

Для повторяющихся действий в примере настроены задачи [Poe the Poet](https://poethepoet.natn.io/). Запускайте их из каталога `example/`. Эти задачи особенно удобны, когда в приложении несколько языков: они обновляют или компилируют каталоги всех языков за один запуск, поэтому не нужно повторять команды для каждого языка отдельно.

Перед запуском установите Poe и утилиты GNU gettext: `xgettext`, `msgmerge` и `msgfmt`. Если Poe ещё не установлен, это можно сделать командой:

```console
uv tool install poethepoet
```

Именно такие определения задач используются в `example/pyproject.toml`:

```toml
[tool.poe.tasks]
run = "streamlit run app.py"
xgettext.shell = "xgettext -d messages -o ./locale/messages.pot *.py --from-code=UTF-8 --no-location"
msgfmt = "find ./locale -name \\*.po -execdir msgfmt messages.po -o messages.mo \\;"
msgmerge.shell = "find locale -name '*.po' -exec msgmerge -U {} locale/messages.pot \\; && find locale -name '*.po~' -delete"
```

`xgettext` собирает строки из Python-файлов в общий шаблон. `msgmerge` обновляет по нему все существующие каталоги `.po` и удаляет резервные файлы, а `msgfmt` компилирует все каталоги `.po` в файлы `.mo`. Poe только запускает задачи — сами команды используют утилиты GNU gettext.

## 1. Пометьте текст для перевода

Оборачивайте строки, которые увидит пользователь, в `gettext` (обычно импортированную как `_`). Для форм единственного и множественного числа используйте `ngettext`. Например:

```python
st.write(_("Some text"))
ngettext("One squirrel", "%(num)d squirrels", count)
```

## 2. Соберите строки из кода

После добавления или изменения переводимых строк сформируйте шаблон сообщений:

```console
poe xgettext
```

Задача запускает `xgettext` для Python-файлов в каталоге `example/` и обновляет `locale/messages.pot`.

## 3. Обновите каталоги и добавьте переводы

Объедините свежий шаблон со всеми существующими каталогами `.po`:

```console
poe msgmerge
```

Откройте файлы `locale/<язык>/LC_MESSAGES/messages.po` и переведите значения `msgstr`. Не меняйте подстановки вроде `%(num)d`. Для множественных форм переведите все варианты `msgstr[n]`, необходимые для языка.

Задача обновляет уже существующие каталоги. Чтобы добавить новый язык, сначала создайте для него файл `.po`.

## 4. Скомпилируйте переводы и проверьте результат

Скомпилируйте каталоги переводов в файлы `.mo`:

```console
poe msgfmt
```

Запустите пример и проверьте переводы в приложении:

```console
poe run
```

Когда исходные строки изменятся, снова выполните `poe xgettext` и `poe msgmerge`, переведите новые или изменившиеся записи и пересоберите каталоги.
