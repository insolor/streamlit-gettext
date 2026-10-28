# 翻译工作流程

示例使用 GNU gettext 翻译目录：

- `locale/messages.pot` 是从源代码中提取文本后生成的模板。
- `locale/<语言>/LC_MESSAGES/messages.po` 保存对应语言的译文。
- `messages.mo` 是应用运行时使用的编译后目录。

许多在线翻译平台都支持 gettext 格式，例如 [Crowdin](https://crowdin.com/) 和 [Transifex](https://www.transifex.com/)。也可以使用专门的软件编辑 `.po` 文件，例如 [Poedit](https://poedit.net/)。

关于使用 gettext 翻译应用的详细教程，请参阅 [Lokalise 指南](https://lokalise.com/blog/translating-apps-with-gettext-comprehensive-tutorial/)。这是有用的参考资料链接，不是广告。

示例项目配置了 [Poe the Poet](https://poethepoet.natn.io/) 任务来自动执行重复操作。请在 `example/` 目录中运行这些任务。它们尤其适用于维护多种语言：一次即可更新或编译所有现有语言目录，无需逐个重复执行命令。

运行任务前，请安装 [GNU gettext](https://www.gnu.org/software/gettext/) 和 [Poe the Poet](https://poethepoet.natn.io/)。如果尚未安装 Poe，可以运行：

```console
uv tool install poethepoet
```

`example/pyproject.toml` 中配置的任务如下：

```toml
[tool.poe.tasks]
run = "streamlit run app.py"
xgettext.shell = "xgettext -d messages -o ./locale/messages.pot *.py --from-code=UTF-8 --no-location"
msgfmt = "find ./locale -name \\*.po -execdir msgfmt messages.po -o messages.mo \\;"
msgmerge.shell = "find locale -name '*.po' -exec msgmerge -U {} locale/messages.pot \\; && find locale -name '*.po~' -delete"
```

`xgettext` 会从 Python 文件中提取字符串并生成共享模板。`msgmerge` 根据模板更新所有现有 `.po` 目录并删除备份文件；`msgfmt` 将每个 `.po` 目录编译为 `.mo` 文件。这些命令属于 GNU gettext，Poe 只负责运行已配置的任务。

## 1. 标记需要翻译的文本

将面向用户的字符串传给 `gettext`（通常导入为 `_`）。单复数形式请使用 `ngettext`。例如：

```python
st.write(_("Some text"))
ngettext("One squirrel", "%(num)d squirrels", count)
```

## 2. 从代码中提取字符串

添加或修改可翻译字符串后，生成消息模板：

```console
poe xgettext
```

此任务会对 `example/` 目录中的 Python 文件运行 `xgettext`，并更新 `locale/messages.pot`。

## 3. 更新目录并添加译文

将最新模板合并到所有现有 `.po` 目录中：

```console
poe msgmerge
```

打开每个 `locale/<语言>/LC_MESSAGES/messages.po` 文件，翻译其中的 `msgstr`。请保留 `%(num)d` 这样的占位符。对于复数消息，请翻译该语言所需的所有 `msgstr[n]` 形式。

此任务会更新已有目录。添加新语言时，请先为其创建 `.po` 文件。

更新目录时，如果源文本发生变化但与旧文本相似，`msgmerge` 可能会将条目标记为 `fuzzy`。旧译文会作为建议保留，但可能不再准确。请检查译文并移除 `fuzzy` 标记：`msgfmt` 会跳过带有该标记的条目，因此应用无法使用这些译文。

## 4. 编译译文并检查结果

将翻译目录编译为 `.mo` 文件：

```console
poe msgfmt
```

启动示例应用并检查译文：

```console
poe run
```

源代码中的字符串发生变化时，请重新运行 `poe xgettext` 和 `poe msgmerge`，翻译新增或变更的条目，然后重新编译目录。
