"""Nox configuration to Lint, Format and Test code."""
import os

import nox


@nox.session(reuse_venv=True)
def reformat(session):
    """Reformat using Black."""
    session.install("black")
    session.run("black", ".")


@nox.session(reuse_venv=True)
def lint(session):
    """Lint using Flake8."""
    session.install(
        "flake8",
        "flake8-docstrings",
        "nox",
    )
    if os.path.isfile("requirements.txt"):
        session.install("-r", "requirements.txt")

    session.run("flake8", "--max-complexity=8")
