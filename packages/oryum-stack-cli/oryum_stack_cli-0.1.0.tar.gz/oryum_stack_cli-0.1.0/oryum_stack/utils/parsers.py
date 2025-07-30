# oryum_stack/utils/parsers.py

def parse_fields(fields_str):
    """Converte uma string de campos no formato nome:tipo para uma lista de dicionários."""
    if not fields_str:
        return []

    fields = []
    for field_def in fields_str.split(","):
        parts = field_def.split(":")
        field = {
            "name": parts[0],
            "type": parts[1] if len(parts) > 1 else "String",
            "nullable": True,
            "unique": False,
            "length": None,
            "default": None
        }
        fields.append(field)
    return fields

def parse_relationships(relationships_str):
    """Converte uma string de relacionamentos no formato nome:Modelo:tipo."""
    if not relationships_str:
        return []

    relationships = []
    for rel_def in relationships_str.split(","):
        name, model, rel_type = rel_def.split(":")
        relationships.append({
            "name": name,
            "model": model,
            "type": rel_type
        })
    return relationships
