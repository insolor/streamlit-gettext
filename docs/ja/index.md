# streamlit-gettext ドキュメント

`streamlit-gettext` は、アプリを多言語化するための Streamlit 拡張機能です。ブラウザーの優先言語に基づいて、ユーザーに翻訳されたテキストを表示できます。

アプリの起動時に一度だけブラウザーの言語を読み取ると、その値がすべてのユーザーに再利用され、最初にアプリを開いた人の言語が全員に表示される場合があります。`streamlit-gettext` は、メッセージを翻訳するたびに現在のユーザーのブラウザー言語を確認することで、この問題を回避します。これにより、同じデプロイ済みアプリを利用するユーザーごとに異なる言語を表示できます。

このプロジェクトは開発中のため、一部の機能や手順は変更される可能性があります。

## 主な機能

- **テキストの翻訳：** 通常は `_` という名前でインポートする `gettext` を使って、翻訳するテキストを指定します。
- **単数形と複数形への対応：** `ngettext` を使って、数量に応じた適切なメッセージ形式を選択します。
- **さまざまな言語設定への対応：** ブラウザーの優先言語に合った翻訳をユーザーに表示します。

## 基本的な使い方

次の例は、Streamlit アプリでこの拡張機能の翻訳関数を使う方法を示しています。

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

この例では、`_()` で翻訳するテキストを指定します。`ngettext()` は単数形と複数形のメッセージを処理し、スライダーでアプリに表示する数量を変更します。

これは使用例であり、セットアップ手順のすべてを説明するものではありません。多言語対応のアプリを実行するには、翻訳ファイルとプロジェクトの設定も必要です。

## 手動で言語を切り替える

次の例では言語セレクターを追加しています。選択した言語を `set_preferred_languages()` に渡すことで、その言語の翻訳をアプリで使用します。

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

## サンプルを試す

[公開されている Streamlit のサンプル](https://st-gettext-example.streamlit.app/)で、実際の動作を確認できます。

詳しくは、[サンプルのソースコード](https://github.com/insolor/streamlit-gettext/tree/main/example)をご覧ください。

## API リファレンス

プロジェクトで公開されているインターフェースの詳細は、[API リファレンス](api.md)をご覧ください。
