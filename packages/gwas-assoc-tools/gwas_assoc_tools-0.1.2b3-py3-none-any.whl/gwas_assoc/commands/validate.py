import argparse
import contextlib
import io
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Set, Tuple

import pandas as pd
import requests
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table

from gwas_assoc.utils.console import console, print_error

# Configure logging with Rich handler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)


class SnpValidator:
    def __init__(self) -> None:
        """
        Initialize the SNP validator
        """
        self.ensembl_api_url = "https://rest.ensembl.org/variation/human/"

    def _get_study_tags(self, file_path: Path) -> Set:
        # Read study sheet to get study tags
        console.print("[info]Reading study tags...[/]")
        try:
            study_df = pd.read_excel(
                file_path, sheet_name="study", skiprows=range(1, 4)
            )

            if study_df.empty:
                print_error("Study sheet is empty or no data found.")
                return set()

            tags = set(study_df.iloc[:, 0].tolist())
            console.print(f"Found [highlight]{len(tags)}[/] study tags")
            return tags

        except Exception as e:
            print_error(f"Error reading study sheet: {str(e)}")
            return set()

    def _get_schema_version(self, file_path: Path) -> str:
        """Get the schema version from the meta sheet of the Excel file"""
        console.print("[info]Reading schema version...[/]")
        meta_df = pd.read_excel(file_path, sheet_name="meta")

        # Find the row with 'schemaVersion' in the 'Key' column
        schema_row = meta_df[meta_df["Key"] == "schemaVersion"]

        if schema_row.empty:
            print_error("schemaVersion not found in meta sheet")
            raise ValueError("schemaVersion not found")

        # Return the value from the 'Value' column
        version = str(schema_row["Value"].iloc[0])
        console.print(f"Schema version: [highlight]{version}[/]")
        return version

    def _get_associations_template_df(self, schema_version: str) -> pd.DataFrame:
        url = f"https://raw.githubusercontent.com/EBISPOT/gwas-template-services/master/schema_definitions/template_schema_v{schema_version}.xlsx"
        console.print(f"[info]Fetching schema template v{schema_version}...[/]")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses

            # Load Excel from memory
            excel_data = io.BytesIO(response.content)

            # Return dict with all sheets
            template_df = pd.read_excel(excel_data, sheet_name="association")
            console.print("[success]Successfully loaded template schema[/]")
            return template_df

        except requests.exceptions.RequestException as e:
            print_error(f"Failed to fetch schema: {str(e)}")
            raise

    def _validate_associations_against_template(
        self,
        associations_df: pd.DataFrame,
        assoc_template_df: pd.DataFrame,
    ) -> Tuple[bool, pd.DataFrame]:
        """
        Validate associations dataframe against template requirements
        """
        invalid_rows = []
        total_rows = len(associations_df)

        # Display progress without using Progress bar
        console.print(f"[info]Starting validation of {total_rows} associations...[/]")

        # Convert the template dataframe to a more usable form
        template_dict: Dict[str, Dict[str, Optional[Any]]] = {}
        for _, row in assoc_template_df.iterrows():
            header = row["HEADER"]
            if isinstance(header, str):
                template_dict[header] = {
                    "name": row["NAME"],
                    "type": row["TYPE"],
                    "pattern": (
                        row["PATTERN"] if not pd.isna(row["PATTERN"]) else None
                    ),
                    "lower": row["LOWER"] if not pd.isna(row["LOWER"]) else None,
                    "upper": row["UPPER"] if not pd.isna(row["UPPER"]) else None,
                    "mandatory_metadata": row["MANDATORY-METADATA"],
                    "size": row["SIZE"] if not pd.isna(row["SIZE"]) else None,
                }

        # Validate each row with periodic status updates
        validated_count = 0
        update_interval = max(1, total_rows // 10)  # Update about 10 times

        for _, row in associations_df.iterrows():
            validated_count += 1

            # Provide periodic updates instead of continuous progress
            if validated_count % update_interval == 0 or validated_count == total_rows:
                percent_complete = (validated_count / total_rows) * 100
                console.print(
                    f"Validated {validated_count}/{total_rows} rows "
                    f"({percent_complete:.1f}%)..."
                )

            row_valid = True
            invalid_values = {}

            for col in associations_df.columns:
                if col not in template_dict:
                    continue

                value = row[col]
                template = template_dict[col]

                # Skip validation if value is empty and not mandatory
                if pd.isna(value) and not template["mandatory_metadata"]:
                    continue

                # Validate mandatory fields
                if template["mandatory_metadata"] and pd.isna(value):
                    invalid_values[col] = "Missing mandatory value"
                    row_valid = False
                    continue

                # Type validation
                try:
                    template_pattern = str(template["pattern"])
                    if template["type"] == "number" and not pd.isna(value):
                        name = template.get("name")
                        try:
                            _ = float(str(value))
                        except Exception as e:
                            invalid_values[
                                col
                            ] = f"The value {_} for '{name}' should be float: {str(e)}"
                            row_valid = False

                        if name == "odds_ratio" and _ <= 0:
                            invalid_values[
                                col
                            ] = f"Value {_} is less than or equal to 0"
                            row_valid = False

                        # Range validation
                        if template["lower"] is not None:
                            lower_parts = str(template["lower"]).split("|")
                            if len(lower_parts) == 2:
                                # Format like "1|-5" means 10^-5 = 0.00001
                                lower_bound = float(lower_parts[0]) * (
                                    10 ** float(lower_parts[1])
                                )
                            else:
                                lower_bound = float(template["lower"])

                            if _ < lower_bound:
                                invalid_values[
                                    col
                                ] = f"Value {_} below minimum {lower_bound}"
                                row_valid = False

                        if template["upper"] is not None and _ > float(
                            template["upper"]
                        ):
                            invalid_values[
                                col
                            ] = f"Value {_} exceeds maximum {template['upper']}"
                            row_valid = False

                    # Pattern validation for strings
                    elif (
                        template["type"] == "string"
                        and template_pattern
                        and not pd.isna(value)
                    ):
                        import re

                        if template_pattern == "$p-value$":
                            with contextlib.suppress(Exception):
                                _ = float(str(value))

                            if _ <= 0:
                                invalid_values[
                                    col
                                ] = f"Value {_} is less than or equal to 0"
                                row_valid = False
                            elif _ >= 1e-05:
                                invalid_values[
                                    col
                                ] = f"Value {_} is greater than or equal to 1e-05"
                                row_valid = False

                            # Special case for p-values in scientific notation
                            pattern = r"^[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?$"
                        else:
                            pattern = template_pattern

                        if not re.match(pattern, str(value)):
                            invalid_values[
                                col
                            ] = f"Value '{value}' doesn't match pattern '{pattern}'"
                            row_valid = False

                    template_size = int(str(template["size"]))
                    # Size validation for strings
                    if (
                        template["type"] == "string"
                        and template_size != -1
                        and not pd.isna(value)
                        and len(str(value)) > template_size
                    ):
                        invalid_values[
                            col
                        ] = f"Value too long ({len(str(value))} > {template_size})"
                        row_valid = False

                except (ValueError, TypeError) as e:
                    invalid_values[col] = f"Type validation error: {str(e)}"
                    row_valid = False

            if not row_valid:
                error_row = row.copy()
                error_row["validation_errors"] = invalid_values
                invalid_rows.append(error_row)

        console.print("[success]Association validation complete[/]")

        return len(invalid_rows) == 0, (
            pd.DataFrame(invalid_rows) if invalid_rows else pd.DataFrame()
        )

    def validate_snps(self, file_path: Path) -> bool:
        """
        Validate SNPs from an Excel file

        Args:
            file_path: Path to Excel file containing SNP data

        Returns:
            bool: True if validation was successful, False otherwise
        """
        sheet_name: str = "association"
        col_study_tag = "Study tag"
        col_variant_id = "Variant ID"

        try:
            file_path_obj = Path(file_path)
            console.print(
                Panel(
                    f"Starting SNP validation for [filename]{file_path_obj.name}[/]",
                    title="GWAS SNP Validator",
                    border_style="blue",
                )
            )

            console.print("[info]Reading association data...[/]")
            header_df = pd.read_excel(
                file_path, sheet_name=sheet_name, nrows=1, header=1
            )
            column_names = header_df.columns.tolist()

            associations_df = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                skiprows=range(1, 4),
                names=column_names,
            )

            console.print(f"Loaded [highlight]{len(associations_df)}[/] associations")

            if associations_df.empty:
                msg = (
                    f"The '{sheet_name}' sheet has headers but no data rows were found."
                )
                print_error(msg)
                return False

            # Check required columns
            required_columns = [col_study_tag, col_variant_id]
            missing_columns = [
                col for col in required_columns if col not in associations_df.columns
            ]

            if missing_columns:
                for col in missing_columns:
                    print_error(f"Required column '{col}' not found in the Excel sheet")
                return False

            # Validate study tags
            study_tags: Set = self._get_study_tags(file_path)
            if not study_tags:
                print_error("No study tags loaded.")
                return False

            # Create a table for invalid study tags
            invalid_tags_found = False
            invalid_tag_table = Table(title="Invalid Study Tags")
            invalid_tag_table.add_column("Row", style="dim")
            invalid_tag_table.add_column("Study Tag", style="metric")
            invalid_tag_table.add_column("Variant ID", style="highlight")

            for idx, row in associations_df.iterrows():
                study_tag = row[col_study_tag]
                if study_tag not in study_tags:
                    invalid_tags_found = True
                    invalid_tag_table.add_row(
                        str(int(str(idx)) + 1), str(study_tag), str(row[col_variant_id])
                    )

            if invalid_tags_found:
                print_error("Invalid study tags found:")
                console.print(invalid_tag_table)
                return False

            # Fetch schema and validate against template
            try:
                schema_version: str = self._get_schema_version(file_path)
                associations_template_df = self._get_associations_template_df(
                    schema_version
                )

            except Exception as e:
                print_error(f"Cannot fetch schema template v{schema_version}: {e}")
                return False

            is_valid, error_rows = self._validate_associations_against_template(
                associations_df, associations_template_df
            )

            if not is_valid:
                error_count = len(error_rows)
                print_error(f"Found {error_count} rows with validation errors:")

                # Group errors by field for summary
                error_summary = {}
                for _, row in error_rows.iterrows():
                    errors = row["validation_errors"]
                    for column, _ in errors.items():
                        if column not in error_summary:
                            error_summary[column] = 0
                        error_summary[column] += 1

                # Create summary table
                summary_table = Table(title="")
                summary_table.add_column("Field", style="header")
                summary_table.add_column("Error Count", style="error")

                for column, count in sorted(
                    error_summary.items(), key=lambda x: x[1], reverse=True
                ):
                    summary_table.add_row(str(column), str(count))

                console.print(summary_table)

                # Display details for each error
                console.print("\n[bold]Detailed Errors:[/]")

                for idx, row in error_rows.iterrows():
                    errors = row["validation_errors"]

                    # Create a panel for each row with errors
                    study_tag = row.get("Study tag", row.get("study_tag", "Unknown"))
                    variant_id = row.get("Variant ID", row.get("variant_id", "Unknown"))

                    error_table = Table(show_header=False, box=None)
                    error_table.add_column("Field", style="header")
                    error_table.add_column("Error", style="error")

                    for column, error in errors.items():
                        error_table.add_row(str(column), error)

                    console.print(
                        Panel(
                            error_table,
                            title=f"Row {int(str(idx)) + 1}",
                            subtitle=(
                                f"Study tag: [metric]{study_tag}[/] | Variant ID: "
                                f"[highlight]{variant_id}[/]"
                            ),
                            border_style="red",
                        )
                    )

                return False

            # Create a unique key for each association
            console.print("[info]Processing associations...[/]")
            associations_df["unique_key"] = (
                associations_df[col_study_tag] + "-" + associations_df[col_variant_id]
            )

            # Remove duplicates
            before_count = len(associations_df)
            associations_df = associations_df.drop_duplicates(subset=["unique_key"])
            after_count = len(associations_df)

            if before_count > after_count:
                console.print(
                    f"Removed [highlight]{before_count - after_count}[/] "
                    f"duplicate associations"
                )

            # Extract unique SNP names
            snp_names = set(associations_df[col_variant_id].unique())
            console.print(
                f"Found [highlight]{len(snp_names)}[/] unique SNP IDs to validate"
            )

            # Success panel
            console.print(
                Panel(
                    "[success]✓ All SNPs successfully validated[/]",
                    border_style="green",
                )
            )
            return True

        except Exception as e:
            console.print_exception()
            print_error(f"SNP Validation Error: {str(e)}")
            return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate SNPs in Excel files")
    parser.add_argument("--file", "-f", help="Path to Excel file")

    args = parser.parse_args()

    validator = SnpValidator()

    if args.file:
        result = validator.validate_snps(args.file)
        if result:
            console.print("[success]✓ Validation completed successfully[/]")
        else:
            console.print("[error]✗ Validation failed[/]")
    else:
        parser.print_help()
