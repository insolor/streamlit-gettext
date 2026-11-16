# 快速入門

建立一個小型應用程式，包含英文原文、繁體中文翻譯、語言選擇器，以及支援語境和複數形式的訊息。

## 1. 安裝工具

請使用 Python 3.11 或更新版本。在終端機中建立專案並安裝 Python 套件：

```sh
mkdir localized-app
cd localized-app
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit streamlit-gettext poethepoet
```

這些指令使用 Linux 或 macOS 上的 Bash。在 Windows 上，請透過使用的命令殼層建立目錄，並在 PowerShell 中執行 `.venv\Scripts\Activate.ps1` 啟用環境。

另外安裝 GNU gettext，它提供 `xgettext` 和 `msgfmt`。例如，在 Ubuntu 或 Debian 上：

```sh
sudo apt-get install gettext
```

在使用 Homebrew 的 macOS 上：

```sh
brew install gettext
```

其他系統請參閱 [GNU gettext 安裝說明](https://www.gnu.org/software/gettext/)。後續指令都應在啟用虛擬環境後，從 `localized-app/` 目錄執行。

## 2. 建立翻譯模組

將下列程式碼儲存為 `i18n.py`，與 `app.py` 放在同一目錄。這個模組屬於你的應用程式，不會由函式庫自動安裝。

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

翻譯目錄的路徑以 `i18n.py` 為基準，因此不受工作目錄影響。預設的訊息網域為 `messages`，對應 `messages.po` 和 `messages.mo`。

## 3. 建立應用程式

將以下程式碼儲存為 `app.py`：

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

`gettext` 翻譯單一訊息。`ngettext` 選擇複數形式。`pgettext` 透過語境引數，區分作為操作的「Open」和作為狀態的「Open」。`npgettext` 結合語境與複數形式的選擇。

選擇 `auto` 使用瀏覽器語言，或選擇語言代碼手動指定。傳入 `None` 即可恢復偵測瀏覽器語言。手動選擇會針對每個 Streamlit 工作階段分別儲存。這個範例的原文是英文，因此在沒有英文翻譯目錄時，`en` 會使用原始訊息。

## 4. 擷取並翻譯訊息

在專案根目錄建立 `pyproject.toml`，加入以下任務；也可以將這個區段加到既有檔案中：

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

[Poe the Poet](https://poethepoet.natn.io/) 會執行儲存在此檔案中的指令。選項只需寫一次，之後使用簡短的任務名稱即可。GNU gettext 仍需另外安裝。

`xgettext` 透過 `.py` 副檔名辨識 Python，處理 Python 原始碼的編碼，並預設辨識 `_`、`gettext` 和 `ngettext`。含語境的呼叫需要額外的 `--keyword` 選項。

擷取選項：

| 選項 | 用途 |
|---|---|
| `--keyword=pgettext:1c,2` | 第 1 個引數是語境（`c`），第 2 個引數是訊息。 |
| `--keyword=npgettext:1c,2,3` | 第 1 個引數是語境，第 2、3 個引數是單數與複數訊息。 |
| `--no-location` | 不記錄原始碼位置，減少移動程式碼時產生的目錄變更。 |
| `--output=locale/messages.pot` | 將共用訊息範本寫入此檔案。 |
| `app.py` | 要掃描的原始碼檔案；隨應用程式擴充，可在此加入其他檔案。 |

`init_po` 接受一個必填的位置引數來指定語言。任務會建立 `locale/<language>/LC_MESSAGES`，並將語言傳給 `msginit`。繁體中文使用 `poe init_po zh_TW`，日文使用 `poe init_po ja`；新增語言時不必修改任務。

`update_po` 和 `compile_mo` 使用 `find` 處理 `locale/` 下的所有 `.po` 檔案。前者會依共用範本更新所有翻譯目錄，不建立備份檔；後者會檢查格式預留位置，並在每個 `.po` 旁產生 `.mo`。`${po%.po}` 會先移除 `.po` 後綴，再加上 `.mo`。`for po do` 處理 `find` 傳入的路徑，`|| exit` 將 gettext 的錯誤傳回呼叫端。使用 `-exec … +` 時，如果一批檔案處理失敗，`find` 也會傳回錯誤，讓 Poe 和 CI 偵測到失敗。路徑使用引號包住，以支援含空格的目錄名稱。

這些 shell 任務需要 POSIX 命令殼層和 `find`，Linux 和 macOS 均提供這些工具。在 Windows 上，請使用 WSL 或其他提供這些工具的環境。

建立共用目錄並擷取訊息：

```sh
mkdir -p locale
poe extract_pot
```

從範本建立 `.po` 檔案：

```sh
poe init_po zh_TW
```

此任務會執行 `msginit`：`--input` 指定範本，`--output-file` 指定新的翻譯目錄檔案，`--locale=zh_TW` 設定語言，而 `--no-translator` 關閉互動式的譯者資訊詢問。指令會建立尚未填入翻譯的項目，並初始化包含 `Language` 和 `Plural-Forms` 的標頭。

每新增一種語言，只需執行一次 `poe init_po <language>`。之後的 `poe update_po` 和 `poe compile_mo` 會一併處理所有已新增的語言。

你可以用 [Poedit](https://poedit.com/) 等專用編輯器填寫翻譯，透過介面編輯訊息和複數形式。許多線上翻譯服務，包括 [Crowdin](https://support.crowdin.com/developer/configuration-file/#gettext-project) 和 [Transifex](https://help.transifex.com/en/articles/6220794-gettext-po)，都原生支援 `.po`，不必轉換成其他格式。

也可以設定這些服務與儲存庫的整合，傳送更新後的原文並取得完成的翻譯，例如使用 [Crowdin 的 GitHub 整合](https://support.crowdin.com/github-integration/)或 [Transifex 的 GitHub 整合](https://help.transifex.com/en/articles/6265125-github-installation-and-configuration)。收到更新後的 `.po` 檔案時，執行 `poe compile_mo`，讓應用程式使用新翻譯。

開啟 `locale/zh_TW/LC_MESSAGES/messages.po`，填入 `msgstr` 和 `msgstr[n]`。在中繼資料標頭（`msgid ""`）中將字元集設為 UTF-8，並填入中文的複數規則。如果 `msginit` 留下 `INTEGER` 或 `EXPRESSION` 預留值，請以下列內容替換對應欄位，並以 UTF-8 編碼儲存檔案：

```po
"Content-Type: text/plain; charset=UTF-8\n"
"Plural-Forms: nplurals=1; plural=0;\n"
```

保留其他自動產生的標頭欄位。上面的 `Plural-Forms` 表示所有數量都使用同一種形式。翻譯後的項目如下：

```po
msgid "File manager"
msgstr "檔案管理員"

msgid "Number of files"
msgstr "檔案數量"

#, python-format
msgid "%(num)d file"
msgid_plural "%(num)d files"
msgstr[0] "%(num)d 個檔案"

msgctxt "action"
msgid "Open"
msgstr "開啟"

msgctxt "state"
msgid "Open"
msgstr "已開啟"

#, python-format
msgctxt "download"
msgid "Download %(num)d file"
msgid_plural "Download %(num)d files"
msgstr[0] "下載 %(num)d 個檔案"
```

`.pot` 是擷取出的範本，`.po` 是可編輯的翻譯，`.mo` 是應用程式載入的編譯後目錄。`msgctxt` 必須與 Python 呼叫中的語境一致。請保留 `%(num)d` 不變，並翻譯該語言所需的所有複數形式。中文不區分單複數，只需要一種形式；其他語言可能需要不同數量的形式和不同的 `Plural-Forms` 運算式。

## 5. 編譯並執行

```sh
poe compile_mo
```

專案現在的結構如下：

```text
localized-app/
├── app.py
├── i18n.py
├── pyproject.toml
└── locale/
    ├── messages.pot
    └── zh_TW/
        └── LC_MESSAGES/
            ├── messages.po
            └── messages.mo
```

啟動應用程式：

```sh
python -m streamlit run app.py
```

選擇 `zh_TW`：標題應變為「檔案管理員」。將滑桿設為 1、2、5，分別查看「1 個檔案」、「2 個檔案」和「5 個檔案」。按鈕顯示「開啟」，狀態顯示「已開啟」。選擇 `en` 回到英文原文，選擇 `auto` 使用瀏覽器語言。

如果訊息仍是英文，請檢查所選語言、目錄位置、訊息網域，以及編輯 `.po` 後是否重新編譯 `.mo`。`msgfmt` 會略過標記為 `fuzzy` 的項目：請檢查翻譯，並在編譯前移除標記。重新編譯目錄後，請重新啟動 Streamlit 以清除翻譯快取。

## 持續更新翻譯

修改原文訊息後，重新擷取並更新翻譯目錄：

```sh
poe extract_pot
poe update_po
```

翻譯新增或變更的項目，檢查 `fuzzy` 標記，執行 `poe compile_mo`，然後重新啟動應用程式。儲存庫範例的任務請參閱[翻譯工作流程](translation_workflow.md)，函式庫介面請參閱 [API 參考](api.md)。
