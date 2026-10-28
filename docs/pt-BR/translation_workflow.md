# Fluxo de trabalho de tradução

O exemplo usa catálogos do GNU gettext:

- `locale/messages.pot` é o modelo com os textos extraídos do código-fonte.
- `locale/<idioma>/LC_MESSAGES/messages.po` contém as traduções de um idioma.
- `messages.mo` é o catálogo compilado usado pelo aplicativo.

O formato gettext é compatível com muitas plataformas de tradução on-line, como [Crowdin](https://crowdin.com/) e [Transifex](https://www.transifex.com/). Também é possível editar arquivos `.po` em programas específicos, como o [Poedit](https://poedit.net/).

Para um guia mais detalhado sobre a tradução de aplicativos com gettext, consulte o [tutorial da Lokalise](https://lokalise.com/blog/translating-apps-with-gettext-comprehensive-tutorial/). É um link para um guia útil, não um anúncio.

O projeto de exemplo inclui tarefas do [Poe the Poet](https://poethepoet.natn.io/) para automatizar etapas repetitivas. Execute-as no diretório `example/`. Elas são especialmente úteis quando o aplicativo tem vários idiomas: atualizam ou compilam todos os catálogos existentes de uma só vez, sem repetir os comandos para cada idioma.

Antes de executar as tarefas, instale o [GNU gettext](https://www.gnu.org/software/gettext/) e o [Poe the Poet](https://poethepoet.natn.io/). Se o Poe ainda não estiver instalado, use:

```console
uv tool install poethepoet
```

Estas são as definições de tarefas usadas em `example/pyproject.toml`:

```toml
[tool.poe.tasks]
run = "streamlit run app.py"
xgettext.shell = "xgettext -d messages -o ./locale/messages.pot *.py --from-code=UTF-8 --no-location"
msgfmt = "find ./locale -name \\*.po -execdir msgfmt messages.po -o messages.mo \\;"
msgmerge.shell = "find locale -name '*.po' -exec msgmerge -U {} locale/messages.pot \\; && find locale -name '*.po~' -delete"
```

`xgettext` reúne as mensagens dos arquivos Python em um modelo comum. `msgmerge` atualiza todos os catálogos `.po` existentes usando esse modelo e remove arquivos de backup; `msgfmt` compila cada catálogo `.po` em um arquivo `.mo`. Esses comandos fazem parte do GNU gettext; o Poe apenas executa as tarefas configuradas.

## 1. Marque o texto para tradução

Envolva as frases exibidas para o usuário com `gettext` (geralmente importado como `_`). Para singular e plural, use `ngettext`. Por exemplo:

```python
st.write(_("Some text"))
ngettext("One squirrel", "%(num)d squirrels", count)
```

## 2. Extraia as mensagens do código

Depois de adicionar ou alterar textos traduzíveis, gere o modelo de mensagens:

```console
poe xgettext
```

A tarefa executa `xgettext` nos arquivos Python do diretório `example/` e atualiza `locale/messages.pot`.

## 3. Atualize os catálogos e traduza

Mescle o modelo mais recente em todos os catálogos `.po` existentes:

```console
poe msgmerge
```

Abra cada arquivo `locale/<idioma>/LC_MESSAGES/messages.po` e traduza os valores de `msgstr`. Não altere marcadores como `%(num)d`. Para mensagens no plural, traduza todas as formas `msgstr[n]` necessárias para o idioma.

Ao atualizar um catálogo, `msgmerge` pode marcar uma entrada como `fuzzy` se o texto original mudou, mas ainda se parece com o anterior. A tradução existente é mantida como sugestão, mas pode não ser mais adequada. Revise-a e remova a marca `fuzzy`: o `msgfmt` ignora essas entradas, que por isso não ficam disponíveis no aplicativo.

A tarefa atualiza os catálogos existentes. Para adicionar um idioma, primeiro crie o arquivo `.po` correspondente.

## 4. Compile as traduções e confira o resultado

Compile os catálogos traduzidos em arquivos `.mo`:

```console
poe msgfmt
```

Inicie o exemplo e confira as traduções no aplicativo:

```console
poe run
```

Quando os textos do código mudarem, execute novamente `poe xgettext` e `poe msgmerge`, traduza as entradas novas ou alteradas e compile os catálogos outra vez.
