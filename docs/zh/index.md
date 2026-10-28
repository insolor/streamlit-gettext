# streamlit-gettext 文档

`streamlit-gettext` 是一个用于 Streamlit 的扩展，帮助应用实现本地化。它会参考浏览器的语言偏好，为用户显示相应的译文。

本项目仍在开发中，文档内容和功能可能会有所变化。

## 这个库能做什么？

- **翻译文本。** 使用 `gettext` 标记需要翻译的字符串，通常将它导入为 `_`。
- **处理单复数。** 使用 `ngettext` 根据数量选择合适的消息形式。
- **选择语言。** 库可以参考浏览器的语言偏好。

## 简单示例

下面展示了如何在 Streamlit 应用中使用翻译函数：

```python
import streamlit as st
from i18n import gettext as _
from i18n import ngettext

st.write(_("Some text"))

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

`_()` 用于标记需要翻译的文本。`ngettext()` 会根据松鼠的数量选择合适的消息形式，滑块则可以调整数量。

这只是一个代码示例，并非完整的配置指南。要运行本地化应用，还需要翻译文件和项目配置。

## 手动切换语言

在这个示例中，用户可以从菜单中选择语言。所选语言会传给 `set_preferred_languages()`，应用随后显示相应的译文：

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

st.write(_("Some text"))

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

## 试用示例应用

可以在 [Streamlit 演示应用](https://st-gettext-example.streamlit.app/)中查看运行效果。

示例的源代码位于[示例目录](https://github.com/insolor/streamlit-gettext/tree/main/example)。

## API 参考

函数和其他接口的说明请参阅 [API 参考](api.md)。
