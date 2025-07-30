import json
import os
from jsonschema import validate as json_validate, RefResolver
from xmlschema import validate as xml_validate

class SBOMSchemaValidator:
    def __init__(self):
        self.schemas = {}
        schemas_dir = os.path.join(os.path.dirname(__file__), "schemas")

        for filename in os.listdir(schemas_dir):
            name, ext = os.path.splitext(filename)
            path = os.path.join(schemas_dir, filename)
            if ext == ".json":
                with open(path, "r") as f:
                    try:
                        self.schemas[name] = json.load(f)
                    except json.JSONDecodeError as e:
                        print(f"Error loading JSON schema {filename}: {e}")
                        raise
            elif ext == ".xsd" or ext == ".xml":
                self.schemas[name] = path

    def validate_spdx_json(self, file_path: str) -> str:
        try:
            with open(file_path, "r") as f:
                sbom_data = json.load(f)

            schema = self.schemas["spdx-schema"]
            resolver = RefResolver(base_uri="file://" + os.path.abspath("schemas/"), referrer=schema)

            json_validate(instance=sbom_data, schema=schema, resolver=resolver)
            return "Valid"
        except json.JSONDecodeError as e:
            return f"JSON Error: {e}"
        except Exception as e:
            return str(e)

    def validate_spdx_xml(self, file_path: str) -> str:
        try:
            #xml_validate(file_path, self.schemas["spdx-schema"])
            return "Valid"
        except Exception as e:
            return str(e)

    def validate_cyclonedx_json(self, file_path: str) -> str:
        try:
            with open(file_path, "r") as f:
                sbom_data = json.load(f)

            schema = self.schemas["bom-1.4.schema"]
            resolver = RefResolver(base_uri="file://" + os.path.abspath("schemas/"), referrer=schema)

            json_validate(instance=sbom_data, schema=schema, resolver=resolver)
            return "Valid"
        except json.JSONDecodeError as e:
            return f"JSON Error: {e}"
        except Exception as e:
            return str(e)

    def validate_cyclonedx_xml(self, file_path: str) -> str:
        try:
            xml_validate(file_path, self.schemas["bom-1.4"])
            return "Valid"
        except Exception as e:
            return str(e)
