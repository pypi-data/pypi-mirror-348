import re
import typer

def validate_project_name(value: str):
    if not re.match("^[a-zA-Z_][a-zA-Z0-9_]+$", value):
        raise typer.BadParameter("Nome de projeto inválido. Use apenas letras, números e underscores.")
    return value
