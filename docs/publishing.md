# Publishing PersonaDock standalone releases

PersonaDock is distributed through GitHub Releases as standalone executables. End users install it with `install.sh` or `install.ps1`; no Python environment or package index is required.

## Release assets

Each release contains:

```text
personadock-linux-x86_64.tar.gz
personadock-linux-arm64.tar.gz
personadock-macos-x86_64.tar.gz
personadock-macos-arm64.tar.gz
personadock-windows-x86_64.zip
persona-demo-<version>.personapack
install.sh
install.ps1
SHA256SUMS
LICENSE
```

## Publish a version

The Git tag must match the version in `pyproject.toml`.

For version `0.1.0`:

```bash
git checkout main
git pull origin main
git tag -a v0.1.0 -m "PersonaDock v0.1.0"
git push origin v0.1.0
```

The `Publish PersonaDock release` workflow will:

1. verify that the tag matches the project version
2. run the test suite
3. build Linux x64 and ARM64 standalone executables
4. build macOS Intel and Apple Silicon standalone executables
5. build a Windows x64 standalone executable
6. run each executable and verify the bundled `persona-builder` Skill
7. build and inspect an example PersonaPack
8. generate `SHA256SUMS`
9. create or update the GitHub Release
10. upload the executables, installer scripts, PersonaPack, checksums, and license

## Releasing the next version

Update both:

```text
pyproject.toml
src/persona_dock/__init__.py
```

Then commit and create a matching new tag such as `v0.1.1` or `v0.2.0`.

## Installation checks

Linux or macOS:

```bash
curl -fsSL https://raw.githubusercontent.com/cuteyuchen/PersonaDock/main/install.sh | sh
personadock --help
personadock skill install --target codex --scope global
```

Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/cuteyuchen/PersonaDock/main/install.ps1 | iex
personadock --help
personadock skill install --target codex --scope global
```

To test a specific release:

```bash
PERSONADOCK_VERSION=v0.1.0 sh install.sh
```

```powershell
$env:PERSONADOCK_VERSION = "v0.1.0"
.\install.ps1
```
