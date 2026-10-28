# Documentação do streamlit-gettext

`streamlit-gettext` é uma extensão para Streamlit que facilita a localização de aplicativos. A biblioteca considera as preferências de idioma do navegador e exibe a tradução adequada para cada pessoa.

O projeto ainda está em desenvolvimento, então a documentação e os recursos disponíveis podem mudar.

## O que a biblioteca faz?

- **Traduz textos.** Marque as frases que precisam de tradução com `gettext`, geralmente importado com o nome curto `_`.
- **Trata singular e plural.** Use `ngettext` para escolher a forma adequada da mensagem de acordo com a quantidade.
- **Escolhe o idioma.** A biblioteca pode considerar as preferências de idioma do navegador.

## Exemplo simples

Veja como usar as funções de tradução em um aplicativo Streamlit:

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

A chamada `_()` marca o texto que será traduzido. `ngettext()` escolhe a forma da mensagem de acordo com a quantidade de esquilos, e o controle deslizante permite alterar esse número.

Este é apenas um exemplo de código, não um guia completo de configuração. Para executar um aplicativo localizado, também são necessários os arquivos de tradução e a configuração do projeto.

## Troca manual de idioma

Nesta versão, a pessoa escolhe o idioma em um menu. A seleção é passada para `set_preferred_languages()` para que o aplicativo exiba a tradução correspondente:

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

## Experimente o aplicativo

Veja como funciona no [aplicativo de demonstração no Streamlit](https://st-gettext-example.streamlit.app/).

O código-fonte está disponível no [diretório do exemplo](https://github.com/insolor/streamlit-gettext/tree/main/example).

## Referência da API

Consulte a [referência da API](api.md) para ver a descrição das funções e de outras interfaces da biblioteca.
