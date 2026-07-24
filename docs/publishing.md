# Publishing PersonaDock to PyPI

PersonaDock uses GitHub Actions and PyPI Trusted Publishing. No long-lived PyPI API token is stored in the repository.

## One-time PyPI setup

1. Sign in to PyPI and verify the account email.
2. Open **Account settings → Publishing**.
3. Add a pending trusted publisher with:

```text
PyPI project name: persona-dock
Owner: cuteyuchen
Repository: PersonaDock
Workflow filename: release.yml
Environment name: pypi
```

The project may be created by the first trusted publication if the name is still available.

## One-time GitHub setup

Open **Repository settings → Environments** and create:

```text
pypi
```

Adding a required reviewer is recommended so a tag cannot publish to PyPI without manual approval.

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

1. verify that `v0.1.0` matches `pyproject.toml`
2. run the test suite
3. build the wheel and source distribution
4. validate both bundled AI editor Skills
5. build and inspect an example PersonaPack
6. publish the Python distributions to PyPI through OIDC
7. create the GitHub Release and upload all release assets

## Releasing the next version

PyPI does not allow replacing files for an already published version. Update both:

```text
pyproject.toml
src/persona_dock/__init__.py
```

Then commit and create a matching new tag such as `v0.1.1` or `v0.2.0`.

## Installation check

After publishing:

```bash
python -m pip install --upgrade persona-dock
personadock --help
personadock skill install --target codex --scope global
```

The default Skill installation should create both:

```text
persona-builder/
persona-distiller/
```
