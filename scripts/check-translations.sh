#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

catalog_roots=(example/locale tests/fixtures/locale)
check_dir="$(mktemp -d)"
trap 'rm -rf -- "$check_dir"' EXIT

find "${catalog_roots[@]}" -name '*.po' -type f -print0 > "$check_dir/sources"
find "${catalog_roots[@]}" -name '*.mo' -type f -print0 > "$check_dir/catalogs"

while IFS= read -r -d '' po_file; do
    mo_file="${po_file%.po}.mo"
    if [[ ! -f "$mo_file" ]]; then
        echo "Missing compiled catalog: $mo_file" >&2
        exit 1
    fi

    msgfmt --check-format "$po_file" -o "$check_dir/compiled.mo"
    # Compare catalog contents, allowing different msgfmt versions and hash tables.
    msgunfmt --sort-output --no-wrap "$check_dir/compiled.mo" > "$check_dir/expected.po"
    msgunfmt --sort-output --no-wrap "$mo_file" > "$check_dir/actual.po"
    if ! diff -u "$check_dir/expected.po" "$check_dir/actual.po"; then
        echo "Outdated compiled catalog: $mo_file. Recompile $po_file with msgfmt." >&2
        exit 1
    fi
    echo "OK: $po_file"
done < "$check_dir/sources"

while IFS= read -r -d '' mo_file; do
    if [[ ! -f "${mo_file%.mo}.po" ]]; then
        echo "Missing source catalog for: $mo_file" >&2
        exit 1
    fi
done < "$check_dir/catalogs"
