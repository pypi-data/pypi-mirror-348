"""
ORYUM STACK CLI - Comando para criar novo projeto
"""
import typer
import os
from pathlib import Path
from cookiecutter.main import cookiecutter
from oryum_stack.utils.i18n import translate as _
from oryum_stack.config import settings
from oryum_stack.utils.validators import validate_project_name
from oryum_stack.utils.console import console, success, info, error

app = typer.Typer(help=_("Criar um novo projeto Flask"))

@app.callback(invoke_without_command=True)
def new(
    project_name: str = typer.Argument(..., callback=validate_project_name, help=_("Nome do projeto")),
    db_type: str = typer.Option(
        "sqlite", 
        "--db-type", "-d", 
        help=_("Tipo de banco de dados (sqlite/postgresql)"),
        autocompletion=lambda: ["sqlite", "postgresql"]
    ),
    with_oauth: bool = typer.Option(
        False, 
        "--with-oauth", 
        help=_("Incluir autenticação OAuth com Google")
    ),
    admin_theme: str = typer.Option(
        "default", 
        "--admin-theme", 
        help=_("Tema do painel administrativo"),
        autocompletion=lambda: ["default", "modern", "dark"]
    ),
    output_dir: Path = typer.Option(
        os.getcwd(), 
        "--output", "-o",
        help=_("Diretório onde o projeto será criado")
    ),
):
    """
    Cria um novo projeto Flask com autenticação e painel admin.
    """
    with console.status(_("Criando projeto: {0}").format(project_name)):
        try:
            # Preparar contexto para o Cookiecutter
            context = {
                "project_name": project_name,
                "project_slug": project_name.lower().replace(" ", "_").replace("-", "_"),
                "db_type": db_type,
                "with_oauth": "y" if with_oauth else "n",
                "admin_theme": admin_theme,
                "python_version": "3.8",
                "author_name": settings.get("author_name", "Oryum Tech"),
                "author_email": settings.get("author_email", "contato@oryum.com.br"),
            }
            
            # Caminho para o template
            template_path = Path(__file__).parent.parent / "templates" / "project"
            
            # Executar Cookiecutter
            info(_("Configurando estrutura básica..."))
            result_path = cookiecutter(
                str(template_path),
                extra_context=context,
                output_dir=str(output_dir),
                no_input=True
            )
            
            # Configurações específicas baseadas nas opções
            if db_type == "postgresql":
                info(_("Configurando banco de dados PostgreSQL..."))
                # Código para configurar PostgreSQL
            
            if with_oauth:
                info(_("Adicionando autenticação OAuth com Google..."))
                # Código para configurar OAuth
            
            # Instalação de dependências
            info(_("Instalando dependências..."))
            os.chdir(result_path)
            os.system("pip install -r requirements.txt")
            
            # Inicializar banco de dados
            info(_("Inicializando banco de dados..."))
            os.system("python init_db.py")
            
            success(_("Projeto criado com sucesso em: {0}").format(result_path))
            typer.echo(_("Para executar o projeto:"))
            typer.echo(f"cd {project_name}")
            typer.echo("flask run")
            
        except Exception as e:
            error(_("Erro ao criar projeto: {0}").format(str(e)))
            raise typer.Exit(code=1)
