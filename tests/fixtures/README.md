# Translation test catalogs

`locale/` contains small gettext catalogs for testing context, plural forms,
custom domains, and language fallback chains. The compiled `.mo` files are
committed so running the tests does not require GNU gettext.

After editing a `.po` file, regenerate the catalogs from `tests/`:

```sh
msgfmt --check-format fixtures/locale/ru/LC_MESSAGES/testing.po -o fixtures/locale/ru/LC_MESSAGES/testing.mo
msgfmt --check-format fixtures/locale/fr/LC_MESSAGES/testing.po -o fixtures/locale/fr/LC_MESSAGES/testing.mo
```
