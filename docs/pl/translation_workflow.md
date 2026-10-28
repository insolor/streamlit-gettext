# Praca z tłumaczeniami

W przykładzie używane są katalogi GNU gettext:

- `locale/messages.pot` — szablon z tekstami zebranymi z kodu źródłowego.
- `locale/<język>/LC_MESSAGES/messages.po` — tłumaczenia dla danego języka.
- `messages.mo` — skompilowany katalog używany przez aplikację.

Format gettext obsługuje wiele internetowych platform tłumaczeniowych, takich jak [Crowdin](https://crowdin.com/) i [Transifex](https://www.transifex.com/). Pliki `.po` można też edytować w specjalnych programach, na przykład [Poedit](https://poedit.net/).

Szczegółowy przewodnik po tłumaczeniu aplikacji za pomocą gettext znajdziesz w [artykule Lokalise](https://lokalise.com/blog/translating-apps-with-gettext-comprehensive-tutorial/). To odnośnik do przydatnego poradnika, a nie reklama.

W projekcie przykładowym skonfigurowano zadania [Poe the Poet](https://poethepoet.natn.io/) automatyzujące powtarzalne czynności. Uruchamiaj je z katalogu `example/`. Są szczególnie przydatne, gdy aplikacja obsługuje kilka języków: aktualizują lub kompilują katalogi wszystkich języków za jednym razem, bez konieczności powtarzania poleceń dla każdego języka.

Przed uruchomieniem zainstaluj Poe i narzędzia GNU gettext: `xgettext`, `msgmerge` oraz `msgfmt`. Jeśli Poe nie jest jeszcze zainstalowane, użyj polecenia:

```console
uv tool install poethepoet
```

Takie definicje zadań znajdują się w pliku `example/pyproject.toml`:

```toml
[tool.poe.tasks]
run = "streamlit run app.py"
xgettext.shell = "xgettext -d messages -o ./locale/messages.pot *.py --from-code=UTF-8 --no-location"
msgfmt = "find ./locale -name \\*.po -execdir msgfmt messages.po -o messages.mo \\;"
msgmerge.shell = "find locale -name '*.po' -exec msgmerge -U {} locale/messages.pot \\; && find locale -name '*.po~' -delete"
```

`xgettext` zbiera teksty z plików Pythona do wspólnego szablonu. `msgmerge` aktualizuje na jego podstawie wszystkie istniejące katalogi `.po` i usuwa pliki kopii zapasowych, a `msgfmt` kompiluje katalogi `.po` do plików `.mo`. Poe jedynie uruchamia zadania — same polecenia korzystają z narzędzi GNU gettext.

## 1. Oznacz tekst do tłumaczenia

Obejmuj tekst widoczny dla użytkownika funkcją `gettext` (zwykle importowaną jako `_`). Do obsługi liczby pojedynczej i mnogiej używaj `ngettext`. Na przykład:

```python
st.write(_("Some text"))
ngettext("One squirrel", "%(num)d squirrels", count)
```

## 2. Zbierz teksty z kodu

Po dodaniu lub zmianie tekstów do tłumaczenia utwórz szablon komunikatów:

```console
poe xgettext
```

To polecenie uruchamia `xgettext` dla plików Pythona w katalogu `example/` i aktualizuje `locale/messages.pot`.

## 3. Zaktualizuj katalogi i dodaj tłumaczenia

Połącz najnowszy szablon ze wszystkimi istniejącymi katalogami `.po`:

```console
poe msgmerge
```

Otwórz pliki `locale/<język>/LC_MESSAGES/messages.po` i przetłumacz wartości `msgstr`. Nie zmieniaj znaczników takich jak `%(num)d`. W przypadku komunikatów w liczbie mnogiej przetłumacz wszystkie formy `msgstr[n]` wymagane dla danego języka.

Zadanie aktualizuje istniejące katalogi. Aby dodać nowy język, najpierw utwórz dla niego plik `.po`.

## 4. Skompiluj tłumaczenia i sprawdź wynik

Skompiluj przetłumaczone katalogi do plików `.mo`:

```console
poe msgfmt
```

Uruchom przykład i sprawdź tłumaczenia w aplikacji:

```console
poe run
```

Po zmianie tekstów źródłowych ponownie uruchom `poe xgettext` i `poe msgmerge`, przetłumacz nowe lub zmienione wpisy, a następnie ponownie skompiluj katalogi.
