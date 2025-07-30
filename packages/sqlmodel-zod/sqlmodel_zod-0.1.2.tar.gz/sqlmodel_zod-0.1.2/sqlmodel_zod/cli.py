import ast
import os
import argparse
from typing import Any, Dict, List, Union

# Define a mapping from SQLModel field types to Zod schema types
TYPE_MAPPING = {
    "str": "z.string()",
    "int": "z.number().int()",
    "float": "z.number()",
    "bool": "z.boolean()",
    "datetime.datetime": "z.date()",
    "list[str]": "z.array(z.string())",
    "list[int]": "z.array(z.number().int())",
    "list[float]": "z.array(z.number())",
    "list[bool]": "z.array(z.boolean())",
    "list[datetime.datetime]": "z.array(z.date())",
    "list[list[str]]": "z.array(z.array(z.string()))",
    "list[list[int]]": "z.array(z.array(z.number().int()))",
    "list[list[float]]": "z.array(z.array(z.number()))",
    "list[list[bool]]": "z.array(z.array(z.boolean()))",
    "list[list[datetime.datetime]]": "z.array(z.array(z.date()))",
    "list[Optional[str]]": "z.array(z.string().optional())",
    "list[Optional[int]]": "z.array(z.number().int().optional())",
    "list[Optional[float]]": "z.array(z.number().optional())",
    "list[Optional[bool]]": "z.array(z.boolean().optional())",
    "list[Optional[datetime.datetime]]": "z.array(z.date().optional())",
    "Optional[str]": "z.string().optional()",
    "Optional[int]": "z.number().int().optional()",
    "Optional[float]": "z.number().optional()",
    "Optional[bool]": "z.boolean().optional()",
    "Optional[datetime.datetime]": "z.date().optional()",
    "Optional[list[str]]": "z.array(z.string()).optional()",
    "Optional[list[int]]": "z.array(z.number().int()).optional()",
    "Optional[list[float]]": "z.array(z.number()).optional()",
    "Optional[list[bool]]": "z.array(z.boolean()).optional()",
    "Optional[list[datetime.datetime]]": "z.array(z.date()).optional()",
    "Optional[list[list[str]]]": "z.array(z.array(z.string())).optional()",
    "Optional[list[list[int]]]": "z.array(z.array(z.number().int())).optional()",
    "Optional[list[list[float]]]": "z.array(z.array(z.number())).optional()",
    "Optional[list[list[bool]]]": "z.array(z.array(z.boolean())).optional()",
    "Optional[list[list[datetime.datetime]]]": "z.array(z.array(z.date())).optional()",
}


def get_zod_type(sqlmodel_type: str, is_optional: bool) -> str:
    zod_type = TYPE_MAPPING.get(sqlmodel_type, "z.any()")
    if is_optional:
        zod_type += ".optional()"
    return zod_type


def parse_sqlmodel_model(node: ast.ClassDef) -> Dict[str, Any]:
    fields = {}
    for body_item in node.body:
        if isinstance(body_item, ast.AnnAssign):
            field_name = body_item.target.id
            field_type = None
            is_optional = False

            if isinstance(body_item.annotation, ast.Subscript):
                field_type = body_item.annotation.value.id
                is_optional = field_type == "Optional"
                if is_optional and isinstance(
                    body_item.annotation.slice, ast.Subscript
                ):
                    inner_type = body_item.annotation.slice.value.id
                    field_type = f"list[{inner_type}]"
                elif is_optional and isinstance(body_item.annotation.slice, ast.Name):
                    field_type = body_item.annotation.slice.id
                elif isinstance(body_item.annotation.slice, ast.Name):
                    field_type = f"list[{body_item.annotation.slice.id}]"
                elif isinstance(body_item.annotation.slice, ast.Subscript):
                    field_type = f"list[{body_item.annotation.slice.value.id}]"
            elif isinstance(body_item.annotation, ast.Name):
                field_type = body_item.annotation.id

            fields[field_name] = get_zod_type(field_type, is_optional)
    return fields


def generate_zod_schema(model_name: str, fields: Dict[str, str]) -> str:
    fields_str = ",\n    ".join([f"{k}: {v}" for k, v in fields.items()])
    return f"const {model_name}Schema = z.object({{\n    {fields_str}\n}});"


def parse_sqlmodels_from_file(
    file_path: str,
) -> List[Dict[str, Union[str, Dict[str, str]]]]:
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    models = []
    model_names = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and any(
            base.id == "SQLModel" for base in node.bases
        ):
            model_name = node.name
            if model_name not in model_names:
                model_names.append(model_name)
            fields = parse_sqlmodel_model(node)
            models.append(
                {"model_name": model_name, "fields": fields, "parent": "SQLModel"}
            )

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and any(
            base.id in model_names for base in node.bases
        ):
            parent = [
                base.id if base.id in model_names else "SQLModel" for base in node.bases
            ][0]
            model_name = node.name
            if model_name not in model_names:
                model_names.append(model_name)
            fields = parse_sqlmodel_model(node)
            models.append(
                {"model_name": model_name, "fields": fields, "parent": parent}
            )

    for model in models:
        if model["parent"] != "SQLModel":
            parent_model = next(
                (m for m in models if m["model_name"] == model["parent"]), None
            )
            if parent_model:
                model["fields"].update(parent_model["fields"])
    return models


def parse_sqlmodels_from_directory(
    directory_path: str,
) -> List[Dict[str, Union[str, Dict[str, str]]]]:
    all_models = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                models = parse_sqlmodels_from_file(file_path)
                all_models.extend(models)
    return all_models


def main():
    parser = argparse.ArgumentParser(
        description="Generate Zod schemas from SQLModel models."
    )
    parser.add_argument(
        "sqlmodel_directory_path",
        type=str,
        help="Path to the directory containing SQLModel models",
    )

    args = parser.parse_args()

    sqlmodel_directory_path = args.sqlmodel_directory_path
    output_file = "zod_schemas.js"

    # Your existing logic here
    models = parse_sqlmodels_from_directory(sqlmodel_directory_path)
    with open(output_file, "w") as f:
        for model in models:
            model_name = model["model_name"]
            fields = model["fields"]
            zod_schema = generate_zod_schema(model_name, fields)
            f.write(zod_schema)
            f.write("\n\n")


# The entry point for the CLI
if __name__ == "__main__":
    main()
