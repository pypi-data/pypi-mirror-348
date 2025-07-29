import base64
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from agents import Agent, Runner, function_tool
from agents.mcp.server import MCPServer
from mcp import ClientSession
from satif_core import AsyncCodeBuilder, CodeBuilder, SDIFDatabase
from satif_sdk.comparators import get_comparator
from satif_sdk.representers import get_representer
from satif_sdk.transformers import CodeTransformer

# Global variables for transformation
INPUT_SDIF_PATH: Optional[Path] = None
OUTPUT_TARGET_FILES: Optional[Dict[Union[str, Path], str]] = None
SCHEMA_ONLY: Optional[bool] = None


def _format_comparison_output(
    comparison_result: Dict[str, Any],
    schema_only_mode: Optional[bool],
    source_file_display_name: str,
    target_file_display_name: str,
) -> str:
    """
    Formats the comparison result string, with special handling for schema_only mode
    where files are equivalent due to being empty.
    """
    base_message_prefix = f"Comparison for {source_file_display_name} [SOURCE] with {target_file_display_name} [TARGET]:"

    if schema_only_mode is True and comparison_result.get("are_equivalent") is True:
        details = comparison_result.get("details", {})
        row_comparison = details.get("row_comparison", {})

        row_count1 = row_comparison.get("row_count1")
        row_count2 = row_comparison.get("row_count2")

        if (
            isinstance(row_count1, (int, float))
            and row_count1 == 0
            and isinstance(row_count2, (int, float))
            and row_count2 == 0
        ):
            return f"{base_message_prefix} Files have the same headers but are both empty (no data rows). This should not happen. Please verify the instructions and try again."

    # Default formatting if the special condition isn't met
    return f"{base_message_prefix} {comparison_result}"


@function_tool
async def execute_transformation(code: str) -> str:
    """Executes the transformation code on the input and returns the
    comparison difference between the transformed output and the target output example.

    Args:
        code: The code to execute on the input.
    """
    if INPUT_SDIF_PATH is None or OUTPUT_TARGET_FILES is None:
        return "Error: Transformation context not initialized"

    code_transformer = CodeTransformer(function=code)
    generated_output_path = code_transformer.export(INPUT_SDIF_PATH)

    comparisons = []
    comparator_kwargs = {}
    if SCHEMA_ONLY:
        comparator_kwargs["check_structure_only"] = True

    if os.path.isdir(generated_output_path):
        # If it's a directory, compare each file with its corresponding target
        generated_files = os.listdir(generated_output_path)

        for (
            output_base_file,
            output_target_file_name,
        ) in OUTPUT_TARGET_FILES.items():
            if output_target_file_name in generated_files:
                generated_file_path = os.path.join(
                    generated_output_path, output_target_file_name
                )
                comparator = get_comparator(output_target_file_name.split(".")[-1])
                comparison = comparator.compare(
                    generated_file_path, output_base_file, **comparator_kwargs
                )
                formatted_message = _format_comparison_output(
                    comparison,
                    SCHEMA_ONLY,
                    generated_file_path,
                    output_target_file_name,
                )
                comparisons.append(formatted_message)
            else:
                comparisons.append(
                    f"Error: {output_target_file_name} not found in the generated output"
                )
    else:
        # If it's a single file, ensure there's only one target and compare
        if len(OUTPUT_TARGET_FILES) == 1:
            output_file = list(OUTPUT_TARGET_FILES.keys())[0]
            output_target_file_name = list(OUTPUT_TARGET_FILES.values())[0]
            comparator = get_comparator(output_file.split(".")[-1])
            comparison = comparator.compare(
                generated_output_path, output_file, **comparator_kwargs
            )
            formatted_message = _format_comparison_output(
                comparison,
                SCHEMA_ONLY,
                str(generated_output_path),
                output_target_file_name,
            )
            comparisons.append(formatted_message)
        else:
            comparisons.append(
                "Error: Single output file generated but multiple target files expected"
            )

    return "\n".join(comparisons)


class TransformationCodeBuilder(CodeBuilder):
    def __init__(self, output_example: Path | List[Path] | Dict[str, Path]):
        self.output_example = output_example

    def build(
        self,
        sdif: Path | SDIFDatabase,
        instructions: Optional[str] = None,
    ) -> str:
        pass


