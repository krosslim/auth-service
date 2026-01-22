import json
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).parent.parent.parent


def openapi_postprocess(schema: dict[str, Any]) -> dict[str, Any]:
    paths = schema.get("paths", {})
    for path_item in paths.values():
        for method_item in path_item.values():
            responses = method_item.get("responses")
            if responses and "422" in responses:
                del responses["422"]

            parameters = method_item.get("parameters")
            if parameters and isinstance(parameters, list):
                method_item["parameters"] = sorted(
                    parameters, key=lambda p: (p.get("in") != "header")
                )
    components = schema.get("components", {})
    schemas = components.get("schemas", {})

    unwanted_schemas = {"HTTPValidationError", "ValidationError"}
    for name in unwanted_schemas:
        schemas.pop(name, None)

    if not schemas:
        components.pop("schemas", None)
    if not components:
        schema.pop("components", None)

    return schema


def openapi_docs(scheme: dict[str, Any]) -> None:
    output_dir = PROJECT_ROOT / "docs"
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "auth-service-openapi.json"
    yaml_path = output_dir / "auth-service-openapi.yml"

    try:
        with Path.open(json_path, "w", encoding="utf-8") as f:
            json.dump(scheme, f, indent=2, ensure_ascii=False)

        with Path.open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(
                scheme,
                f,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
                indent=2,
            )

    except OSError as e:
        print(f"OSError: {e}")
    except (TypeError, ValueError) as e:
        print(f"TypeError / ValueError: {e}")


if __name__ == "__main__":
    from src.app.main import app

    spec = app.openapi()
    processed_spec = openapi_postprocess(spec)
    openapi_docs(processed_spec)
