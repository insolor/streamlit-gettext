# 翻譯工作流程

範例使用 GNU gettext 翻譯目錄：

- `locale/messages.pot` 是從原始碼擷取文字後產生的範本。
- `locale/<語言>/LC_MESSAGES/messages.po` 儲存對應語言的翻譯。
- `messages.mo` 是應用程式執行時使用的編譯目錄。

許多線上翻譯平台都支援 gettext 格式，例如 [Crowdin](https://crowdin.com/) 和 [Transifex](https://www.transifex.com/)。也可以使用專門的軟體編輯 `.po` 檔案，例如 [Poedit](https://poedit.net/)。

若要深入了解如何使用 gettext 翻譯應用程式，請參閱 [Lokalise 指南](https://lokalise.com/blog/translating-apps-with-gettext-comprehensive-tutorial/)。這是實用指南的連結，不是廣告。

範例專案設定了 [Poe the Poet](https://poethepoet.natn.io/) 工作任務，用來自動處理重複步驟。請在 `example/` 目錄中執行這些任務。若應用程式支援多種語言，這些任務特別實用：一次即可更新或編譯所有現有語言目錄，不必逐一重複執行命令。

執行任務前，請安裝 [GNU gettext](https://www.gnu.org/software/gettext/) 和 [Poe the Poet](https://poethepoet.natn.io/)。若尚未安裝 Poe，請執行：

```console
uv tool install poethepoet
```

`example/pyproject.toml` 中使用的任務定義如下：

```toml
[tool.poe.tasks]
run = "streamlit run app.py"
xgettext.shell = "xgettext -d messages -o ./locale/messages.pot *.py --from-code=UTF-8 --no-location"
msgfmt = "find ./locale -name \\*.po -execdir msgfmt messages.po -o messages.mo \\;"
msgmerge.shell = "find locale -name '*.po' -exec msgmerge -U {} locale/messages.pot \\; && find locale -name '*.po~' -delete"
```

`xgettext` 會從 Python 檔案擷取字串並建立共用範本。`msgmerge` 會依據範本更新所有現有 `.po` 目錄並刪除備份檔；`msgfmt` 則會將每個 `.po` 目錄編譯成 `.mo` 檔案。這些命令都包含在 GNU gettext 中，Poe 僅負責執行已設定的任務。

## 1. 標記需要翻譯的文字

將面向使用者的字串傳給 `gettext`（通常匯入為 `_`）。單複數形式請使用 `ngettext`。例如：

```python
st.write(_("Squirrel application"))
ngettext("One squirrel", "%(num)d squirrels", count)
```

## 2. 從程式碼擷取字串

新增或修改可翻譯字串後，請產生訊息範本：

```console
poe xgettext
```

此任務會對 `example/` 目錄中的 Python 檔案執行 `xgettext`，並更新 `locale/messages.pot`。

## 3. 更新目錄並新增翻譯

將最新範本合併至所有現有 `.po` 目錄：

```console
poe msgmerge
```

開啟每個 `locale/<語言>/LC_MESSAGES/messages.po` 檔案，翻譯其中的 `msgstr`。請勿修改 `%(num)d` 這類佔位符。複數訊息請翻譯該語言所需的所有 `msgstr[n]` 形式。

此任務會更新現有目錄。若要新增語言，請先為它建立 `.po` 檔案。

更新目錄時，如果原始文字有所變更但與舊文字相似，`msgmerge` 可能會將項目標記為 `fuzzy`。舊翻譯會保留為建議內容，但可能已不再適用。請檢查翻譯並移除 `fuzzy` 標記：`msgfmt` 會略過這些項目，因此應用程式無法使用它們。

## 4. 編譯翻譯並檢查結果

將翻譯目錄編譯成 `.mo` 檔案：

```console
poe msgfmt
```

啟動範例並檢查應用程式中的翻譯：

```console
poe run
```

原始碼字串變更時，請重新執行 `poe xgettext` 和 `poe msgmerge`，翻譯新增或修改的項目，再重新編譯目錄。
