import argparse
import sys
from .validator import SBOMSchemaValidator

def main():
    parser = argparse.ArgumentParser(
        description="Validate SBOM files (SPDX or CycloneDX) in JSON or XML format."
    )

    parser.add_argument(
        "file", type=str, help="Path to the SBOM file to validate."
    )
    parser.add_argument(
        "--format", choices=["spdx-json", "spdx-xml", "cyclonedx-json", "cyclonedx-xml"],
        required=True, help="Specify the SBOM format and encoding."
    )

    args = parser.parse_args()

    validator = SBOMSchemaValidator()

    if args.format == "spdx-json":
        result = validator.validate_spdx_json(args.file)
    elif args.format == "spdx-xml":
        result = validator.validate_spdx_xml(args.file)
    elif args.format == "cyclonedx-json":
        result = validator.validate_cyclonedx_json(args.file)
    elif args.format == "cyclonedx-xml":
        result = validator.validate_cyclonedx_xml(args.file)
    else:
        result = "Unsupported format."

    print(result)

    if result != "Valid":
        sys.exit(1)

if __name__ == "__main__":
    main()
