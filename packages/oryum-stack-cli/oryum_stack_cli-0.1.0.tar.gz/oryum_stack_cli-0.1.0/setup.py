from setuptools import setup, find_packages

setup(
    name="oryum-stack-cli",
    version="0.1.0",
    author="Kalleby Evangelho",
    author_email="kallebyevangelho03@gmail.com",
    description="CLI para gerar projetos Flask com autenticação e painel administrativo",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KallebyX/Oryum_stack_cli",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "oryum_stack": [
            "cli/templates/project/*",
            "cli/templates/snippets/*"
        ]
    },
    install_requires=[
        "typer[all]",
        "cookiecutter",
        "Jinja2",
        "SQLAlchemy",
        "Flask",
        "Flask-Login"
    ],
    entry_points={
        "console_scripts": [
            "oryum=oryum_stack.cli.cli:app"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
