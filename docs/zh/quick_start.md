# 快速入门

创建一个小型应用，包含英文原文、简体中文翻译、语言选择器，以及支持上下文和复数形式的消息。

## 1. 安装工具

请使用 Python 3.11 或更高版本。在终端中创建项目并安装 Python 包：

```sh
mkdir localized-app
cd localized-app
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit streamlit-gettext poethepoet
```

这些命令使用 Linux 或 macOS 上的 Bash。在 Windows 上，请用自己的命令行环境创建目录，并在 PowerShell 中执行 `.venv\Scripts\Activate.ps1` 激活环境。

另行安装 GNU gettext，它提供 `xgettext` 和 `msgfmt`。例如，在 Ubuntu 或 Debian 上：

```sh
sudo apt-get install gettext
```

在使用 Homebrew 的 macOS 上：

```sh
brew install gettext
```

其他系统请参阅 [GNU gettext 安装说明](https://www.gnu.org/software/gettext/)。后续命令均应在已激活虚拟环境的情况下，从 `localized-app/` 目录执行。

## 2. 创建翻译模块

将以下代码保存为 `i18n.py`，与 `app.py` 放在同一目录。此模块属于你的应用，不会由库自动安装。

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

目录路径相对于 `i18n.py`，因此不依赖当前工作目录。默认的消息域是 `messages`，对应 `messages.po` 和 `messages.mo`。

## 3. 创建应用

将以下代码保存为 `app.py`：

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

`gettext` 翻译单条消息。`ngettext` 选择复数形式。`pgettext` 通过上下文参数区分作为操作的“Open”和作为状态的“Open”。`npgettext` 将上下文与复数选择结合起来。

选择 `auto` 使用浏览器语言，或选择语言代码进行手动指定。传入 `None` 可恢复浏览器语言检测。手动选择会按 Streamlit 会话分别保存。本例的原文为英语，因此在没有英语目录时，`en` 使用原始消息。

## 4. 提取并翻译消息

在项目根目录创建 `pyproject.toml`，写入以下任务；也可以将这一节添加到现有文件中：

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

[Poe the Poet](https://poethepoet.natn.io/) 执行此文件中保存的命令。参数只需编写一次，之后使用简短的任务名即可。GNU gettext 仍需单独安装。

`xgettext` 根据 `.py` 扩展名识别 Python，处理 Python 源文件编码，并默认识别 `_`、`gettext` 和 `ngettext`。带上下文的调用需要额外的 `--keyword` 参数。

提取参数：

| 参数 | 用途 |
|---|---|
| `--keyword=pgettext:1c,2` | 第 1 个参数是上下文（`c`），第 2 个参数是消息。 |
| `--keyword=npgettext:1c,2,3` | 第 1 个参数是上下文，第 2、3 个参数是单数和复数消息。 |
| `--no-location` | 不在目录中记录源代码位置，减少移动代码产生的变更。 |
| `--output=locale/messages.pot` | 将共用消息模板写入此文件。 |
| `app.py` | 要扫描的源文件；随着应用扩展，可在此添加其他源文件。 |

`init_po` 接收一个必填的位置参数来指定语言。它创建 `locale/<language>/LC_MESSAGES`，并将语言传给 `msginit`。简体中文使用 `poe init_po zh_CN`，日语使用 `poe init_po ja`；新增语言时无需修改任务。

`update_po` 和 `compile_mo` 使用 `find` 处理 `locale/` 下的所有 `.po` 文件。前者从共用模板更新所有目录，不创建备份文件；后者检查格式占位符，并在每个 `.po` 旁生成 `.mo`。`${po%.po}` 会先移除 `.po` 后缀，再加上 `.mo`。`for po do` 处理 `find` 传入的路径，`|| exit` 将 gettext 的错误向上传递。使用 `-exec … +` 时，如果一批文件处理失败，`find` 也会返回错误，使 Poe 和 CI 能检测到失败。路径使用引号包围，以支持包含空格的目录名。

这些 shell 任务需要 POSIX shell 和 `find`，Linux 和 macOS 均提供这些工具。在 Windows 上，请使用 WSL 或其他提供这些工具的环境。

创建共用目录并提取消息：

```sh
mkdir -p locale
poe extract_pot
```

从模板创建 `.po` 文件：

```sh
poe init_po zh_CN
```

此任务运行 `msginit`：`--input` 指定模板，`--output-file` 指定新的翻译目录文件，`--locale=zh_CN` 设置语言，`--no-translator` 关闭交互式译者信息询问。该命令创建翻译为空的条目，并初始化包括 `Language` 和 `Plural-Forms` 在内的头部信息。

每添加一种语言，只需运行一次 `poe init_po <language>`。之后的 `poe update_po` 和 `poe compile_mo` 会一起处理所有已添加的语言。

可以用 [Poedit](https://poedit.com/) 等专用编辑器填写翻译，通过图形界面编辑消息和复数形式。许多在线翻译服务，包括 [Crowdin](https://support.crowdin.com/developer/configuration-file/#gettext-project) 和 [Transifex](https://help.transifex.com/en/articles/6220794-gettext-po)，都原生支持 `.po`，无需转换为其他格式。

还可以配置这些服务与代码仓库的集成，以发送更新后的原文并接收完成的翻译，例如使用 [Crowdin 的 GitHub 集成](https://support.crowdin.com/github-integration/)或 [Transifex 的 GitHub 集成](https://help.transifex.com/en/articles/6265125-github-installation-and-configuration)。收到更新后的 `.po` 文件后，运行 `poe compile_mo`，让应用使用新翻译。

打开 `locale/zh_CN/LC_MESSAGES/messages.po`，填写 `msgstr` 和 `msgstr[n]`。在元数据头部（`msgid ""`）将字符集设置为 UTF-8，并填写中文的复数规则。如果 `msginit` 留下了 `INTEGER` 或 `EXPRESSION` 占位值，请用以下内容替换相应字段，并以 UTF-8 编码保存文件：

```po
"Content-Type: text/plain; charset=UTF-8\n"
"Plural-Forms: nplurals=1; plural=0;\n"
```

保留其他自动生成的头部字段。上面的 `Plural-Forms` 表示所有数量都使用同一种形式。翻译后的条目如下：

```po
msgid "File manager"
msgstr "文件管理器"

msgid "Number of files"
msgstr "文件数量"

#, python-format
msgid "%(num)d file"
msgid_plural "%(num)d files"
msgstr[0] "%(num)d 个文件"

msgctxt "action"
msgid "Open"
msgstr "打开"

msgctxt "state"
msgid "Open"
msgstr "已打开"

#, python-format
msgctxt "download"
msgid "Download %(num)d file"
msgid_plural "Download %(num)d files"
msgstr[0] "下载 %(num)d 个文件"
```

`.pot` 是提取出的模板，`.po` 是可编辑的翻译，`.mo` 是应用加载的编译后目录。`msgctxt` 必须与 Python 调用中的上下文一致。保持 `%(num)d` 不变，并翻译目标语言所需的所有复数形式。中文不区分单复数，只需要一种形式；其他语言可能需要不同数量的形式和不同的 `Plural-Forms` 表达式。

## 5. 编译并运行

```sh
poe compile_mo
```

现在项目结构如下：

```text
localized-app/
├── app.py
├── i18n.py
├── pyproject.toml
└── locale/
    ├── messages.pot
    └── zh_CN/
        └── LC_MESSAGES/
            ├── messages.po
            └── messages.mo
```

启动应用：

```sh
python -m streamlit run app.py
```

选择 `zh_CN`：标题应变为“文件管理器”。将滑块设置为 1、2、5，分别查看“1 个文件”“2 个文件”和“5 个文件”。按钮显示“打开”，状态显示“已打开”。选择 `en` 返回英文原文，选择 `auto` 使用浏览器语言。

如果某条消息仍显示为英文，请检查所选语言、目录位置、消息域，以及编辑 `.po` 后是否重新编译了 `.mo`。`msgfmt` 会跳过标记为 `fuzzy` 的条目：请检查翻译，并在编译前移除标记。重新编译目录后，请重启 Streamlit 以清除翻译缓存。

## 持续更新翻译

修改原文消息后，再次提取消息并更新翻译目录：

```sh
poe extract_pot
poe update_po
```

翻译新增或修改的条目，检查 `fuzzy` 标记，运行 `poe compile_mo` 并重启应用。仓库示例的任务请参阅[翻译工作流程](translation_workflow.md)，库接口请参阅 [API 参考](api.md)。
