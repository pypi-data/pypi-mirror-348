# === File: act/actfile_parser.py ===

import configparser # Can be useful, but this implementation uses regex/manual split
import os
import re
import json
import logging
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

# Configure logger for this module
logger = logging.getLogger(__name__)

class ActfileParserError(Exception):
    """Custom exception for Actfile parsing errors."""
    pass

class ActfileParser:
    """
    Parses an Actfile (INI-like format) into a structured dictionary.
    Handles sections: [workflow], [node:*], [edges], [parameters],
                       [dependencies], [env], [settings].
    Handles comments (# or ;) and basic value types.
    """
    SUPPORTED_SECTIONS = [
        'workflow', 'parameters', 'nodes', 'edges',
        'dependencies', 'env', 'settings'
    ]

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)
        self.parsed_data: Dict[str, Any] = {
             # Initialize with default empty structures
             "parameters": {},
             "workflow": {},
             "nodes": {},
             "edges": {},
             "dependencies": {},
             "env": {},
             "settings": {}
        }
        logger.info(f"Initialized ActfileParser for path: {self.file_path}")

    def parse(self) -> Dict[str, Any]:
        """
        Parses the Actfile specified during initialization.

        Returns:
            Dict[str, Any]: A dictionary containing the parsed workflow structure.

        Raises:
            ActfileParserError: If the file is not found or parsing fails.
        """
        if not self.file_path.is_file():
            raise ActfileParserError(f"Actfile not found: {self.file_path}")

        logger.info(f"Starting parsing of Actfile: {self.file_path}")
        try:
            # Read the entire file content
            with open(self.file_path, 'r', encoding='utf-8') as file: # Specify encoding
                content = file.read()

            # Split content into logical sections based on [section_name] headers
            sections = self._split_sections(content)
            logger.debug(f"Raw sections found: {list(sections.keys())}")

            # Parse each known section type
            # Use .get(section, default_value) to handle missing sections gracefully
            self.parsed_data["parameters"] = self._parse_parameters(sections.get('parameters', ''))
            self.parsed_data["workflow"] = self._parse_key_value_section(sections.get('workflow', ''))
            self.parsed_data["nodes"] = self._parse_nodes(sections) # Nodes require special handling
            self.parsed_data["edges"] = self._parse_edges(sections.get('edges', ''))
            self.parsed_data["dependencies"] = self._parse_dependencies(sections.get('dependencies', ''))
            self.parsed_data["env"] = self._parse_env(sections.get('env', ''))
            self.parsed_data["settings"] = self._parse_key_value_section(sections.get('settings', '')) # Use generic parser

            # --- Post-Parsing Steps ---
            # Replace parameter placeholders (e.g., {{.Parameter.my_param}})
            self._replace_parameters()

            # Validate the overall structure (e.g., edges reference existing nodes)
            self._validate_parsed_data()

            logger.info("Actfile parsing completed successfully.")

        except ActfileParserError as e: # Re-raise specific parser errors
            logger.error(f"Actfile parsing failed: {e}")
            raise
        except Exception as e: # Catch other unexpected errors during parsing
            logger.error(f"Unexpected error during Actfile parsing: {e}", exc_info=True)
            # Wrap unexpected errors in the specific exception type
            raise ActfileParserError(f"Error parsing Actfile: {e}")

        return self.parsed_data

    def _split_sections(self, content: str) -> Dict[str, str]:
        """
        Splits the file content into a dictionary based on [section] headers.
        Handles comments and whitespace more carefully.
        """
        sections = {}
        current_section_name = None
        current_section_lines = []

        for line in content.splitlines():
            stripped_line = line.strip()

            # Check for section header
            match = re.match(r'^\s*\[([^\]]+)\]\s*(?:[#;].*)?$', line) # Allow comments after header
            if match:
                # If we were processing a section, save it
                if current_section_name is not None:
                    sections[current_section_name] = "\n".join(current_section_lines)

                # Start the new section
                current_section_name = match.group(1).strip()
                current_section_lines = []
                # logger.debug(f"Detected section start: [{current_section_name}]")
            elif current_section_name is not None:
                # Add line to the current section if it's not a full-line comment or empty
                if stripped_line and not stripped_line.startswith('#') and not stripped_line.startswith(';'):
                    current_section_lines.append(line) # Keep original line for parsing later

        # Save the last section
        if current_section_name is not None:
            sections[current_section_name] = "\n".join(current_section_lines)

        return sections

        # --- Inside ActfileParser class ---

    def _parse_key_value_section(self, content: str) -> Dict[str, Any]:
        """
        Parses a key=value section, handling comments, value types,
        and basic multiline JSON arrays/objects.
        """
        section_data = {}
        lines = content.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            i += 1 # Move to next line index

            # Skip empty lines and full comment lines
            if not line or line.startswith('#') or line.startswith(';'):
                continue

            if '=' in line:
                key, value_part = line.split('=', 1)
                key = key.strip()

                # Remove inline comments from the initial value part
                if '#' in value_part: value_part = value_part.split('#', 1)[0]
                if ';' in value_part: value_part = value_part.split(';', 1)[0]
                value_str = value_part.strip()

                # --- >> NEW: Check for Multiline JSON Start << ---
                is_multiline_json = False
                if (value_str.startswith('[') and not value_str.endswith(']')) or \
                   (value_str.startswith('{') and not value_str.endswith('}')):
                    # Potential start of a multiline JSON structure
                    open_bracket = value_str[0]
                    close_bracket = ']' if open_bracket == '[' else '}'
                    bracket_level = value_str.count(open_bracket) - value_str.count(close_bracket)
                    json_lines = [value_str] # Start with the first line

                    # Consume subsequent lines until brackets are balanced
                    while bracket_level > 0 and i < len(lines):
                        next_line = lines[i].strip()
                        i += 1 # Consume this line
                        # Remove comments from next line before processing
                        if '#' in next_line: next_line = next_line.split('#', 1)[0].strip()
                        if ';' in next_line: next_line = next_line.split(';', 1)[0].strip()

                        if next_line: # Ignore empty lines within JSON structure? Or handle?
                             json_lines.append(next_line)
                             bracket_level += next_line.count(open_bracket)
                             bracket_level -= next_line.count(close_bracket)

                    # Join the collected lines into a single string for parsing
                    value_str = " ".join(json_lines) # Join with space, JSON parser ignores whitespace
                    is_multiline_json = True
                    logger.debug(f"Detected multiline JSON for key '{key}': {value_str[:100]}...")
                # --- >> END Multiline Check << ---

                # Only add if the key is valid
                if key:
                     # Pass the potentially concatenated value_str to _parse_value
                     section_data[key] = self._parse_value(value_str)
                     # Log if multiline parsing failed but looked like it should work
                     if is_multiline_json and not isinstance(section_data[key], (list, dict)):
                          logger.warning(f"Parsing multiline value for key '{key}' did not result in list/dict. Check JSON syntax.")
            # else: # Handle lines without '='
            #      logger.warning(f"Line in key-value section without '=': '{line}'")

        return section_data

    # _parse_value remains mostly the same, but it now receives the full multiline string
    def _parse_value(self, value_str: str) -> Any:
        """
        Tries to interpret the value string as JSON, boolean, number, or fallback to string.
        Removes surrounding quotes from strings.
        Leaves placeholders like {{...}} and ${...} as strings for later resolution.
        """
        # Keep placeholders as strings
        if (value_str.startswith('{{') and value_str.endswith('}}')) or \
           (value_str.startswith('${') and value_str.endswith('}')):
            return value_str

        # Try parsing as JSON (object or array) - should now receive full string
        if (value_str.startswith('{') and value_str.endswith('}')) or \
           (value_str.startswith('[') and value_str.endswith(']')):
            try:
                # Attempt to parse the potentially multiline string as JSON
                parsed_json = json.loads(value_str)
                logger.debug(f"Successfully parsed value as JSON type: {type(parsed_json).__name__}")
                return parsed_json
            except json.JSONDecodeError as e:
                # Log the error if parsing fails, helps debugging Actfile syntax
                logger.warning(f"Value looked like JSON but failed to parse: {e}. Value snippet: '{value_str[:100]}...'")
                # Fall through to other checks

        # Try boolean
        if value_str.lower() == 'true': return True
        if value_str.lower() == 'false': return False

        # Try integer
        if value_str.isdigit() or (value_str.startswith('-') and value_str[1:].isdigit()):
            try: return int(value_str)
            except ValueError: pass

        # Try float
        try:
            # Python's float() is quite robust
            return float(value_str)
        except ValueError:
            pass # Not a float

        # Handle quoted strings (remove outer quotes)
        if len(value_str) >= 2:
            if value_str.startswith('"') and value_str.endswith('"'): return value_str[1:-1]
            if value_str.startswith("'") and value_str.endswith("'"): return value_str[1:-1]

        # Fallback to return the string as is
        return value_str

    def _parse_value(self, value_str: str) -> Any:
        """
        Tries to interpret the value string as JSON, boolean, number, or fallback to string.
        Removes surrounding quotes from strings.
        Leaves placeholders like {{...}} and ${...} as strings for later resolution.
        """
        # Keep placeholders as strings
        if (value_str.startswith('{{') and value_str.endswith('}}')) or \
           (value_str.startswith('${') and value_str.endswith('}')):
            return value_str

        # Try parsing as JSON (object or array)
        if (value_str.startswith('{') and value_str.endswith('}')) or \
           (value_str.startswith('[') and value_str.endswith(']')):
            try:
                return json.loads(value_str)
            except json.JSONDecodeError:
                # Not valid JSON, proceed to other types
                pass # logger.debug(f"Value '{value_str[:50]}...' looked like JSON but failed parse.")

        # Try boolean
        if value_str.lower() == 'true':
            return True
        if value_str.lower() == 'false':
            return False

        # Try integer
        if value_str.isdigit() or (value_str.startswith('-') and value_str[1:].isdigit()):
            try:
                return int(value_str)
            except ValueError: pass # Should not happen, but safety

        # Try float
        # Use a simpler check as complex float parsing can be tricky
        if '.' in value_str or 'e' in value_str.lower():
             try:
                 # Check if it only contains valid float characters (more or less)
                 if re.match(r'^-?\d+(\.\d*)?([eE][-+]?\d+)?$', value_str):
                      return float(value_str)
             except ValueError: pass

        # Handle quoted strings
        if len(value_str) >= 2 and value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]
        if len(value_str) >= 2 and value_str.startswith("'") and value_str.endswith("'"):
            return value_str[1:-1]

        # Fallback to return the string as is (stripped of outer whitespace already)
        return value_str


    def _parse_nodes(self, sections: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
        """Parses all [node:*] sections."""
        nodes = {}
        for section_name, content in sections.items():
            if section_name.startswith('node:'):
                # Extract node name carefully, handling potential spaces
                parts = section_name.split(':', 1)
                if len(parts) == 2 and parts[1].strip():
                    node_name = parts[1].strip()
                    logger.debug(f"Parsing node section: [{node_name}]")
                    # Use the generic key-value parser for the node's content
                    node_data = self._parse_key_value_section(content)
                    # Add validation specific to nodes
                    if 'type' not in node_data:
                        raise ActfileParserError(f"Node '{node_name}' must have a 'type' field defined.")
                    nodes[node_name] = node_data
                else:
                     logger.warning(f"Ignoring invalid node section header format: [{section_name}]")
        logger.info(f"Parsed {len(nodes)} node definitions.")
        return nodes

    def _parse_edges(self, content: str) -> Dict[str, List[str]]:
        """Parses the [edges] section, handling comments and multiple targets."""
        edges: Dict[str, List[str]] = {}
        for line_num, line in enumerate(content.splitlines(), 1):
            line = line.strip()
            # Skip empty lines or lines that are purely comments
            if not line or line.startswith('#') or line.startswith(';'):
                continue

            if '=' in line:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    source, targets_str = parts
                    source = source.strip()

                    # Remove potential inline comments from source
                    if '#' in source: source = source.split('#', 1)[0].strip()
                    if ';' in source: source = source.split(';', 1)[0].strip()

                    # Skip if source becomes empty after comment removal
                    if not source:
                        logger.warning(f"Skipping edge line {line_num} due to empty source after comment removal.")
                        continue

                    # Process targets: split by comma, then clean each one
                    cleaned_targets = []
                    potential_targets = targets_str.split(',')
                    for target in potential_targets:
                        target_clean = target.strip()
                        # Remove potential inline comments from target
                        if '#' in target_clean: target_clean = target_clean.split('#', 1)[0].strip()
                        if ';' in target_clean: target_clean = target_clean.split(';', 1)[0].strip()

                        # Add the cleaned target if it's not empty
                        if target_clean:
                            cleaned_targets.append(target_clean)
                        elif target.strip(): # Log if something was there before cleaning
                             logger.warning(f"Ignoring empty target part on line {line_num} after cleaning: '{target}'")


                    # Only add the edge if we have a valid source and at least one valid target
                    if source and cleaned_targets:
                        # Handle duplicate source keys: Append targets instead of overwriting
                        if source in edges:
                            edges[source].extend(cleaned_targets)
                            # Optional: remove duplicates if needed and order doesn't matter
                            # edges[source] = list(dict.fromkeys(edges[source]))
                        else:
                            edges[source] = cleaned_targets
                        logger.debug(f"Parsed edge: {source} -> {cleaned_targets}")
                    elif source and not cleaned_targets:
                         logger.warning(f"Edge definition for source '{source}' on line {line_num} resulted in no valid targets.")

                else:
                     # Should not happen if '=' is in line and split gives 2 parts
                     logger.warning(f"Skipping invalid edge line format (unexpected split result): '{line}' on line {line_num}")
            else:
                 logger.warning(f"Skipping edge line {line_num} without '=': '{line}'")

        logger.info(f"Parsed {sum(len(v) for v in edges.values())} edges from {len(edges)} source nodes.")
        return edges

    def _parse_dependencies(self, content: str) -> Dict[str, List[str]]:
        """Parses [dependencies] section: NodeTypeName = Dep1, Dep2,..."""
        dependencies = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#') or line.startswith(';'): continue
            if '=' in line:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    node_type, deps_str = parts
                    node_type = node_type.strip()
                    # Clean comments from deps_str
                    if '#' in deps_str: deps_str = deps_str.split('#', 1)[0]
                    if ';' in deps_str: deps_str = deps_str.split(';', 1)[0]

                    deps_list = [d.strip() for d in deps_str.split(',') if d.strip()]
                    if node_type and deps_list:
                        dependencies[node_type] = deps_list
        logger.debug(f"Parsed dependencies: {dependencies}")
        return dependencies

    def _parse_env(self, content: str) -> Dict[str, str]:
        """Parses [env] section, resolving ${ENV_VAR} placeholders immediately."""
        env_vars = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#') or line.startswith(';'): continue
            if '=' in line:
                key, value_part = line.split('=', 1)
                key = key.strip()
                # Clean comments from value part
                if '#' in value_part: value_part = value_part.split('#', 1)[0]
                if ';' in value_part: value_part = value_part.split(';', 1)[0]
                value = value_part.strip()

                if not key: continue

                # Resolve environment variable placeholders
                final_value = value
                if value.startswith('${') and value.endswith('}'):
                    env_var_name = value[2:-1].strip()
                    if env_var_name:
                        # Provide empty string default if env var not set
                        env_value = os.environ.get(env_var_name, None)
                        if env_value is not None:
                             final_value = env_value
                             logger.debug(f"Resolved env var '{env_var_name}' for key '{key}'")
                        else:
                             final_value = "" # Use empty string if env var doesn't exist
                             logger.warning(f"Environment variable '${{{env_var_name}}}' for key '{key}' not found, using empty string.")
                    else:
                         logger.warning(f"Empty environment variable name in placeholder: {value}")
                         final_value = "" # Treat ${} as empty

                env_vars[key] = final_value # Store the resolved value (or original if not placeholder)
        logger.debug(f"Parsed environment variables: {list(env_vars.keys())}") # Log only keys for safety
        return env_vars

    def _parse_parameters(self, content: str) -> Dict[str, Any]:
        """Parses the [parameters] section using the generic key-value parser."""
        logger.debug("Parsing [parameters] section...")
        params = self._parse_key_value_section(content)
        logger.info(f"Parsed {len(params)} parameters.")
        return params

    def _replace_parameters(self):
        """Recursively replaces {{.Parameter.key}} placeholders in parsed data."""
        if not self.parsed_data.get('parameters'):
            # logger.debug("No parameters found, skipping parameter replacement.")
            return

        logger.debug("Starting replacement of {{.Parameter.*}} placeholders...")
        params = self.parsed_data['parameters']

        def replace_recursive(item: Any) -> Any:
            if isinstance(item, str):
                # Use regex to find all parameter placeholders in the string
                param_pattern = re.compile(r'\{\{\s*\.Parameter\.([A-Za-z_][A-Za-z0-9_]*)\s*\}\}')
                new_string = item
                for match in param_pattern.finditer(item):
                    placeholder = match.group(0)
                    param_key = match.group(1)
                    if param_key in params:
                        param_value = str(params[param_key]) # Ensure value is string for replacement
                        logger.debug(f"Replacing parameter '{placeholder}' with value: '{param_value[:50]}...'")
                        new_string = new_string.replace(placeholder, param_value)
                    else:
                        logger.warning(f"Parameter placeholder '{placeholder}' references unknown parameter '{param_key}'. Leaving placeholder.")
                return new_string
            elif isinstance(item, dict):
                # Recursively process dictionary values
                return {key: replace_recursive(value) for key, value in item.items()}
            elif isinstance(item, list):
                # Recursively process list items
                return [replace_recursive(elem) for elem in item]
            else:
                # Return non-string/dict/list items as is
                return item

        # Apply replacement to the entire parsed_data structure
        # Be careful not to replace within the parameters section itself
        for section_key, section_value in self.parsed_data.items():
             if section_key != 'parameters':
                  self.parsed_data[section_key] = replace_recursive(section_value)

        logger.debug("Parameter replacement finished.")


    def _validate_parsed_data(self):
        """Performs basic validation checks on the parsed data structure."""
        logger.debug("Validating parsed Actfile data...")
        # Validate workflow section
        if 'name' not in self.parsed_data.get('workflow', {}):
            logger.warning("Workflow section missing 'name' attribute.")
        if 'start_node' not in self.parsed_data.get('workflow', {}):
             raise ActfileParserError("Workflow section must contain a 'start_node' attribute.")
        start_node = self.parsed_data['workflow']['start_node']
        if start_node not in self.parsed_data['nodes']:
             raise ActfileParserError(f"Workflow 'start_node' ('{start_node}') does not exist in [node:*] definitions.")


        # Validate edges reference existing nodes
        all_defined_nodes = set(self.parsed_data['nodes'].keys())
        edge_sources = self.parsed_data.get('edges', {})
        if not isinstance(edge_sources, dict): # Should be dict from parsing
             raise ActfileParserError(f"Internal Error: Parsed 'edges' is not a dictionary (type: {type(edge_sources)})")

        for source, targets in edge_sources.items():
            if source not in all_defined_nodes:
                # Allow start_node to be special? No, start node must be defined.
                raise ActfileParserError(f"Edge source node '{source}' is not defined in any [node:*] section.")
            if not isinstance(targets, list): # Should be list from parsing
                 raise ActfileParserError(f"Internal Error: Edge targets for '{source}' is not a list (type: {type(targets)})")
            for target in targets:
                if target not in all_defined_nodes:
                    raise ActfileParserError(f"Edge target node '{target}' (from source '{source}') is not defined in any [node:*] section.")

        # Validate dependencies (Optional: Check if dependent types actually exist?)
        # node_types = set(node.get('type', 'UNKNOWN') for node in self.parsed_data['nodes'].values())
        # for dep_node_type, required_types in self.parsed_data.get('dependencies', {}).items():
        #      # Add more checks here if needed, e.g., if required_types exist
        #      pass

        logger.debug("Parsed data validation passed.")


    # --- Public Accessor Methods ---

    def get_workflow_name(self) -> Optional[str]:
        """Returns the name defined in the [workflow] section."""
        return self.parsed_data.get('workflow', {}).get('name')

    def get_workflow_description(self) -> Optional[str]:
         """Returns the description defined in the [workflow] section."""
         return self.parsed_data.get('workflow', {}).get('description')

    def get_start_node(self) -> Optional[str]:
        """Returns the start_node defined in the [workflow] section."""
        return self.parsed_data.get('workflow', {}).get('start_node')

    def get_node_successors(self, node_name: str) -> List[str]:
        """Returns a list of target node names for a given source node name."""
        # Return a copy to prevent modification of internal data
        return list(self.parsed_data.get('edges', {}).get(node_name, []))

    def get_all_nodes(self) -> Dict[str, Dict[str, Any]]:
         """Returns the dictionary of all parsed node configurations."""
         # Return a copy? Deep copy might be safer depending on usage.
         import copy
         return copy.deepcopy(self.parsed_data.get('nodes', {}))

    def get_node_config(self, node_name: str) -> Optional[Dict[str, Any]]:
         """Returns the configuration dictionary for a specific node."""
         return self.parsed_data.get('nodes', {}).get(node_name)

    def get_env_var(self, key: str, default: Any = None) -> Any:
        """Gets a resolved environment variable defined in the [env] section."""
        return self.parsed_data.get('env', {}).get(key, default)

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Gets a setting defined in the [settings] section."""
        return self.parsed_data.get('settings', {}).get(key, default)

    def get_parameter(self, key: str, default: Any = None) -> Any:
         """Gets a parameter defined in the [parameters] section."""
         return self.parsed_data.get('parameters', {}).get(key, default)

    def to_json(self, indent: int = 2) -> str:
        """Returns the entire parsed data structure as a JSON string."""
        try:
            return json.dumps(self.parsed_data, indent=indent)
        except TypeError as e:
            logger.error(f"Could not serialize parsed data to JSON: {e}")
            # Attempt serialization with default=str as fallback
            try:
                 return json.dumps(self.parsed_data, indent=indent, default=str)
            except Exception as e_inner:
                 logger.error(f"Fallback JSON serialization also failed: {e_inner}")
                 return f'{{"error": "Failed to serialize parsed data: {e_inner}"}}'


    @staticmethod
    def find_actfile(start_dir: Union[str, Path] = None) -> Path:
        """
        Finds the Actfile (named 'Actfile' or 'actfile.ini' etc.)
        by searching up the directory tree from start_dir (or cwd).
        """
        possible_names = ["Actfile", "actfile", "actfile.ini", "Actfile.ini"] # Add other common names
        current_dir = Path(start_dir or os.getcwd()).resolve()
        logger.debug(f"Searching for Actfile starting from: {current_dir}")

        while True:
            for name in possible_names:
                 actfile_path = current_dir / name
                 if actfile_path.is_file():
                      logger.info(f"Found Actfile at: {actfile_path}")
                      return actfile_path

            # Check if we've reached the root directory
            if current_dir.parent == current_dir:
                break # Stop if we are at the filesystem root

            # Move up to the parent directory
            current_dir = current_dir.parent

        # If loop finishes without finding the file
        raise ActfileParserError(f"Actfile ({'/'.join(possible_names)}) not found in '{Path(start_dir or os.getcwd()).resolve()}' or any parent directory.")


# --- Example Usage (for standalone testing of the parser) ---
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(name)s:%(message)s')

    # Create a dummy Actfile content for testing
    dummy_content = """
# This is a comment for the whole file
[parameters]
default_level = info
user_name = "Test User"
threshold = 30.5
complex_setting = {"a": 1, "b": ["x", "y"]}

[workflow]
name = Test Workflow ; inline comment
description = A test for the parser.
# Another comment line
start_node = NodeA

[env]
API_KEY = ${MY_API_KEY_ENV_VAR} ; Using env var
STATIC_VAR = some_static_value

[node:NodeA]
type = LogMessage
message = Hello {{.Parameter.user_name}}! Starting...
level = {{.Parameter.default_level}}

[node:NodeB]
type = if
value1 = {{NodeA.result.some_output}} # Placeholder for node output
operator = ">="
value2 = {{.Parameter.threshold}}
level = debug # Extra param ignored by IfNode

[node:NodeC]
type = LogMessage
message = NodeB condition was true. API Key starts with: {{.Env.API_KEY[:5]}}...

[node:NodeD]
type = LogMessage ; comment
message = NodeB condition was false.

[edges]
# Edges section with comments and multiple targets
NodeA = NodeB ; Start the check
NodeB = NodeC # True branch comment
NodeB = NodeD, NodeE ; False branch with multiple targets (NodeE doesn't exist)
# Another comment line
NodeC = NodeF ; This source doesn't exist yet

[settings]
timeout = 60
retry_count = 3
flags = ["A", "B"]
"""
    # Create dummy env var for testing
    os.environ['MY_API_KEY_ENV_VAR'] = 'test_key_1234567890'

    dummy_path = Path("./_test_actfile_parser.ini")
    try:
        dummy_path.write_text(dummy_content, encoding='utf-8')
        print(f"\n--- Testing Parser with: {dummy_path} ---")
        parser = ActfileParser(dummy_path)
        parsed = parser.parse() # This will raise errors if validation fails
        print("\n--- Parsed Data (JSON) ---")
        print(parser.to_json())
        print("\n--- Accessor Method Examples ---")
        print(f"Workflow Name: {parser.get_workflow_name()}")
        print(f"Start Node: {parser.get_start_node()}")
        print(f"Successors of NodeA: {parser.get_node_successors('NodeA')}")
        print(f"Successors of NodeB: {parser.get_node_successors('NodeB')}") # Expect ['NodeC', 'NodeD', 'NodeE']
        print(f"NodeB Config: {parser.get_node_config('NodeB')}")
        print(f"Env API_KEY: {parser.get_env_var('API_KEY')}")
        print(f"Setting timeout: {parser.get_setting('timeout')} (type: {type(parser.get_setting('timeout'))})")
        print(f"Parameter threshold: {parser.get_parameter('threshold')} (type: {type(parser.get_parameter('threshold'))})")

    except ActfileParserError as e:
        print(f"\n--- PARSER ERROR ---")
        print(e)
        # Validation errors are expected for NodeE and NodeF in the dummy content
        if "NodeE" in str(e) or "NodeF" in str(e):
             print("(Validation Error for non-existent nodes NodeE/NodeF is expected with this test content)")
        else:
             raise # Re-raise unexpected errors
    except Exception as e:
         print(f"\n--- UNEXPECTED ERROR ---")
         print(e)
         raise
    finally:
        # Clean up the dummy file
        if dummy_path.exists():
            dummy_path.unlink()
            print(f"\nRemoved dummy file: {dummy_path}")
        del os.environ['MY_API_KEY_ENV_VAR'] # Clean up env var