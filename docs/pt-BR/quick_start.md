# Início rápido

Crie um pequeno aplicativo com textos originais em inglês, traduções em português do Brasil, um seletor de idioma e mensagens com contexto e formas de plural.

## 1. Instale as ferramentas

Use Python 3.11 ou mais recente. Em um terminal, crie um projeto e instale os pacotes Python:

```sh
mkdir localized-app
cd localized-app
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit streamlit-gettext poethepoet
```

Estes comandos usam Bash no Linux ou macOS. No Windows, siga todo o guia dentro do WSL, incluindo a configuração do ambiente virtual, para que `poe` e as tarefas de shell usem o mesmo ambiente Linux.

Instale o GNU gettext separadamente; ele fornece `xgettext` e `msgfmt`. Por exemplo, no Ubuntu ou Debian:

```sh
sudo apt-get install gettext
```

No macOS com Homebrew:

```sh
brew install gettext
```

Para outros sistemas, consulte as [instruções de instalação do GNU gettext](https://www.gnu.org/software/gettext/). Execute os demais comandos em `localized-app/`, com o ambiente virtual ativado.

## 2. Crie o módulo de tradução

Salve o código abaixo como `i18n.py`, ao lado de `app.py`. Esse módulo pertence ao seu aplicativo; a biblioteca não o instala.

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

O caminho do catálogo é relativo a `i18n.py`, portanto não depende do diretório de trabalho. O domínio padrão é `messages`, correspondente a `messages.po` e `messages.mo`.

## 3. Crie o aplicativo

Salve este código como `app.py`:

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

`gettext` traduz uma mensagem. `ngettext` escolhe uma forma de plural. `pgettext` diferencia a ação “Open” do estado “Open” pelo argumento de contexto. `npgettext` combina contexto e seleção de plural.

Selecione `auto` para seguir o idioma do navegador, ou um código de idioma para substituí-lo. Passar `None` restaura a detecção pelo navegador. As preferências manuais são armazenadas separadamente para cada sessão do Streamlit. Os textos originais deste exemplo estão em inglês: assim, `en` usa as mensagens originais quando não há catálogo em inglês.

## 4. Extraia e traduza as mensagens

Crie `pyproject.toml` na raiz do projeto com estas tarefas, ou adicione a seção a um arquivo existente:

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

[Poe the Poet](https://poethepoet.natn.io/) executa os comandos armazenados nesse arquivo. Você escreve as opções uma vez; depois, basta usar os nomes curtos das tarefas. O GNU gettext ainda precisa ser instalado separadamente.

`xgettext` identifica Python pela extensão `.py`, considera a codificação do código Python e reconhece `_`, `gettext` e `ngettext` por padrão. Chamadas com contexto exigem as opções adicionais `--keyword`.

Opções de extração:

| Opção | Finalidade |
|---|---|
| `--keyword=pgettext:1c,2` | O argumento 1 é o contexto (`c`); o argumento 2 é a mensagem. |
| `--keyword=npgettext:1c,2,3` | O argumento 1 é o contexto; os argumentos 2 e 3 são as mensagens no singular e no plural. |
| `--no-location` | Omitir posições do código-fonte para reduzir alterações quando o código é movido. |
| `--output=locale/messages.pot` | Gravar o modelo compartilhado de mensagens nesse arquivo. |
| `app.py` | Arquivo-fonte a analisar; adicione outros arquivos à medida que o aplicativo crescer. |

`init_po` recebe um argumento posicional obrigatório com o idioma. A tarefa cria `locale/<language>/LC_MESSAGES` e passa o idioma para `msginit`. Execute `poe init_po pt_BR` para português do Brasil ou `poe init_po ja` para japonês; não é necessário editar as tarefas ao adicionar idiomas.

`update_po` e `compile_mo` usam `find` para processar todos os arquivos `.po` em `locale/`. A primeira atualiza os catálogos a partir do modelo compartilhado sem arquivos de backup; a segunda verifica os marcadores de formatação e cria um `.mo` ao lado de cada `.po`. `${po%.po}` remove o sufixo `.po` antes de adicionar `.mo`. `for po do` processa os caminhos passados por `find`, e `|| exit` propaga falhas do gettext. Com `-exec … +`, `find` também retorna erro se um lote falhar, permitindo que Poe e CI detectem o problema. Os caminhos ficam entre aspas para aceitar diretórios com espaços.

Essas tarefas exigem um shell POSIX e `find`, disponíveis no Linux e macOS. No Windows, siga o guia dentro do WSL.

Crie o diretório comum dos catálogos e extraia as mensagens:

```sh
mkdir -p locale
poe extract_pot
```

Crie o arquivo `.po` a partir do modelo:

```sh
poe init_po pt_BR
```

Essa tarefa executa `msginit`: `--input` seleciona o modelo, `--output-file` o novo catálogo, `--locale=pt_BR` o idioma e `--no-translator` desativa perguntas interativas sobre o tradutor. O comando cria entradas com traduções vazias e inicializa o cabeçalho, incluindo `Language` e `Plural-Forms`.

Execute `poe init_po <language>` uma vez para cada novo idioma. As próximas execuções de `poe update_po` e `poe compile_mo` processam todos os idiomas adicionados em conjunto.

Você pode preencher as traduções com um editor especializado, como [Poedit](https://poedit.com/), que oferece uma interface para mensagens e formas de plural. Muitos serviços on-line, incluindo [Crowdin](https://support.crowdin.com/developer/configuration-file/#gettext-project) e [Transifex](https://help.transifex.com/en/articles/6220794-gettext-po), oferecem suporte nativo a `.po`, sem conversão de formato.

É possível configurar uma integração com o repositório para enviar mensagens originais atualizadas e receber traduções prontas, por exemplo pela [integração do Crowdin com GitHub](https://support.crowdin.com/github-integration/) ou pela [integração do Transifex com GitHub](https://help.transifex.com/en/articles/6265125-github-installation-and-configuration). Depois de receber os `.po` atualizados, execute `poe compile_mo` para que o aplicativo use as novas traduções.

Abra `locale/pt_BR/LC_MESSAGES/messages.po` e preencha `msgstr` e `msgstr[n]`. No cabeçalho de metadados (`msgid ""`), defina UTF-8 como codificação e salve o arquivo nessa codificação:

```po
"Content-Type: text/plain; charset=UTF-8\n"
```

Mantenha os demais campos gerados do cabeçalho, incluindo `Plural-Forms`. As entradas traduzidas devem ficar assim:

```po
msgid "File manager"
msgstr "Gerenciador de arquivos"

msgid "Number of files"
msgstr "Número de arquivos"

#, python-format
msgid "%(num)d file"
msgid_plural "%(num)d files"
msgstr[0] "%(num)d arquivo"
msgstr[1] "%(num)d arquivos"

msgctxt "action"
msgid "Open"
msgstr "Abrir"

msgctxt "state"
msgid "Open"
msgstr "Aberto"

#, python-format
msgctxt "download"
msgid "Download %(num)d file"
msgid_plural "Download %(num)d files"
msgstr[0] "Baixar %(num)d arquivo"
msgstr[1] "Baixar %(num)d arquivos"
```

`.pot` é o modelo extraído, `.po` é a tradução editável e `.mo` é o catálogo compilado carregado pelo aplicativo. `msgctxt` deve corresponder ao contexto da chamada Python. Mantenha `%(num)d` sem alterações e traduza todas as formas de plural exigidas pelo idioma. O português do Brasil tem duas formas; outros idiomas podem exigir outra quantidade e outra expressão `Plural-Forms`.

## 5. Compile e execute

```sh
poe compile_mo
```

O projeto agora tem esta estrutura:

```text
localized-app/
├── app.py
├── i18n.py
├── pyproject.toml
└── locale/
    ├── messages.pot
    └── pt_BR/
        └── LC_MESSAGES/
            ├── messages.po
            └── messages.mo
```

Inicie o aplicativo:

```sh
python -m streamlit run app.py
```

Selecione `pt_BR`: o título deve mudar para “Gerenciador de arquivos”. Ajuste o controle deslizante para 1, 2 e 5 para ver “1 arquivo”, “2 arquivos” e “5 arquivos”. O botão mostra “Abrir”, enquanto o estado mostra “Aberto”. Selecione `en` para voltar ao texto original em inglês, ou `auto` para usar o idioma do navegador.

Se uma mensagem continuar em inglês, confira o idioma selecionado, a localização do catálogo, o domínio e se o `.mo` foi recompilado após editar o `.po`. `msgfmt` ignora entradas marcadas como `fuzzy`: revise a tradução e remova a marca antes de compilar. Reinicie o Streamlit após recompilar os catálogos para limpar as traduções em cache.

## Mantenha as traduções atualizadas

Depois de alterar as mensagens originais, extraia-as novamente e atualize os catálogos:

```sh
poe extract_pot
poe update_po
```

Traduza as entradas novas ou alteradas, revise as marcas `fuzzy`, execute `poe compile_mo` e reinicie o aplicativo. Consulte o [fluxo de tradução](translation_workflow.md) para as tarefas do exemplo do repositório, ou a [referência da API](api.md) para as interfaces da biblioteca.
