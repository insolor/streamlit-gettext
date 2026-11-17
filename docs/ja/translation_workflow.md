# 翻訳のワークフロー

サンプルプロジェクトでは、GNU gettext のカタログファイルを使用します。

- `locale/messages.pot` は、ソースコードから抽出したテンプレートです。
- `locale/<language>/LC_MESSAGES/messages.po` には、各言語の翻訳が含まれます。
- `locale/<language>/LC_MESSAGES/messages.mo` は、アプリが使用するコンパイル済みのカタログです。

gettext 形式は、[Crowdin](https://crowdin.com/) や [Transifex](https://www.transifex.com/) など、多くのオンライン翻訳プラットフォームでサポートされています。[Poedit](https://poedit.net/) などの専用ソフトウェアで `.po` ファイルを編集することもできます。

gettext を使ったアプリの翻訳について詳しくは、[Lokalise のチュートリアル](https://lokalise.com/blog/translating-apps-with-gettext-comprehensive-tutorial/)をご覧ください。

サンプルには、繰り返し行う作業のために [Poe the Poet](https://poethepoet.natn.io/) のタスクが定義されています。`example/` ディレクトリから実行してください。これらのタスクは、複数の言語を管理する場合に特に便利です。言語ごとにコマンドを繰り返すことなく、既存のすべての言語カタログを一括で更新またはコンパイルできます。

タスクを実行する前に、[GNU gettext](https://www.gnu.org/software/gettext/) と [Poe the Poet](https://poethepoet.natn.io/) をインストールしてください。Poe がまだインストールされていない場合は、次のコマンドを実行します。

```console
uv tool install poethepoet
```

`example/pyproject.toml` では、次のようにタスクが定義されています。

```toml
[tool.poe.tasks]
run = "streamlit run app.py"
extract_pot.shell = "xgettext -d messages -o ./locale/messages.pot *.py --from-code=UTF-8 --no-location"
compile_mo = "find ./locale -name \\*.po -execdir msgfmt messages.po -o messages.mo \\;"
update_po.shell = "find locale -name '*.po' -exec msgmerge -U {} locale/messages.pot \\; && find locale -name '*.po~' -delete"
```

`xgettext` は Python ファイルから共通のテンプレートを作成します。`msgmerge` はそのテンプレートを使って既存のすべての `.po` カタログを更新し、バックアップファイルを削除します。`msgfmt` はすべての `.po` カタログを `.mo` ファイルにコンパイルします。これらのコマンドは GNU gettext に含まれており、Poe はタスクの実行だけを担当します。

## 1. 翻訳するテキストを指定する

ユーザーに表示する文字列を `gettext`（通常は `_` という名前でインポート）で囲みます。単数形と複数形には `ngettext` を使います。例：

```python
st.write(_("Squirrel application"))
ngettext("One squirrel", "%(num)d squirrels", count)
```

## 2. メッセージを抽出する

翻訳対象の文字列を追加または変更したら、メッセージテンプレートを生成します。

```console
poe extract_pot
```

このコマンドは `example/` 内の Python ファイルに対して `xgettext` を実行し、`locale/messages.pot` を更新します。

## 3. カタログを更新して翻訳する

最新のテンプレートを既存のすべての `.po` カタログにマージします。

```console
poe update_po
```

各 `locale/<language>/LC_MESSAGES/messages.po` ファイルを開き、`msgstr` の項目を翻訳してください。`%(num)d` などのプレースホルダーは変更しないでください。複数形のメッセージでは、その言語で必要な各 `msgstr[n]` 形式を翻訳します。

`msgmerge` がカタログを更新するとき、変更された原文が以前の項目と似ている場合、その項目に `fuzzy` フラグが付くことがあります。既存の翻訳が候補として引き継がれますが、正確でなくなっている可能性があります。内容を確認し、`fuzzy` フラグを削除してください。`msgfmt` は fuzzy の項目をスキップするため、フラグが残っている翻訳はアプリで使用できません。

このタスクは既存のカタログを更新します。新しい言語を追加するには、先にその言語の `.po` カタログを作成する必要があります。

## 4. コンパイルして確認する

翻訳したカタログを `.mo` ファイルにコンパイルします。

```console
poe compile_mo
```

次に、サンプルアプリを実行して翻訳を確認します。

```console
poe run
```

ソースの文字列を変更するたびに `poe extract_pot` と `poe update_po` を再実行し、新規または変更された項目を翻訳して、カタログを再度コンパイルしてください。
