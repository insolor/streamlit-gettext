# streamlit-gettext 文件

`streamlit-gettext` 是一個用於 Streamlit 的擴充套件，可協助應用程式實作在地化。它會參考瀏覽器的語言偏好，向使用者顯示相應的翻譯。

如果應用程式只在啟動時讀取一次瀏覽器語言，這個值可能會由所有使用者共用，導致大家看到第一位開啟應用程式的使用者所使用的語言。`streamlit-gettext` 會在每次翻譯訊息時檢查目前使用者的瀏覽器語言，因此同一個執行中的應用程式可以為不同使用者顯示不同語言。

本專案仍在開發中，文件內容和功能可能會有所變動。

## 這個套件可以做什麼？

- **翻譯文字。** 使用 `gettext` 標記需要翻譯的字串，通常會將它匯入為 `_`。
- **處理單複數。** 使用 `ngettext` 根據數量選擇合適的訊息形式。
- **選擇語言。** 套件可以參考瀏覽器的語言偏好。

## 簡單範例

以下示範如何在 Streamlit 應用程式中使用翻譯函式：

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

`_()` 用來標記需要翻譯的文字。`ngettext()` 會根據松鼠的數量選擇合適的訊息形式，滑桿則可用來調整數量。

這只是程式碼範例，並非完整的設定指南。若要執行在地化應用程式，還需要翻譯檔案和專案設定。

## 手動切換語言

在這個範例中，使用者可以從選單選擇語言。所選語言會傳入 `set_preferred_languages()`，讓應用程式顯示相應的翻譯：

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

## 試用範例應用程式

可在 [Streamlit 示範應用程式](https://st-gettext-example.streamlit.app/)查看實際效果。

範例原始碼位於[範例目錄](https://github.com/insolor/streamlit-gettext/tree/main/example)。

## API 參考

函式與其他介面的說明請參閱 [API 參考](api.md)。
