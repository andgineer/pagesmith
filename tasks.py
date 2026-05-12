import shutil
import sys
from contextlib import contextmanager
from pathlib import Path
from invoke import Collection, Context, task


DOCS_SRC = Path('docs/src/')


def get_allowed_doc_languages():
    """Detect languages as subfolders in docs/src/

    Ensure `en` is always first.
    """
    return ['en'] + [f.name for f in DOCS_SRC.iterdir() if f.is_dir() and f.name != "en"]


ALLOWED_DOC_LANGUAGES = get_allowed_doc_languages()
ALLOWED_VERSION_TYPES = ["release", "bug", "feature"]


@task
def version(_c: Context):
    """Show the current version."""
    with open("src/pagesmith/__about__.py") as f:
        version_line = f.readline()
        version_num = version_line.split('"')[1]
        print(version_num)
        return version_num


def ver_task_factory(version_type: str):
    @task
    def ver(c: Context):
        """Bump the version."""
        c.run(f"./scripts/verup.sh {version_type}")

    return ver


def reqs(c: Context):
    """Upgrade requirements including pre-commit."""
    c.run("pre-commit autoupdate")
    c.run("uv lock --upgrade")


@contextmanager
def docs_rendered(language: str):
    """Render docs sources for language specified.

    Copy language agnostic assets from en to non-en folders.
    Substitute language and site dir in config copy.

    Returns config copy path.
    """
    config_template_path = Path("docs/mkdocs.yml")
    config_copy_path = Path("docs/_mkdocs.yml")
    reference_master_path = DOCS_SRC / "en" / "reference.md"
    reference_copy_path = DOCS_SRC / language / "reference.md"

    site_dir = "site" if language == "en" else f"site/{language}"

    config = config_template_path.read_text()
    config = config.replace("LANGUAGE", language)
    config = config.replace("SITE_DIR", site_dir)
    try:
        config_copy_path.write_text(config)
        if language != "en":
            shutil.copy2(reference_master_path, reference_copy_path)
        yield config_copy_path
    finally:
        config_copy_path.unlink(missing_ok=True)
        if language != "en":
            reference_copy_path.unlink(missing_ok=True)


def docs_task_factory(language: str):
    @task
    def docs(c: Context):
        """Docs preview for the language specified."""
        with docs_rendered(language) as config_copy_path:
            port = 8001
            c.run(f"open -a 'Google Chrome' http://127.0.0.1:{port}")
            c.run(f"zensical serve --config-file {config_copy_path} --dev-addr localhost:{port}")
    return docs


@task
def build_docs(c: Context):
    """Build docs in docs/site/."""
    for language in ALLOWED_DOC_LANGUAGES:
        with docs_rendered(language) as config_copy_path:
            c.run(f"zensical build --config-file {config_copy_path}")


@task
def uv(c: Context):
    """Install or upgrade uv."""
    c.run("curl -LsSf https://astral.sh/uv/install.sh | sh")


@task
def pre(c):
    """Run pre-commit checks"""
    c.run("pre-commit run --verbose --all-files")


namespace = Collection.from_module(sys.modules[__name__])
for name in ALLOWED_VERSION_TYPES:
    namespace.add_task(ver_task_factory(name), name=f"ver-{name}")  # type: ignore[bad-argument-type]
for name in ALLOWED_DOC_LANGUAGES:
    namespace.add_task(docs_task_factory(name), name=f"docs-{name}")  # type: ignore[bad-argument-type]