class TransformationAsyncCodeBuilder(AsyncCodeBuilder):
    """This class is used to build a transformation code that will be used to transform a SDIF database into a set of files following the format of the given output files."""

    def __init__(
        self,
        mcp_server: MCPServer,
        mcp_session: ClientSession,
        llm_model: str = "o4-mini",
    ):
        self.mcp_server = mcp_server
        self.mcp_session = mcp_session
        self.llm_model = llm_model

    async def build(
        self,
        sdif: Path,  # This will now be relative to project root (MCP server CWD)
        output_target_files: Dict[Union[str, Path], str] | List[Path],
        output_sdif: Optional[Path] = None,  # This will now be relative or None
        instructions: str = "",
        schema_only: bool = False,
        representer_options_for_build: Optional[Dict[str, Any]] = None,
    ) -> str:
        global INPUT_SDIF_PATH, OUTPUT_TARGET_FILES, SCHEMA_ONLY
        # INPUT_SDIF_PATH is used by execute_transformation tool, needs to be accessible from where that tool runs.
        # If execute_transformation runs in the same process as the builder, absolute path is fine.
        # If it were a separate context, this might need adjustment.
        # For now, assume execute_transformation can access absolute paths if needed for its *input SDIF*.
        # However, the sdif for MCP URIs must be relative.
        INPUT_SDIF_PATH = Path(sdif).resolve()
        SCHEMA_ONLY = schema_only
        # Paths for MCP URIs are now expected to be relative to MCP server CWD (project root)
        # So, use them directly as strings.
        input_sdif_mcp_uri_path = base64.b64encode(str(sdif).encode()).decode()
        output_sdif_mcp_uri_path = (
            base64.b64encode(str(output_sdif).encode()).decode()
            if output_sdif
            else None
        )

        input_schema = await self.mcp_session.read_resource(
            f"schema://{input_sdif_mcp_uri_path}"
        )
        input_sample = await self.mcp_session.read_resource(
            f"sample://{input_sdif_mcp_uri_path}"
        )

        output_schema_text = "N/A"
        output_sample_text = "N/A"
        if output_sdif_mcp_uri_path:
            try:
                output_schema_content = await self.mcp_session.read_resource(
                    f"schema://{output_sdif_mcp_uri_path}"
                )
                if output_schema_content.contents:
                    output_schema_text = output_schema_content.contents[0].text
            except Exception as e:
                print(
                    f"Warning: Could not read schema for output_sdif {output_sdif_mcp_uri_path}: {e}"
                )

            try:
                output_sample_content = await self.mcp_session.read_resource(
                    f"sample://{output_sdif_mcp_uri_path}"
                )
                if output_sample_content.contents:
                    output_sample_text = output_sample_content.contents[0].text
            except Exception as e:
                print(
                    f"Warning: Could not read sample for output_sdif {output_sdif_mcp_uri_path}: {e}"
                )

        # OUTPUT_TARGET_FILES keys are absolute paths to original example files for local reading by representers/comparators.
        # Values are agent-facing filenames.
        if isinstance(output_target_files, list):
            OUTPUT_TARGET_FILES = {
                file_path.resolve(): file_path.name for file_path in output_target_files
            }
        elif isinstance(output_target_files, dict):
            temp_map = {}
            for k, v in output_target_files.items():
                if isinstance(k, Path):
                    temp_map[k.resolve()] = v
                else:
                    temp_map[k] = v
            OUTPUT_TARGET_FILES = temp_map
        else:
            OUTPUT_TARGET_FILES = {}

        output_representation = defaultdict(dict)
        if OUTPUT_TARGET_FILES:
            for file_key_abs_path in list(OUTPUT_TARGET_FILES.keys()):
                agent_facing_name = OUTPUT_TARGET_FILES[file_key_abs_path]
                print(f"Representing {agent_facing_name} from {file_key_abs_path}")
                try:
                    # Representer uses the absolute path (file_key_abs_path) to read the example file.
                    representer = get_representer(file_key_abs_path)
                    representation, used_params = representer.represent(
                        file_key_abs_path, **(representer_options_for_build or {})
                    )
                    output_representation[agent_facing_name] = {
                        "representation": representation,
                        "used_params": used_params,
                    }
                except Exception as e:
                    print(
                        f"Warning: Could not get representation for {agent_facing_name} (path {file_key_abs_path}): {e}"
                    )
                    output_representation[agent_facing_name] = (
                        f"Error representing file: {e}"
                    )

        prompt = await self.mcp_session.get_prompt(
            "create_transformation",
            arguments={
                "input_file": Path(
                    input_sdif_mcp_uri_path
                ).name,  # Display name for prompt (from relative path)
                "input_schema": input_schema.contents[0].text
                if input_schema.contents
                else "Error reading input schema",
                "input_sample": input_sample.contents[0].text
                if input_sample.contents
                else "Error reading input sample",
                "output_files": str(list(OUTPUT_TARGET_FILES.values())),
                "output_schema": output_schema_text,
                "output_sample": output_sample_text
                if not SCHEMA_ONLY
                else "Sample not available. File is empty (no data).",
                "output_representation": str(output_representation),
                "instructions": instructions
                or "No instructions provided. Use the output example.",
            },
        )
        agent = Agent(
            name="Transformation Builder",
            mcp_servers=[self.mcp_server],
            tools=[execute_transformation],
            model=self.llm_model,
        )
        result = await Runner.run(agent, prompt.messages[0].content.text)
        transformation_code = self.parse_code(result.final_output)
        return transformation_code

    def parse_code(self, code) -> str:
        match = re.search(r"```(?:python)?(.*?)```", code, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            # Handle case where no code block is found
            return code.strip()
