# クイックスタート

英語の原文、日本語の翻訳、言語セレクター、コンテキストと複数形に対応したメッセージを備える小さなアプリを作成します。

## 1. ツールをインストールする

Python 3.11 以降を使用してください。ターミナルでプロジェクトを作成し、Python パッケージをインストールします。

```sh
mkdir localized-app
cd localized-app
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit streamlit-gettext poethepoet
```

これらのコマンドは Linux または macOS の Bash 用です。Windows では使用するシェルでディレクトリを作成し、PowerShell で `.venv\Scripts\Activate.ps1` を実行して環境を有効にしてください。

`xgettext` と `msgfmt` を提供する GNU gettext も別途インストールします。Ubuntu や Debian では、次のコマンドを使用できます。

```sh
sudo apt-get install gettext
```

macOS で Homebrew を使用する場合：

```sh
brew install gettext
```

その他のシステムについては、[GNU gettext のインストール案内](https://www.gnu.org/software/gettext/)をご覧ください。以降のコマンドは、仮想環境を有効にした状態で `localized-app/` から実行してください。

## 2. 翻訳モジュールを作成する

次のコードを `app.py` と同じディレクトリに `i18n.py` として保存します。このモジュールはアプリの一部であり、ライブラリによってインストールされるものではありません。

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

カタログのパスは `i18n.py` を基準にするため、作業ディレクトリに依存しません。デフォルトのドメインは `messages` で、`messages.po` と `messages.mo` に対応します。

## 3. アプリを作成する

次のコードを `app.py` として保存します。

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

`gettext` は単一のメッセージを翻訳します。`ngettext` は数量に応じた形式を選択します。`pgettext` はコンテキスト引数によって、操作としての「Open」と状態としての「Open」を区別します。`npgettext` はコンテキストと複数形の選択を組み合わせます。

ブラウザーの言語に従う場合は `auto`、手動で指定する場合は言語コードを選択します。`None` を渡すと、ブラウザーからの自動検出に戻ります。手動の設定は Streamlit のセッションごとに保存されます。この例の原文は英語なので、英語のカタログが存在しない場合、`en` は原文のメッセージを使用します。

## 4. メッセージを抽出して翻訳する

プロジェクトのルートに次のタスクを定義した `pyproject.toml` を作成するか、既存のファイルにこのセクションを追加します。

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

[Poe the Poet](https://poethepoet.natn.io/) は、このファイルに保存したコマンドを実行します。オプションを一度記述すれば、以降は短いタスク名で実行できます。GNU gettext は引き続き別途インストールする必要があります。

`xgettext` は拡張子 `.py` から Python を判別し、Python ソースの文字コードを処理します。`_`、`gettext`、`ngettext` はデフォルトで認識されます。コンテキスト付きの呼び出しには、追加の `--keyword` オプションが必要です。

抽出オプション：

| オプション | 用途 |
|---|---|
| `--keyword=pgettext:1c,2` | 第 1 引数はコンテキスト（`c`）、第 2 引数はメッセージです。 |
| `--keyword=npgettext:1c,2,3` | 第 1 引数はコンテキスト、第 2・第 3 引数は単数形と複数形のメッセージです。 |
| `--no-location` | ソースの位置情報を省略し、コード移動によるカタログの変更を減らします。 |
| `--output=locale/messages.pot` | 共通のメッセージテンプレートをこのファイルに書き込みます。 |
| `app.py` | 抽出対象のソースファイルです。アプリの拡張に合わせて他のファイルも追加してください。 |

`init_po` は言語を必須の位置引数として受け取ります。`locale/<language>/LC_MESSAGES` を作成し、その言語を `msginit` に渡します。日本語には `poe init_po ja`、ドイツ語には `poe init_po de` を実行します。言語を追加するたびにタスクを書き換える必要はありません。

`update_po` と `compile_mo` は、`find` で `locale/` 内のすべての `.po` を処理します。前者はバックアップファイルを作成せずに共通テンプレートから全カタログを更新し、後者は書式プレースホルダーを検証して各 `.po` の隣に `.mo` を作成します。`${po%.po}` は `.po` の接尾辞を削除してから `.mo` を付けるための式です。`for po do` は `find` が渡したパスを処理し、`|| exit` は gettext のエラーを呼び出し元に伝えます。`-exec … +` では、処理の一部が失敗すると `find` もエラーを返すため、Poe や CI で失敗を検出できます。パスを引用符で囲むことで、空白を含むディレクトリ名にも対応します。

これらのシェルタスクには、Linux や macOS で利用できる POSIX シェルと `find` が必要です。Windows では WSL など、これらのツールを備えた環境を使用してください。

共通のカタログディレクトリを作成し、メッセージを抽出します。

```sh
mkdir -p locale
poe extract_pot
```

テンプレートから `.po` ファイルを作成します。

```sh
poe init_po ja
```

このタスクは `msginit` を実行します。`--input` はテンプレート、`--output-file` は新しい翻訳カタログ、`--locale=ja` は言語を指定します。`--no-translator` は翻訳者情報の対話的な入力を無効にします。コマンドは翻訳が空の項目を作成し、`Language` や `Plural-Forms` を含むヘッダーを初期化します。

新しい言語ごとに `poe init_po <language>` を一度実行します。以降の `poe update_po` と `poe compile_mo` は、追加済みのすべての言語を一括で処理します。

翻訳の入力には、メッセージや複数形を画面上で編集できる [Poedit](https://poedit.com/) などの専用エディターを使用できます。[Crowdin](https://support.crowdin.com/developer/configuration-file/#gettext-project) や [Transifex](https://help.transifex.com/en/articles/6220794-gettext-po) など、多くのオンライン翻訳サービスも `.po` をネイティブにサポートしており、別形式への変換は不要です。

これらのサービスとリポジトリを連携させることで、更新した原文を送信し、完成した翻訳を取得できます。例えば、[Crowdin の GitHub 連携](https://support.crowdin.com/github-integration/)や [Transifex の GitHub 連携](https://help.transifex.com/en/articles/6265125-github-installation-and-configuration)を設定できます。更新された `.po` を取得したら `poe compile_mo` を実行し、新しい翻訳をアプリで利用できるようにしてください。

`locale/ja/LC_MESSAGES/messages.po` を開き、`msgstr` と `msgstr[n]` に翻訳を入力します。メタデータヘッダー（`msgid ""`）の文字コードを UTF-8 に設定し、ファイルも UTF-8 で保存してください。

```po
"Content-Type: text/plain; charset=UTF-8\n"
```

`Plural-Forms` を含む他の生成済みヘッダーフィールドはそのままにします。翻訳後の項目は次のようになります。

```po
msgid "File manager"
msgstr "ファイルマネージャー"

msgid "Number of files"
msgstr "ファイル数"

#, python-format
msgid "%(num)d file"
msgid_plural "%(num)d files"
msgstr[0] "%(num)d個のファイル"

msgctxt "action"
msgid "Open"
msgstr "開く"

msgctxt "state"
msgid "Open"
msgstr "開いている"

#, python-format
msgctxt "download"
msgid "Download %(num)d file"
msgid_plural "Download %(num)d files"
msgstr[0] "%(num)d個のファイルをダウンロード"
```

`.pot` は抽出したテンプレート、`.po` は編集可能な翻訳、`.mo` はアプリが読み込むコンパイル済みカタログです。`msgctxt` は Python 呼び出しのコンテキストと一致する必要があります。`%(num)d` は変更せず、その言語で必要なすべての形式を翻訳してください。日本語では数量にかかわらず 1 つの形式を使用します。他の言語では、形式の数や `Plural-Forms` の式が異なる場合があります。

## 5. コンパイルして実行する

```sh
poe compile_mo
```

プロジェクトは次の構成になります。

```text
localized-app/
├── app.py
├── i18n.py
├── pyproject.toml
└── locale/
    ├── messages.pot
    └── ja/
        └── LC_MESSAGES/
            ├── messages.po
            └── messages.mo
```

アプリを起動します。

```sh
python -m streamlit run app.py
```

`ja` を選択すると、タイトルが「ファイルマネージャー」に変わります。スライダーを 1、2、5 に設定すると、「1個のファイル」「2個のファイル」「5個のファイル」が表示されます。ボタンには「開く」、状態には「開いている」が表示されます。`en` を選ぶと英語の原文に戻り、`auto` を選ぶとブラウザーの言語を使用します。

メッセージが英語のままの場合は、選択した言語、カタログの場所、ドメイン、および `.po` の編集後に `.mo` を再コンパイルしたかを確認してください。`msgfmt` は `fuzzy` の項目をスキップするため、翻訳を確認してフラグを削除してからコンパイルします。カタログを再コンパイルした後は Streamlit を再起動し、翻訳のキャッシュをクリアしてください。

## 翻訳を更新する

原文のメッセージを変更したら、再度抽出して翻訳カタログを更新します。

```sh
poe extract_pot
poe update_po
```

新規または変更された項目を翻訳し、`fuzzy` の項目を確認して `poe compile_mo` を実行し、アプリを再起動します。リポジトリのサンプルで使うタスクは[翻訳のワークフロー](translation_workflow.md)、ライブラリのインターフェースは [API リファレンス](api.md)をご覧ください。
