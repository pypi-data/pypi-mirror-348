"""
ORYUM STACK CLI - Ponto de entrada principal
"""
import typer
from typing import Optional
from oryum_stack import __version__
from oryum_stack.cli.commands import new, make_model
from oryum_stack.utils.i18n import translate as _

# Aplicação principal
app = typer.Typer(
    name="oryum",
    help=_("Ferramenta para criação de projetos Flask com autenticação e painel admin"),
    add_completion=True,  # Habilita autocompleção no shell
)

# Registrar grupos de comandos como subcomandos
app.add_typer(new.app, name="new")

# Registrar comandos individuais
app.command(name="make:model")(make_model.make_model)
# app.command(name="make:route")(make_route.make_route)
# app.command(name="make:api")(make_api.make_api)

# Callback principal para opções globais
@app.callback()
def main(
    version: bool = typer.Option(False, "--version", "-v", help=_("Mostrar versão")),
    verbose: bool = typer.Option(False, "--verbose", help=_("Modo verboso")),
    config: Optional[str] = typer.Option(None, "--config", "-c", help=_("Arquivo de configuração"))
):
    """
    ORYUM STACK CLI: Gerador de projetos Flask com autenticação e painel admin.
    """
    from oryum_stack.config import settings
    
    # Configurar modo verboso
    if verbose:
        settings.set("verbose", True)
    
    # Carregar configuração personalizada
    if config:
        settings.load_from_file(config)
    
    # Mostrar versão e sair
    if version:
        typer.echo(f"ORYUM STACK CLI v{__version__}")
        raise typer.Exit()
