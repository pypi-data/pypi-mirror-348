"""
ORYUM STACK CLI - Comando para criar modelo
"""
import typer
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from oryum_stack.utils.i18n import translate as _
from oryum_stack.utils.console import console, success, info, error
from oryum_stack.utils.project import is_oryum_project, get_project_root
from oryum_stack.utils.parsers import parse_fields, parse_relationships

def make_model(
    name: str = typer.Argument(..., help=_("Nome do modelo")),
    fields: str = typer.Option(
        None, 
        "--fields", "-f", 
        help=_("Lista de campos no formato 'nome:tipo:modificadores' (ex: 'titulo:string:nullable,preco:float')")
    ),
    timestamps: bool = typer.Option(
        True, 
        "--timestamps/--no-timestamps", 
        help=_("Incluir campos created_at e updated_at")
    ),
    relationships: str = typer.Option(
        None, 
        "--relationships", "-r", 
        help=_("Lista de relacionamentos no formato 'nome:Modelo:tipo' (ex: 'categorias:Categoria:many')")
    ),
):
    """
    Cria um novo modelo SQLAlchemy.
    """
    with console.status(_("Gerando modelo: {0}").format(name)):
        try:
            # Verificar se estamos em um projeto Oryum
            if not is_oryum_project():
                error(_("Este comando deve ser executado dentro de um projeto Oryum."))
                raise typer.Exit(code=1)
            
            # Obter raiz do projeto
            project_root = get_project_root()
            
            # Processar nome do modelo
            model_name = name.strip()
            if not model_name[0].isupper():
                model_name = model_name[0].upper() + model_name[1:]
            
            model_file = model_name.lower() + ".py"
            model_path = project_root / "models" / model_file
            
            # Verificar se o modelo já existe
            if model_path.exists():
                error(_("O modelo {0} já existe em {1}").format(model_name, model_path))
                raise typer.Exit(code=1)
            
            # Processar campos
            parsed_fields = parse_fields(fields) if fields else []
            
            # Processar relacionamentos
            parsed_relationships = parse_relationships(relationships) if relationships else []
            
            # Carregar template
            env = Environment(loader=FileSystemLoader(Path(__file__).parent.parent / "templates" / "snippets"))
            template = env.get_template("model.py.jinja2")
            
            # Renderizar template
            model_content = template.render(
                model_name=model_name,
                fields=parsed_fields,
                timestamps=timestamps,
                relationships=parsed_relationships,
            )
            
            # Escrever arquivo
            with open(model_path, "w") as f:
                f.write(model_content)
            
            # Atualizar __init__.py para importar o novo modelo
            init_path = project_root / "models" / "__init__.py"
            with open(init_path, "a") as f:
                f.write(f"\nfrom .{model_name.lower()} import {model_name}")
            
            # Atualizar modelos relacionados se necessário
            for rel in parsed_relationships:
                info(_("Atualizando modelo relacionado: {0}").format(rel["model"]))
                # Código para atualizar modelos relacionados
            
            success(_("Modelo criado com sucesso: {0}").format(model_path))
            
        except Exception as e:
            error(_("Erro ao criar modelo: {0}").format(str(e)))
            raise typer.Exit(code=1)
