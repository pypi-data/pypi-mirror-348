# === File: act/execution_manager.py ===

import importlib
import traceback
import logging
import json
from typing import Callable, Dict, Any, List, Optional, Type, Tuple, Union, Set
import asyncio
from datetime import datetime, timedelta
import re
import os
from pathlib import Path
import inspect
import sys
import copy

# Third-party libraries
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("Warning: colorama not found. Colors will not be used in output.")
    class DummyStyle:
        def __getattr__(self, name): return ""
    Fore = DummyStyle()
    Style = DummyStyle()

try:
    from tabulate import tabulate
except ImportError:
    print("Warning: tabulate not found. Status tables will be basic.")
    def tabulate(table_data, headers, tablefmt, maxcolwidths=None): # Added maxcolwidths stub
        if not table_data: return "No data to display."
        widths = [len(h) for h in headers]
        for row in table_data:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))
        # Basic maxcolwidths handling if needed (simple truncation)
        if maxcolwidths:
            for i, w in enumerate(maxcolwidths):
                if w is not None and widths[i] > w:
                    widths[i] = w

        sep = "+".join("-" * (w + 2) for w in widths)
        header_line = "|" + "|".join(f" {h:<{widths[i]}} " for i, h in enumerate(headers)) + "|"

        def format_cell(cell, width):
             s_cell = str(cell)
             if maxcolwidths and maxcolwidths[i] is not None and len(s_cell) > width:
                  return f" {s_cell[:width-3]}... "
             return f" {s_cell:<{width}} "

        data_lines = [
            "|" + "|".join(format_cell(cell, widths[i]) for i, cell in enumerate(row)) + "|"
            for row in table_data
        ]
        return "\n".join([sep, header_line, sep] + data_lines + [sep])

# --- Custom Exception Definitions ---
class NodeExecutionError(Exception):
    """Custom exception for errors during node execution."""
    pass

class NodeValidationError(Exception):
    """Custom exception for errors during node validation or parameter issues."""
    pass

class PlaceholderResolutionError(Exception):
    """Custom exception for errors during placeholder resolution."""
    pass

# Relative imports (assuming package structure)
try:
    from .actfile_parser import ActfileParser, ActfileParserError
    from .nodes.base_node import BaseNode
except ImportError as e:
    print(f"Warning: Relative import failed ({e}). Attempting direct imports or using placeholders.")
    class ActfileParserError(Exception): pass
    class ActfileParser:
        def __init__(self, path): self.path = path; logger.warning("Using dummy ActfileParser.")
        def parse(self): logger.warning("Using dummy ActfileParser.parse()"); return {'workflow': {'start_node': None, 'name': 'DummyFlow'}, 'nodes': {}, 'edges': {}}
        def get_start_node(self): return None
        def get_node_successors(self, node_name): return []
        def get_workflow_name(self): return "DummyFlow"
    class BaseNode:
        node_type: Optional[str] = None # Add placeholder for node_type hint
        def set_execution_manager(self, manager): pass
        def set_sandbox_timeout(self, timeout): pass
        async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]: return {"status": "success", "result": {}}

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s [%(levelname)s] - %(message)s')
logger = logging.getLogger(__name__)

# --- ExecutionManager Class ---

class ExecutionManager:
    """
    Manages the loading, resolution, and execution of workflows defined in Actfiles.
    Handles node discovery, advanced placeholder resolution (cache, debug, fallback,
    circular refs), and sequential/conditional execution based on defined edges.
    """
    def __init__(self,
                 actfile_path: Union[str, Path] = 'Actfile',
                 sandbox_timeout: int = 600,
                 resolution_debug_mode: bool = False,
                 fail_on_unresolved: bool = False):
        """
        Initializes the ExecutionManager.

        Args:
            actfile_path: Path to the Actfile definition.
            sandbox_timeout: Maximum execution time for the workflow in seconds (0 for no timeout).
            resolution_debug_mode: Enable detailed logging for placeholder resolution.
            fail_on_unresolved: If True, raise an error if any placeholder fails to resolve during execution preparation.
        """
        logger.info(f"Initializing ExecutionManager with Actfile: {actfile_path}")
        self.actfile_path = Path(actfile_path)
        self.sandbox_timeout = sandbox_timeout
        self.resolution_debug_mode = resolution_debug_mode
        self.fail_on_unresolved = fail_on_unresolved
        if self.resolution_debug_mode:
            logger.setLevel(logging.DEBUG)
            logger.debug("Placeholder resolution debug mode enabled.")

        self.node_results: Dict[str, Any] = {}
        self.sandbox_start_time: Optional[datetime] = None
        self.node_loading_status: Dict[str, Dict[str, str]] = {}

        # Track node execution status
        self.node_execution_status: Dict[str, Dict[str, Any]] = {}
        self.current_execution_id: Optional[str] = None
        self.status_callbacks: List[Callable] = []

        # Store initial workflow input data
        self.initial_input_data: Dict[str, Any] = {}

        # Store parsed workflow data and the parser instance
        self.workflow_data: Dict[str, Any] = {}
        self.actfile_parser: Optional[ActfileParser] = None
        self.node_executors: Dict[str, Any] = {}

        # Placeholder Resolution Cache & Tracking
        self.resolution_cache: Dict[str, Any] = {} # Stores {{placeholder}} -> resolved_value
        self.resolved_values_by_key: Dict[str, Any] = {} # Stores `key` -> value (from set nodes, etc.)

        # Load workflow data and node executors during initialization
        try:
            self.load_workflow()
        except (FileNotFoundError, ActfileParserError) as e:
            logger.error(f"Failed to initialize ExecutionManager: {e}")
            raise

    # --- Status Reporting ---

    def register_status_callback(self, callback: Callable):
        """Registers a callback function to receive status updates during execution."""
        if callable(callback):
            self.status_callbacks.append(callback)
            logger.debug(f"Registered status callback: {getattr(callback, '__name__', 'anonymous')}")
        else:
            logger.warning("Attempted to register a non-callable status callback.")

    def update_node_status(self, node_name: str, status: str, message: str = ""):
        """Updates the status of a node and notifies all registered callbacks."""
        timestamp = datetime.now().isoformat()
        status_entry = {
            "status": status,
            "message": message,
            "timestamp": timestamp
        }
        self.node_execution_status[node_name] = status_entry
        # Use DEBUG level for frequent updates, INFO for final/major statuses
        log_level = logging.DEBUG if status in ["running", "pending"] else logging.INFO
        logger.log(log_level, f"Node '{node_name}' Status -> {status.upper()}: {message[:100] + ('...' if len(message)>100 else '')}")

        # Notify all registered callbacks
        for callback in self.status_callbacks:
            try:
                callback(node_name, status, message, self.node_execution_status)
            except Exception as e:
                logger.error(f"Error in status callback '{getattr(callback, '__name__', 'anonymous')}': {e}", exc_info=True)

    def get_execution_status(self) -> Dict[str, Any]:
        """Returns the current execution status including results and configuration."""
        wf_name = "N/A"
        if self.actfile_parser and hasattr(self.actfile_parser, 'get_workflow_name'):
             wf_name = self.actfile_parser.get_workflow_name() or "N/A"

        return {
            "execution_id": self.current_execution_id,
            "node_status": self.node_execution_status,
            "results": self.node_results, # Note: results might contain unresolved placeholders until end
            "initial_input": self.initial_input_data,
            "workflow_name": wf_name
        }

    # --- Workflow Loading and Node Discovery ---

    def load_workflow(self):
        """Loads the workflow data using ActfileParser and loads node executors."""
        logger.info(f"Loading workflow data from: {self.actfile_path}")
        if not self.actfile_path.is_file():
             error_msg = f"Actfile not found at path: {self.actfile_path}"
             logger.error(error_msg)
             raise FileNotFoundError(error_msg)

        try:
            self.actfile_parser = ActfileParser(self.actfile_path)
            self.workflow_data = self.actfile_parser.parse()
            logger.info("Actfile parsed successfully.")
            if not self.workflow_data.get('nodes'):
                 logger.warning("Actfile parsed but contains no 'nodes' section.")

        except ActfileParserError as e:
            logger.error(f"Error parsing Actfile: {e}")
            self.workflow_data = {}
            self.actfile_parser = None
            raise
        except Exception as e:
            logger.error(f"Unexpected error during Actfile parsing: {e}", exc_info=True)
            self.workflow_data = {}
            self.actfile_parser = None
            raise ActfileParserError(f"Unexpected error during parsing: {e}")

        # Load executors only after successful parsing
        if self.workflow_data:
            self.load_node_executors()
        else:
            logger.warning("Skipping node executor loading due to parsing failure.")

    def discover_node_classes(self) -> Dict[str, Type[BaseNode]]:
        """
        Discovers available BaseNode subclasses from the 'act.nodes' package.

        Returns:
            A dictionary mapping discovered node type strings to their class objects.
        """
        node_classes: Dict[str, Type[BaseNode]] = {}
        nodes_package_name = "act.nodes"

        try:
            nodes_module = importlib.import_module(nodes_package_name)
            package_path = getattr(nodes_module, '__path__', None)
            if not package_path:
                 package_file = inspect.getfile(nodes_module)
                 nodes_dir = Path(package_file).parent
            else:
                 nodes_dir = Path(package_path[0])

            logger.info(f"Scanning nodes directory: {nodes_dir}")
        except (ImportError, TypeError, AttributeError, FileNotFoundError) as e:
            logger.error(f"Could not import or find nodes package '{nodes_package_name}' at expected location: {e}", exc_info=False)
            logger.info("Attempting fallback nodes directory lookup...")
            try:
                # Fallback: Assume nodes directory is sibling to act directory
                nodes_dir = Path(__file__).parent.parent / "nodes" # Adjust if needed
                if not nodes_dir.is_dir():
                    # Fallback 2: Assume nodes directory is sibling to this file's dir
                    nodes_dir = Path(__file__).parent / "nodes"
                    if not nodes_dir.is_dir():
                         raise FileNotFoundError("Fallback directories also not found.")
                logger.info(f"Falling back to scanning nodes directory: {nodes_dir}")
            except Exception as fallback_e:
                logger.error(f"Nodes directory could not be located via standard import or fallbacks: {fallback_e}. Node discovery aborted.")
                return {}

        # --- Node Registry (Optional) ---
        registry_module_name = f"{nodes_package_name}.node_registry"
        try:
            registry_module = importlib.import_module(registry_module_name)
            # Look for common registry variable names
            registry = getattr(registry_module, 'NODES', None) or \
                       getattr(registry_module, 'NODE_REGISTRY', None) or \
                       getattr(registry_module, 'node_registry', None)
            if isinstance(registry, dict):
                logger.info(f"Found node registry '{registry_module_name}' with {len(registry)} nodes")
                # Ensure values are valid BaseNode subclasses
                for node_type, node_class in registry.items():
                     if inspect.isclass(node_class) and issubclass(node_class, BaseNode):
                         if node_type not in node_classes:
                             node_classes[node_type] = node_class
                         else:
                             logger.warning(f"Node type '{node_type}' from registry conflicts with previous definition. Keeping first found.")
                     else:
                         logger.warning(f"Invalid entry in registry for '{node_type}': {node_class}. Skipping.")
            else: logger.debug(f"No NODES/NODE_REGISTRY dict found in {registry_module_name}")
        except (ImportError, AttributeError) as e:
            logger.debug(f"Node registry {registry_module_name} not found or error loading: {e}")
        except Exception as e:
             logger.error(f"Unexpected error loading node registry {registry_module_name}: {e}", exc_info=True)

        # --- Dynamic Discovery from Files ---
        node_files: Dict[str, Path] = {}
        logger.debug(f"Globbing for Python files in {nodes_dir}")
        for file_path in nodes_dir.glob('*.py'):
            module_name = file_path.stem
            if file_path.name.startswith('__') or module_name.lower() in ('base_node', 'node_registry'):
                logger.debug(f"Skipping file: {file_path.name}")
                continue
            logger.debug(f"Found potential node file: {module_name}")
            node_files[module_name] = file_path

        if node_files: logger.info(f"Found {len(node_files)} potential node files for dynamic loading.")
        else: logger.info("No additional node files found for dynamic loading.")

        for module_name, file_path in node_files.items():
            try:
                # Determine the full module path for importlib
                # This logic assumes 'act.nodes' is the correct base, might need adjustment
                # depending on how the package is installed/structured.
                # We'll try relative to the discovered nodes_dir first if possible.
                full_module_name = None
                try:
                    # Find the 'act' root relative to the nodes_dir
                    current = nodes_dir.parent
                    package_parts = [nodes_dir.name, module_name]
                    while current.name != 'act' and current != current.parent:
                         package_parts.insert(0, current.name)
                         current = current.parent
                    if current.name == 'act':
                        package_parts.insert(0, 'act')
                        full_module_name = ".".join(package_parts)
                        logger.debug(f"Trying module import path: {full_module_name}")
                    else: # Fallback if 'act' root wasn't found that way
                         logger.debug(f"Could not determine package root. Falling back to default guess: {nodes_package_name}.{module_name}")
                         full_module_name = f"{nodes_package_name}.{module_name}"

                except Exception: # Broad exception during path calculation
                     logger.warning(f"Error calculating full module name for {module_name}. Using fallback.")
                     full_module_name = f"{nodes_package_name}.{module_name}"

                logger.debug(f"Attempting to import module: {full_module_name}")
                module = importlib.import_module(full_module_name)

                for attr_name, attr_value in inspect.getmembers(module, inspect.isclass):
                    if issubclass(attr_value, BaseNode) and attr_value is not BaseNode and not inspect.isabstract(attr_value):
                        node_class = attr_value
                        node_type = self._determine_node_type(node_class, attr_name, module_name)

                        if node_type and node_type not in node_classes:
                             logger.info(f"Discovered node class {attr_name} (from {module_name}) -> type '{node_type}'")
                             node_classes[node_type] = node_class
                        elif node_type and node_type in node_classes:
                             logger.debug(f"Node type '{node_type}' from {attr_name} (in {module_name}) already registered. Skipping dynamic load for this class.")
                        elif not node_type:
                             logger.warning(f"Could not determine node type for class {attr_name} in {module_name}.")
            except ImportError:
                logger.error(f"ImportError processing node file {module_name} using path '{full_module_name}'. Check PYTHONPATH or package structure.", exc_info=False)
            except Exception as e:
                logger.error(f"Error processing node file {module_name} ({file_path}): {e}", exc_info=True)

        logger.info(f"Node discovery finished. Total distinct node types found: {len(node_classes)}")
        return node_classes

    def _determine_node_type(self, node_class: Type[BaseNode], class_name: str, module_name: str) -> Optional[str]:
        """Helper to determine the node type string from class.node_type or class name."""
        node_type = None
        try:
            # Prefer explicit node_type defined on the class
            schema_node_type = getattr(node_class, 'node_type', None)
            if schema_node_type and isinstance(schema_node_type, str):
                node_type = schema_node_type
                logger.debug(f"Using node_type '{node_type}' from class variable for class {class_name}")
                return node_type

            # Note: 'get_schema' is generally for parameters, not the node type itself.
            # if hasattr(node_class, 'get_schema'):
            #      logger.debug(f"Class {class_name} has get_schema method.")
            #      pass

        except Exception as e: logger.warning(f"Error checking node_type for {class_name}: {e}")

        # Fallback to class name conversion
        if class_name.endswith('Node'): node_type = self._snake_case(class_name[:-4])
        else: node_type = self._snake_case(class_name)
        logger.debug(f"Using derived node_type '{node_type}' from class name {class_name}")
        return node_type

    def load_node_executors(self):
        """Instantiates node executor classes required by the current workflow."""
        logger.info("Loading node executors for the current workflow...")
        if not self.workflow_data or 'nodes' not in self.workflow_data:
             logger.error("Cannot load node executors: Workflow data is not loaded or empty.")
             return

        node_types_in_workflow = set()
        for node_name, node_config in self.workflow_data['nodes'].items():
            if isinstance(node_config, dict) and node_config.get('type'):
                 node_types_in_workflow.add(node_config['type'])
            else:
                 logger.warning(f"Node '{node_name}' configuration is invalid or missing 'type'. Skipping.")

        if not node_types_in_workflow: logger.warning("No valid node types found in the current workflow definition."); return

        logger.info(f"Workflow requires node types: {', '.join(sorted(list(node_types_in_workflow)))}")
        self.node_executors = {}
        self.node_loading_status = {node_type: {'status': 'pending', 'message': ''} for node_type in node_types_in_workflow}
        all_available_node_classes = self.discover_node_classes()
        logger.info(f"Discovered {len(all_available_node_classes)} potentially available node types.")

        for node_type in node_types_in_workflow:
            node_class = None; load_message = ""; status = "error"
            node_class = all_available_node_classes.get(node_type)
            if node_class: load_message = f"Found exact match: class {node_class.__name__}"; logger.debug(f"Found exact match for '{node_type}': {node_class.__name__}")
            else:
                # Case-insensitive fallback search
                logger.debug(f"No exact match for '{node_type}', checking case-insensitive...")
                found_case_insensitive = False
                for available_type, klass in all_available_node_classes.items():
                    if available_type.lower() == node_type.lower():
                        node_class = klass
                        load_message = f"Found case-insensitive match: type '{available_type}' (class {node_class.__name__})"
                        logger.debug(f"Found case-insensitive match for '{node_type}': Using type '{available_type}' ({node_class.__name__})")
                        found_case_insensitive = True
                        break
                if not found_case_insensitive:
                    load_message = "No suitable node class found (checked exact and case-insensitive)."
                    logger.warning(f"Could not find class for node type: '{node_type}'.")

            if node_class:
                try:
                    node_instance = self._instantiate_node(node_class)
                    if node_instance:
                        self.node_executors[node_type] = node_instance
                        status = 'success'
                        load_message += " -> Instantiated successfully."
                        logger.info(f"Successfully loaded executor for '{node_type}'.")
                    else:
                        status = 'error'
                        load_message += " -> Instantiation failed (returned None)."
                        logger.error(f"Instantiation of {node_class.__name__} for '{node_type}' returned None.")
                except Exception as e:
                    status = 'error'
                    load_message += f" -> Instantiation error: {e}"
                    logger.error(f"Error instantiating {node_class.__name__} for '{node_type}': {e}", exc_info=True)

            self.node_loading_status[node_type]['status'] = status
            self.node_loading_status[node_type]['message'] = load_message

        self._print_node_loading_status()

    def _print_node_loading_status(self):
        """Prints a formatted table showing the loading status of required nodes."""
        if not self.node_loading_status: print("\nNo nodes required by workflow or loading not performed.\n"); return
        headers = ["Required Node Type", "Loading Status", "Details"]; table_data = []
        for node_type, status_info in sorted(self.node_loading_status.items()):
            status = status_info['status']; message = status_info['message']
            if status == 'success': status_symbol, color = "🟢", Fore.GREEN
            elif status == 'fallback': status_symbol, color = "🟡", Fore.YELLOW # Note: Fallback status not currently set, but kept for potential future use
            elif status == 'error': status_symbol, color = "🔴", Fore.RED
            else: status_symbol, color = "⚪", Fore.WHITE # Pending
            table_data.append([node_type, f"{color}{status_symbol} {status.upper()}{Style.RESET_ALL}", message])
        try:
            table = tabulate(table_data, headers=headers, tablefmt="grid", maxcolwidths=[None, 15, 80])
        except NameError:
             table = self._basic_table(table_data, headers)
        print("\n--- Node Executor Loading Status ---\n" + table + "\n------------------------------------\n")

    def _basic_table(self, data, headers):
         """Minimal text table formatting if tabulate is unavailable."""
         # (Implementation copied from the original prompt)
         if not data: return "No data."
         widths = [len(h) for h in headers]
         for row in data:
             for i, cell in enumerate(row): widths[i] = max(widths[i], len(str(cell)))
         sep = "+".join("-" * (w + 2) for w in widths)
         header_line = "|" + "|".join(f" {h:<{widths[i]}} " for i, h in enumerate(headers)) + "|"
         data_lines = [ "|" + "|".join(f" {str(cell):<{widths[i]}} " for i, cell in enumerate(row)) + "|" for row in data ]
         return "\n".join([sep, header_line, sep] + data_lines + [sep])

    def _instantiate_node(self, node_class: Type[BaseNode]) -> Optional[BaseNode]:
        """Instantiates a node class, handles sandbox_timeout, sets execution_manager."""
        logger.debug(f"Instantiating node class: {node_class.__name__}")
        try:
            # Check constructor signature (optional, for advanced DI if needed later)
            # sig = inspect.signature(node_class.__init__)
            # if len(sig.parameters) > 1: # More than self
            #     logger.warning(f"Node class {node_class.__name__} has constructor parameters. Ensure defaults or DI are handled if needed.")

            node_instance = node_class()

            # Dependency Injection: Provide ExecutionManager and settings
            set_manager_method = getattr(node_instance, 'set_execution_manager', None)
            if callable(set_manager_method):
                logger.debug(f"Setting execution manager for instance of {node_class.__name__}")
                set_manager_method(self)
            else:
                 logger.debug(f"Node class {node_class.__name__} does not have 'set_execution_manager' method.")


            set_timeout_method = getattr(node_instance, 'set_sandbox_timeout', None)
            if callable(set_timeout_method):
                logger.debug(f"Setting sandbox timeout ({self.sandbox_timeout}s) for instance of {node_class.__name__}")
                set_timeout_method(self.sandbox_timeout)
            else:
                logger.debug(f"Node class {node_class.__name__} does not have 'set_sandbox_timeout' method.")


            return node_instance
        except Exception as e:
            logger.error(f"Failed to instantiate {node_class.__name__}: {e}", exc_info=True)
            return None # Return None on failure to indicate issue

    # --- Workflow Execution ---

    def execute_workflow(self,
                         execution_id: Optional[str] = None,
                         initial_input: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes the loaded workflow synchronously. Accepts initial input data.
        Manages the async execution loop internally using asyncio.run().
        """
        self.current_execution_id = execution_id or f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        logger.info(f"Starting synchronous execution wrapper for workflow ID: {self.current_execution_id}")

        # Reset state for this execution run
        self.node_results = {}
        self.node_execution_status = {}
        self.resolution_cache = {} # Clear resolution cache for new run
        self.resolved_values_by_key = {} # Clear key-specific value cache
        self.initial_input_data = dict(initial_input) if initial_input else {}
        logger.debug(f"Stored initial input data for run {self.current_execution_id}: {self.log_safe_node_data(self.initial_input_data)}")

        if self.workflow_data and 'nodes' in self.workflow_data:
             # Initialize status for all defined nodes
             for node_name in self.workflow_data['nodes'].keys():
                 self.update_node_status(node_name, "pending", "Waiting for execution")
        else:
             logger.error("Cannot execute workflow: Workflow data not loaded or missing nodes.")
             return {"status": "error", "message": "Workflow data not loaded/invalid.", "results": {}, "node_status": self.node_execution_status, "execution_id": self.current_execution_id}

        try:
             # Run the async execution logic within a synchronous context
             result = asyncio.run(self.execute_workflow_async())
             logger.info(f"Workflow {self.current_execution_id} execution finished.")
             self._print_node_execution_results() # Print summary table
             return result
        except Exception as e:
             logger.error(f"Critical error during workflow execution run: {e}", exc_info=True)
             # Ensure results table is printed even on critical failure
             self._print_node_execution_results()
             # Find the last running/pending node if possible
             last_node = "N/A"
             for name, status in self.node_execution_status.items():
                  if status["status"] in ("running", "pending"):
                       last_node = name
                       self.update_node_status(last_node, "error", f"Workflow crashed: {e}")
                       break
             return {"status": "error", "message": f"Workflow execution failed with unexpected error: {e}", "results": self.node_results, "node_status": self.node_execution_status, "execution_id": self.current_execution_id}

    async def execute_workflow_async(self) -> Dict[str, Any]:
        """
        Asynchronously executes the workflow step-by-step based on Actfile edges.
        Handles node execution, result storage, status updates, and timeout checks.
        Uses the stored `self.initial_input_data` for placeholder resolution context.
        Includes conditional logic based on If/Switch nodes.
        """
        exec_id = self.current_execution_id
        logger.info(f"Starting ASYNC execution of workflow ID: {exec_id}")
        if self.resolution_debug_mode: logger.debug(f"Initial input data for this run: {self.log_safe_node_data(self.initial_input_data)}")

        if not self.actfile_parser:
            logger.error("Cannot execute async workflow: Actfile parser not available.")
            return {"status": "error", "message": "Actfile parser not initialized.", "results": {}, "node_status": self.node_execution_status, "execution_id": exec_id}

        self.sandbox_start_time = datetime.now()
        execution_queue: List[Tuple[str, Optional[Dict[str, Any]]]] = [] # Stores (node_name, previous_node_result_context)
        executed_nodes = set() # Prevents re-execution in simple loops/merges

        try:
            start_node_name = self.actfile_parser.get_start_node()
            if not start_node_name:
                logger.error("No start node specified in Actfile.")
                return {"status": "error", "message": "No start node specified.", "results": {}, "node_status": self.node_execution_status, "execution_id": exec_id}
            if start_node_name not in self.workflow_data.get('nodes', {}):
                error_msg = f"Start node '{start_node_name}' defined in workflow but not found in 'nodes' section."
                logger.error(error_msg)
                return {"status": "error", "message": error_msg, "results": {}, "node_status": self.node_execution_status, "execution_id": exec_id}

            logger.info(f"Workflow starting at node: {start_node_name}")
            execution_queue.append((start_node_name, None)) # Start node has no preceding result

            # --- Main Execution Loop ---
            while execution_queue:
                # Check timeout at the beginning of each iteration
                if self.sandbox_timeout > 0 and (datetime.now() - self.sandbox_start_time).total_seconds() > self.sandbox_timeout:
                    timeout_msg = f"Workflow timeout ({self.sandbox_timeout}s) exceeded."
                    logger.error(timeout_msg)
                    # Update status of the node about to run (if any)
                    node_about_to_run = execution_queue[0][0] if execution_queue else "N/A"
                    if node_about_to_run != "N/A" and node_about_to_run in self.node_execution_status:
                         self.update_node_status(node_about_to_run, "error", f"Timeout before execution: {timeout_msg}")
                    return {"status": "error", "message": timeout_msg, "results": self.node_results, "node_status": self.node_execution_status, "execution_id": exec_id}

                node_name, previous_node_result_context = execution_queue.pop(0)

                # Skip if already executed (simple cycle prevention)
                # TODO: More sophisticated cycle handling might be needed for complex workflows
                if node_name in executed_nodes:
                    logger.info(f"Node '{node_name}' already executed in this run. Skipping to avoid simple loops.")
                    # Note: This prevents infinite loops but might block intentional cycles.
                    # Consider adding logic to allow re-entry based on conditions or specific node types if needed.
                    continue

                # Check if node exists before executing (safety check again, might be redundant but safe)
                if node_name not in self.workflow_data.get('nodes', {}):
                    logger.error(f"Node '{node_name}' was scheduled but is not defined in workflow 'nodes'. Stopping execution.")
                    # Update status if possible
                    if node_name in self.node_execution_status:
                         self.update_node_status(node_name, "error", "Node definition missing.")
                    return {"status": "error", "message": f"Node '{node_name}' not found in workflow definition.", "results": self.node_results, "node_status": self.node_execution_status, "execution_id": exec_id}

                logger.info(f"--- Executing Node: {node_name} ---")
                self.update_node_status(node_name, "running", "Node execution started")

                # Execute the node asynchronously
                try:
                    # Pass previous result for context if needed (e.g., for placeholder resolution if not handled globally)
                    node_result = await self.execute_node_async(node_name, input_context=previous_node_result_context)
                    self.node_results[node_name] = node_result # Store the raw result immediately
                    executed_nodes.add(node_name) # Mark as executed *after* successful or failed execution attempt
                except PlaceholderResolutionError as pre:
                    # Handle errors specifically from placeholder resolution during execute_node_async prep
                    error_msg = f"Critical placeholder resolution error for node '{node_name}': {pre}"
                    logger.error(error_msg, exc_info=False) # exc_info might be excessive here
                    self.update_node_status(node_name, "error", error_msg)
                    return {"status": "error", "message": error_msg, "results": self.node_results, "node_status": self.node_execution_status, "execution_id": exec_id}
                except Exception as node_exec_ex:
                    # Catch unexpected errors during the execute_node_async call itself
                    error_msg = f"Unexpected internal error preparing or running node '{node_name}': {node_exec_ex}"
                    logger.error(error_msg, exc_info=True)
                    self.update_node_status(node_name, "error", error_msg)
                    return {"status": "error", "message": error_msg, "results": self.node_results, "node_status": self.node_execution_status, "execution_id": exec_id}


                # --- Handle Node Result Status ---
                # Status should have been updated internally by execute_node_async, but we check the returned status for flow control.
                node_status = node_result.get('status') if isinstance(node_result, dict) else 'error' # Default to error if format is wrong

                if node_status == 'error':
                    error_msg = node_result.get('message', 'Unknown node error') if isinstance(node_result, dict) else 'Node returned non-dict result'
                    logger.error(f"Node '{node_name}' execution failed: {error_msg}. Stopping workflow.")
                    # Status already updated by execute_node_async on error
                    return {"status": "error", "message": f"Workflow failed at node '{node_name}': {error_msg}", "results": self.node_results, "node_status": self.node_execution_status, "execution_id": exec_id}
                else:
                    # Status already updated by execute_node_async
                    logger.info(f"Node '{node_name}' finished with status: {node_status}")

                # --- Queue Successors (Handling Conditional Logic) ---
                all_successors = self.actfile_parser.get_node_successors(node_name)
                logger.debug(f"Potential successors for '{node_name}': {all_successors}")
                current_node_type = self.workflow_data['nodes'][node_name].get('type')
                nodes_to_queue = []

                # Retrieve result data carefully for branching logic
                # Assumes node result structure is {'status': ..., 'result': {...}}
                result_data = node_result.get('result', {}) if isinstance(node_result, dict) else {}
                if not isinstance(result_data, dict):
                     logger.warning(f"Result data for node '{node_name}' is not a dictionary ({type(result_data).__name__}). Conditional branching may fail.")
                     result_data = {} # Prevent errors below

                # --- Conditional Branching Logic ---
                if current_node_type == 'if':
                    # Convention: Result should contain a boolean 'result' key
                    # Convention: Edge order matters: 0=True path, 1=False path
                    condition_outcome = result_data.get('result') # Can be None if key missing
                    if isinstance(condition_outcome, bool):
                        logger.info(f"IfNode '{node_name}' outcome: {condition_outcome}. Applying conditional branch.")
                        true_target = all_successors[0] if len(all_successors) > 0 else None
                        false_target = all_successors[1] if len(all_successors) > 1 else None
                        target_node_name = true_target if condition_outcome else false_target

                        if target_node_name:
                            nodes_to_queue.append(target_node_name)
                            logger.debug(f"IfNode '{node_name}' branching to: '{target_node_name}'")
                        elif condition_outcome and not true_target:
                            logger.warning(f"IfNode '{node_name}' was True, but no 'True' path (1st successor) defined. Path ends here.")
                        elif not condition_outcome and not false_target:
                            logger.warning(f"IfNode '{node_name}' was False, but no 'False' path (2nd successor) defined. Path ends here.")
                        else: # Should not happen if targets are None correctly
                            logger.info(f"IfNode '{node_name}' condition met ({condition_outcome}) but no corresponding path defined. Path ends.")
                    else:
                        logger.error(f"IfNode '{node_name}' did not return a boolean 'result' key in its result data (found type: {type(condition_outcome).__name__}). Cannot determine branch. Result data: {self.log_safe_node_data(result_data)}")
                        # Stop workflow? Or allow non-conditional successors? Stop is safer.
                        return {"status": "error", "message": f"IfNode '{node_name}' failed due to invalid result format.", "results": self.node_results, "node_status": self.node_execution_status, "execution_id": exec_id}

                elif current_node_type == 'switch':
                    # Convention: Result should contain 'selected_node' key with the name of the target node (or None/empty)
                    target_node_name = result_data.get('selected_node') # Can be None
                    if isinstance(target_node_name, str) and target_node_name:
                        # Validate that the selected node is actually a successor edge
                        if target_node_name in all_successors:
                             logger.info(f"SwitchNode '{node_name}' selected target: '{target_node_name}'.")
                             nodes_to_queue.append(target_node_name)
                        else:
                             logger.error(f"SwitchNode '{node_name}' selected target '{target_node_name}', but this node is not defined as a successor edge in the Actfile. Stopping.")
                             return {"status": "error", "message": f"SwitchNode '{node_name}' selected invalid target '{target_node_name}'.", "results": self.node_results, "node_status": self.node_execution_status, "execution_id": exec_id}
                    elif target_node_name is None or target_node_name == "":
                         logger.info(f"SwitchNode '{node_name}' selected no target (result was None or empty string). Path ends here.")
                    else:
                         logger.error(f"SwitchNode '{node_name}' did not return a valid string 'selected_node' key in its result data (found type: {type(target_node_name).__name__}). Cannot branch. Result data: {self.log_safe_node_data(result_data)}")
                         # Stop workflow? Or allow non-conditional successors? Stop is safer.
                         return {"status": "error", "message": f"SwitchNode '{node_name}' failed due to invalid result format.", "results": self.node_results, "node_status": self.node_execution_status, "execution_id": exec_id}

                else: # Default behavior: Queue all direct successors defined in edges
                     logger.debug(f"Node type '{current_node_type}' is not conditional. Queueing all defined successors.")
                     nodes_to_queue.extend(all_successors)

                # --- Add Valid Successors to Queue ---
                queued_count = 0
                for successor_name in nodes_to_queue:
                     if not successor_name:
                         logger.debug(f"Skipping empty successor name from node '{node_name}'.")
                         continue
                     if successor_name not in self.workflow_data.get('nodes', {}):
                         logger.warning(f"Target node '{successor_name}' (from '{node_name}') is not defined in the workflow 'nodes' section. Skipping this path.")
                         continue
                     # Avoid adding duplicates to the queue in the same iteration (e.g., if node branches to same target twice)
                     if any(item[0] == successor_name for item in execution_queue):
                         logger.debug(f"Target node '{successor_name}' is already in the execution queue. Skipping duplicate add.")
                         continue
                     if successor_name in executed_nodes:
                         logger.debug(f"Target node '{successor_name}' has already been executed. Skipping queuing (avoids simple loops).")
                         continue

                     logger.info(f"Queueing next node: '{successor_name}' (from '{node_name}')")
                     # Pass the current node's result as context for the next node
                     execution_queue.append((successor_name, node_result))
                     # Ensure the queued node has a 'pending' status if not already set
                     if successor_name not in self.node_execution_status or self.node_execution_status[successor_name]['status'] not in ['running', 'error', 'success', 'warning']:
                        self.update_node_status(successor_name, "pending", f"Queued after '{node_name}'")
                     queued_count += 1

                if not nodes_to_queue:
                    logger.debug(f"Node '{node_name}' produced no successors to queue.")
                elif queued_count == 0 and nodes_to_queue:
                     logger.debug(f"Node '{node_name}' had potential successors {nodes_to_queue}, but none were valid or needed queuing.")


            # --- Loop Finished Successfully ---
            logger.info(f"Workflow execution queue completed successfully for ID: {exec_id}")

            # Final post-processing to resolve any remaining placeholders (e.g., Set node values referencing later nodes)
            # self.resolve_all_node_results() # Optional: Can be useful but adds complexity

            return {"status": "success", "message": "Workflow executed successfully", "results": self.node_results, "node_status": self.node_execution_status, "execution_id": exec_id}

        except Exception as e:
            # Catch unexpected errors within the main loop or setup
            logger.error(f"Unexpected error during async workflow execution loop for {exec_id}: {e}", exc_info=True)
            last_node = locals().get('node_name', 'N/A') # Get the node being processed if possible
            if last_node != "N/A" and last_node in self.node_execution_status:
                 self.update_node_status(last_node, "error", f"Workflow loop error: {e}")
            # Return error status
            return {"status": "error", "message": f"Workflow failed unexpectedly during execution: {e}", "results": self.node_results, "node_status": self.node_execution_status, "execution_id": exec_id}

    async def execute_node_async(self, node_name: str, input_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes a single node: gets config, resolves placeholders, prepares data, calls executor.
        Handles placeholder resolution with caching, debugging, fallbacks, and circular reference checks.
        """
        if self.resolution_debug_mode: logger.debug(f"EXEC_NODE_ASYNC: Starting execution for node '{node_name}'")
        try:
            # 1. Get Config & Basic Validation
            if not self.workflow_data or node_name not in self.workflow_data.get('nodes', {}):
                raise NodeExecutionError(f"Node '{node_name}' configuration not found in workflow data.")

            # Use deepcopy to avoid modifying the original workflow data during resolution
            node_config = copy.deepcopy(self.workflow_data['nodes'][node_name])
            node_type = node_config.get('type')

            if not node_type:
                raise NodeExecutionError(f"Node '{node_name}' definition is missing the required 'type' field.")

            # 2. Resolve Placeholders with advanced features
            if self.resolution_debug_mode: logger.debug(f"EXEC_NODE_ASYNC: Resolving placeholders for '{node_name}' (type: {node_type}). Config before: {self.log_safe_node_data(node_config)}")
            try:
                # Start resolution with an empty stack for circular reference detection
                resolution_stack: Set[str] = set()
                resolved_node_config = self.resolve_placeholders_recursively(node_config, resolution_stack)
                if self.resolution_debug_mode: logger.debug(f"EXEC_NODE_ASYNC: '{node_name}' config AFTER resolving: {self.log_safe_node_data(resolved_node_config)}")
            except PlaceholderResolutionError as resolve_err:
                 # This catches circular references or potentially other resolution failures if configured
                 raise NodeExecutionError(f"Failed placeholder resolution for node '{node_name}': {resolve_err}") from resolve_err
            except Exception as resolve_err:
                 # Catch unexpected errors during resolution
                 logger.error(f"Unexpected error during placeholder resolution for '{node_name}': {resolve_err}", exc_info=True)
                 raise NodeExecutionError(f"Unexpected error resolving placeholders for node '{node_name}': {resolve_err}") from resolve_err

            # 3. Prepare Data for Executor (Includes type conversion)
            if self.resolution_debug_mode: logger.debug(f"EXEC_NODE_ASYNC: Processing resolved parameters for '{node_name}'...")
            processed_data = self._process_node_parameters(resolved_node_config)
            executor_data = self._structure_data_for_executor(processed_data, node_name, input_context)
            if self.resolution_debug_mode: logger.debug(f"EXEC_NODE_ASYNC: Final data package for executor '{node_name}': {self.log_safe_node_data(executor_data)}")

            # 4. Get Executor Instance
            executor = self.node_executors.get(node_type)
            if not executor:
                # This should ideally be caught during loading, but double-check
                raise NodeExecutionError(f"No executor instance loaded for type '{node_type}' (node: '{node_name}'). Check loading status.")

            # 5. Execute Node Logic
            logger.info(f"Calling {type(executor).__name__}.execute for node '{node_name}'")
            execute_method = getattr(executor, 'execute', None)
            if not callable(execute_method):
                raise NodeExecutionError(f"Executor for node type '{node_type}' (class {type(executor).__name__}) has no callable 'execute' method.")

            node_result = None
            start_time = datetime.now()
            try:
                if inspect.iscoroutinefunction(execute_method):
                    node_result = await execute_method(executor_data)
                else:
                    # Execute synchronous node in a thread pool to avoid blocking the event loop
                    # logger.warning(f"Executing synchronous node '{node_name}' ({node_type}) in thread pool.")
                    loop = asyncio.get_running_loop()
                    # Pass executor_data using functools.partial or lambda to avoid scope issues
                    node_result = await loop.run_in_executor(None, lambda data=executor_data: execute_method(data))

                # Handle cases where sync function mistakenly returns awaitable (less likely with run_in_executor)
                if inspect.iscoroutine(node_result):
                    logger.warning(f"Execute method for '{node_name}' returned an awaitable unexpectedly. Awaiting it.")
                    node_result = await node_result

            except Exception as exec_err:
                 # Catch errors *during* the node's execute method
                 logger.error(f"Error during {node_type}.execute() for node '{node_name}': {exec_err}", exc_info=True)
                 # Wrap the execution error
                 raise NodeExecutionError(f"Node execution failed: {exec_err}") from exec_err
            finally:
                 duration = datetime.now() - start_time
                 logger.info(f"Node '{node_name}' execution took {duration.total_seconds():.3f} seconds.")


            # 6. Process and Validate Result Structure
            if self.resolution_debug_mode: logger.debug(f"EXEC_NODE_ASYNC: Node '{node_name}' raw result: {self.log_safe_node_data(node_result)}")

            if not isinstance(node_result, dict) or 'status' not in node_result:
                 logger.warning(f"Node '{node_name}' result is not a dict or missing 'status'. Wrapping. Original result: {node_result}")
                 # Try to preserve the original result under a 'result' key if possible
                 final_result = {
                     "status": "warning", # Treat unexpected format as a warning
                     "message": "Node returned unexpected result format (expected dict with 'status' key).",
                     "result": node_result # Store the original problematic result
                 }
            else:
                 final_result = node_result # Result seems structurally okay

            # Validate and sanitize status
            node_status = final_result.get('status', 'error') # Default to error if status somehow becomes None
            valid_statuses = ['success', 'error', 'warning']
            if node_status not in valid_statuses:
                 logger.warning(f"Node '{node_name}' returned invalid status '{node_status}'. Normalizing to 'warning'.")
                 original_message = final_result.get('message', '')
                 final_result['status'] = 'warning'
                 final_result['message'] = f"[Invalid Status '{node_status}'] {original_message}"
                 node_status = 'warning' # Use the normalized status

            node_message = final_result.get('message', '') # Get message after potential normalization

            # 7. Handle Special Node Post-processing (e.g., caching 'set' results)
            if node_type == 'set' and node_status != 'error': # Only process if set node didn't fail
                set_result_data = final_result.get('result', {})
                if isinstance(set_result_data, dict):
                    key = set_result_data.get('key')
                    value = set_result_data.get('value') # Value might still be a placeholder here
                    if key and isinstance(key, str):
                        # Store the value associated with this key for {{key:key_name}} resolution
                        self.resolved_values_by_key[key] = value
                        if self.resolution_debug_mode: logger.debug(f"EXEC_NODE_ASYNC: Stored value from 'set' node '{node_name}' for key '{key}': {self.log_safe_node_data(value)}")
                    else:
                         logger.warning(f"'Set' node '{node_name}' result missing 'key' or key is not a string in its result data: {self.log_safe_node_data(set_result_data)}")

            # Update global status based on the final node result
            self.update_node_status(node_name, node_status, node_message)
            return final_result # Return the processed result

        except (NodeExecutionError, NodeValidationError, ActfileParserError) as e:
             # Catch errors specific to node execution setup or known validation issues
             error_msg = f"Error executing node {node_name}: {e}"
             logger.error(error_msg, exc_info=False) # Typically don't need full trace for these
             self.update_node_status(node_name, "error", error_msg)
             return {"status": "error", "message": error_msg, "error_type": type(e).__name__}
        except FileNotFoundError as e:
            # Catch file not found errors specifically (e.g., node needs a file)
             error_msg = f"File not found during execution of node {node_name}: {e}"
             logger.error(error_msg, exc_info=False)
             self.update_node_status(node_name, "error", error_msg)
             return {"status": "error", "message": error_msg, "error_type": type(e).__name__}
        except Exception as e:
             # Catch any other unexpected errors during the process
             error_msg = f"Unexpected internal error during execution preparation or finalization for node {node_name}: {str(e)}"
             logger.error(error_msg, exc_info=True) # Log full trace for unexpected errors
             self.update_node_status(node_name, "error", error_msg)
             return {"status": "error", "message": error_msg, "error_type": type(e).__name__}

    def _structure_data_for_executor(self,
                                     processed_data: Dict[str, Any],
                                     node_name: str,
                                     previous_node_result_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Organizes processed data into the structure expected by node execute methods."""
        executor_data = {}
        params = {}
        # Standard keys often found directly in node config (metadata)
        metadata_keys = {'type', 'label', 'position_x', 'position_y', 'description'}

        for k, v in processed_data.items():
            if k in metadata_keys:
                executor_data[k] = v
            else:
                # Assume everything else is a parameter for the node logic
                params[k] = v

        executor_data['params'] = params
        # Add execution context metadata, prefixed for clarity
        executor_data['__node_name'] = node_name
        executor_data['__execution_id'] = self.current_execution_id
        # Optionally include the previous node's result if needed (might be large)
        # executor_data['__previous_result'] = previous_node_result_context
        if self.resolution_debug_mode: logger.debug(f"Structuring data for executor {node_name}. Metadata keys: {metadata_keys}. Params keys: {list(params.keys())}")

        return executor_data

    def _process_node_parameters(self, resolved_node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempts type conversions on resolved values (bool, numeric, JSON).
        Operates on the already placeholder-resolved data.
        """
        processed_data = resolved_node_data.copy() # Work on a copy
        if self.resolution_debug_mode: logger.debug(f"PROCESS_PARAMS: Starting type conversion processing for keys: {list(processed_data.keys())}")

        for key, value in processed_data.items():
            # Only attempt conversion if the value is currently a string
            if isinstance(value, str):
                original_value_repr = repr(value)
                new_value = value # Start with the original string value
                conversion_applied = False

                # Skip conversion if it still looks like an unresolved placeholder (safety check)
                # This might happen if resolution failed and fallbacks weren't used or also failed
                if (value.startswith('{{') and value.endswith('}}')) or \
                   (value.startswith('${') and value.endswith('}')):
                    if self.resolution_debug_mode: logger.debug(f"PROCESS_PARAMS: Key '{key}' value '{original_value_repr}' looks like unresolved placeholder. Skipping conversion.")
                    continue

                # 1. Try boolean conversion first (simple cases)
                if value.lower() == 'true':
                    new_value = True
                    conversion_applied = True
                elif value.lower() == 'false':
                    new_value = False
                    conversion_applied = True

                # 2. Try numeric conversion (int then float) if not boolean
                # Be careful with strings that look numeric but shouldn't be (e.g., version numbers "1.0")
                # We only convert if it strictly matches numeric patterns.
                elif not conversion_applied:
                    # Try integer (allows leading sign)
                    if re.fullmatch(r'-?\d+', value):
                         try:
                             new_value = int(value)
                             conversion_applied = True
                         except ValueError: pass # Should not happen with regex match, but safety
                    # Try float if not integer (allows sign, decimal, requires digits)
                    elif re.fullmatch(r'-?\d+(\.\d+)?', value) or re.fullmatch(r'-?\.\d+', value):
                         try:
                             new_value = float(value)
                             conversion_applied = True
                         except ValueError: pass # Safety

                # 3. Try JSON decoding for structural hints or common keys (if no other conversion applied)
                # This is heuristic and might misinterpret some strings.
                elif not conversion_applied:
                    looks_like_json = (value.strip().startswith(('[', '{')) and value.strip().endswith((']', '}')))
                    # Add more keys if specific nodes commonly use JSON strings for certain params
                    is_potential_json_key = key.lower() in [
                        'messages', 'json_body', 'data', 'payload', 'headers',
                        'items', 'list', 'options', 'config', 'arguments', 'parameters'
                    ]

                    if looks_like_json or is_potential_json_key:
                        try:
                            decoded_json = json.loads(value)
                            # Only accept if it looks like JSON *and* decodes successfully
                            if looks_like_json:
                                 new_value = decoded_json
                                 conversion_applied = True
                                 if self.resolution_debug_mode: logger.debug(f"PROCESS_PARAMS: Key '{key}' looked like JSON and decoded successfully.")
                            # If it was just a potential key match, be more cautious
                            elif is_potential_json_key:
                                 # Maybe only accept if the result is dict/list?
                                 if isinstance(decoded_json, (dict, list)):
                                      new_value = decoded_json
                                      conversion_applied = True
                                      if self.resolution_debug_mode: logger.debug(f"PROCESS_PARAMS: Key '{key}' matched potential JSON key and decoded to dict/list.")
                                 else:
                                      if self.resolution_debug_mode: logger.debug(f"PROCESS_PARAMS: Key '{key}' matched potential JSON key but decoded to non-container type ({type(decoded_json).__name__}). Keeping as string.")
                        except json.JSONDecodeError:
                            if looks_like_json and self.resolution_debug_mode:
                                logger.debug(f"PROCESS_PARAMS: Key '{key}' value looked like JSON but failed to decode. Keeping as string.")
                            # Don't log if it was just a potential key match that failed decode

                # Log if conversion happened
                if conversion_applied:
                    processed_data[key] = new_value
                    if self.resolution_debug_mode: logger.debug(f"PROCESS_PARAMS: Converted key '{key}': {original_value_repr}(str) -> {repr(new_value)}({type(new_value).__name__})")
            else:
                # Value is not a string, no conversion needed/possible here
                if self.resolution_debug_mode: logger.debug(f"PROCESS_PARAMS: Key '{key}' is already type {type(value).__name__}. No string conversion needed.")


        if self.resolution_debug_mode: logger.debug(f"PROCESS_PARAMS: Finished parameter type conversion.")
        return processed_data

    # --- Advanced Placeholder Resolution ---

    def resolve_placeholders_recursively(self, data: Any, resolution_stack: Set[str]) -> Any:
        """
        Recursively resolves placeholders in data structures (dicts, lists, strings)
        with caching, circular reference detection, and fallback support.

        Args:
            data: The data structure (dict, list, string, etc.) to resolve.
            resolution_stack: A set tracking placeholders currently being resolved
                              in the recursion chain to detect cycles.

        Returns:
            The data structure with placeholders resolved.

        Raises:
            PlaceholderResolutionError: If a circular reference is detected or if
                                        `self.fail_on_unresolved` is True and a
                                        placeholder cannot be resolved.
        """
        if isinstance(data, dict):
            resolved_dict = {}
            for key, value in data.items():
                # Resolve value first, then potentially the key if it's also a string placeholder
                resolved_value = self.resolve_placeholders_recursively(value, resolution_stack)

                # Key resolution is less common, but possible
                if isinstance(key, str) and ('{{' in key or '${' in key):
                    resolved_key = self.resolve_placeholder_string(key, resolution_stack)
                    if not isinstance(resolved_key, str):
                        logger.warning(f"Placeholder key '{key}' resolved to non-string type ({type(resolved_key).__name__}). Using original key.")
                        resolved_key = key
                else:
                    resolved_key = key

                resolved_dict[resolved_key] = resolved_value
            return resolved_dict
        elif isinstance(data, list):
            # Resolve each item in the list
            return [self.resolve_placeholders_recursively(item, resolution_stack) for item in data]
        elif isinstance(data, str):
            # Resolve placeholders within the string
            return self.resolve_placeholder_string(data, resolution_stack)
        else:
            # Not a dict, list, or string - return as is
            return data

    def resolve_placeholder_string(self, text: str, resolution_stack: Set[str]) -> Any:
        """
        Resolves ${ENV_VAR} and {{source.path | fallback}} placeholders within a string.
        Handles caching, circular reference detection, full vs partial replacement.

        Args:
            text: The string possibly containing placeholders.
            resolution_stack: Set tracking current resolution chain.

        Returns:
            The resolved value. If the entire string was a single placeholder, returns
            the native type (int, bool, dict, list, etc.). If placeholders were part
            of a larger string, returns a string with replacements. If resolution fails,
            returns the original text or fallback value.

        Raises:
            PlaceholderResolutionError: On circular reference or if fail_on_unresolved=True.
        """
        if not isinstance(text, str) or not ('${' in text or '{{' in text):
             # Optimization: If no placeholder markers exist, return immediately
             return text

        # --- 0. Check Cache for the exact string ---
        # Cache key is the raw placeholder string itself
        if text in self.resolution_cache:
            if self.resolution_debug_mode: logger.debug(f"RESOLVE_STR: Cache hit for '{text}'")
            return self.resolution_cache[text]

        # --- Check for Circular Reference ---
        if text in resolution_stack:
            cycle_path = " -> ".join(list(resolution_stack) + [text])
            logger.error(f"Circular placeholder reference detected: {cycle_path}")
            raise PlaceholderResolutionError(f"Circular reference detected: {cycle_path}")

        # Add current placeholder to the stack for this resolution branch
        resolution_stack.add(text)
        if self.resolution_debug_mode: logger.debug(f"RESOLVE_STR: Added '{text}' to stack: {resolution_stack}")

        resolved_value = text # Default to original text if resolution fails

        try:
            # --- 1. Environment Variables ${...} ---
            # Resolve these first, as they might form part of a workflow placeholder
            env_var_pattern = re.compile(r'\$\{([A-Za-z_][A-Za-z0-9_]*)\}')
            resolved_text_env = text
            offset = 0
            for match in env_var_pattern.finditer(text):
                 var_name = match.group(1)
                 env_value = os.environ.get(var_name)

                 start, end = match.span()
                 start += offset
                 end += offset
                 placeholder = match.group(0)

                 if env_value is not None:
                     if self.resolution_debug_mode: logger.debug(f"RESOLVE_STR: Resolved env var '{placeholder}'")
                     resolved_text_env = resolved_text_env[:start] + env_value + resolved_text_env[end:]
                     offset += len(env_value) - len(placeholder)
                 else:
                     logger.warning(f"Env var '${{{var_name}}}' not found. Leaving placeholder.")
                     # Keep the original placeholder text, offset doesn't change

            current_text = resolved_text_env # Use the env-resolved text for further processing

            # --- 2. Workflow Placeholders {{...}} ---
            placeholder_pattern = re.compile(r'\{\{(.*?)\}\}') # Non-greedy match inside {{}}
            matches = list(placeholder_pattern.finditer(current_text))

            if not matches:
                # No workflow placeholders found (after env var resolution)
                resolved_value = current_text
            else:
                # --- Full String Match Check ---
                # If the entire string (ignoring leading/trailing whitespace) is one placeholder
                first_match = matches[0]
                is_full_match = len(matches) == 1 and first_match.group(0) == current_text.strip()

                if is_full_match:
                    placeholder_content_full = first_match.group(1).strip()
                    if not placeholder_content_full:
                        resolved_value = current_text # Empty placeholder {{}}, return original
                    else:
                        if self.resolution_debug_mode: logger.debug(f"RESOLVE_STR: Attempting FULL resolution for: '{{{{{placeholder_content_full}}}}}'")
                        # Resolve the content, potentially returning native type
                        resolved_native = self._resolve_single_placeholder_content(placeholder_content_full, resolution_stack)

                        if resolved_native is not None:
                             resolved_value = resolved_native # Keep the native type
                             if self.resolution_debug_mode: logger.debug(f"RESOLVE_STR: Full placeholder resolved to type {type(resolved_value).__name__}")
                        else:
                             # Resolution failed for the full placeholder
                             logger.warning(f"RESOLVE_STR: Could not resolve full placeholder '{{{{{placeholder_content_full}}}}}'. Returning original text fragment: '{current_text}'")
                             if self.fail_on_unresolved:
                                  raise PlaceholderResolutionError(f"Unresolved placeholder: '{{{{{placeholder_content_full}}}}}' and fail_on_unresolved is True.")
                             resolved_value = current_text # Return original string as resolution failed

                else:
                    # --- Partial/Multiple Placeholder Replacement ---
                    if self.resolution_debug_mode: logger.debug(f"RESOLVE_STR: Performing partial/multiple replacements in: '{current_text}'")
                    resolved_text_partial = current_text
                    offset = 0 # Offset for string modifications

                    for match in matches:
                        start, end = match.span()
                        start += offset
                        end += offset

                        full_placeholder = match.group(0)
                        placeholder_content_partial = match.group(1).strip()
                        if not placeholder_content_partial: continue # Skip empty {{}}

                        # Resolve the content, expect string representation for embedding
                        value_partial = self._resolve_single_placeholder_content(placeholder_content_partial, resolution_stack)

                        if value_partial is not None:
                            # Convert resolved value to string for embedding
                            str_value = str(value_partial)
                            if self.resolution_debug_mode: logger.debug(f"RESOLVE_STR: Replacing partial '{{{{{placeholder_content_partial}}}}}' with string: '{str_value[:50]}{'...' if len(str_value)>50 else ''}'")

                            resolved_text_partial = resolved_text_partial[:start] + str_value + resolved_text_partial[end:]
                            offset += len(str_value) - len(full_placeholder) # Adjust offset
                        else:
                            # Failed to resolve this partial placeholder
                            logger.warning(f"RESOLVE_STR: Could not resolve partial placeholder '{{{{{placeholder_content_partial}}}}}'. Leaving it in the string.")
                            if self.fail_on_unresolved:
                                 raise PlaceholderResolutionError(f"Unresolved placeholder: '{{{{{placeholder_content_partial}}}}}' and fail_on_unresolved is True.")
                            # Keep original placeholder, no change in offset needed unless len differs (unlikely here)

                    resolved_value = resolved_text_partial # Final string after all replacements

        except PlaceholderResolutionError:
             raise # Propagate resolution errors (circular ref, fail_on_unresolved)
        except Exception as e:
            logger.error(f"RESOLVE_STR: Unexpected error resolving string '{text}': {e}", exc_info=True)
            # Depending on policy, either raise or return original text
            # Returning original is often safer for continuing workflow, but hides errors.
            # Let's re-raise as a PlaceholderResolutionError for clarity
            raise PlaceholderResolutionError(f"Unexpected error resolving string '{text}': {e}") from e
        finally:
            # --- Remove from stack and Cache Result ---
            resolution_stack.remove(text)
            if self.resolution_debug_mode: logger.debug(f"RESOLVE_STR: Removed '{text}' from stack: {resolution_stack}")

            # Cache the final resolved value (could be native type or string) against the original text key
            self.resolution_cache[text] = resolved_value
            if self.resolution_debug_mode: logger.debug(f"RESOLVE_STR: Cached result for '{text}': {self.log_safe_node_data(resolved_value)}")

        return resolved_value


    def _resolve_single_placeholder_content(self, content: str, resolution_stack: Set[str]) -> Any:
         """
         Resolves the content inside {{...}}, handling 'key:' prefix, 'source.path',
         and '|' fallback values. Calls fetch_value for source.path resolution.

         Args:
             content: The raw string content inside {{ }}.
             resolution_stack: Set tracking current resolution chain.

         Returns:
             The resolved value (can be any type), or None if resolution fails and
             no fallback is provided or the fallback itself fails.
         """
         content = content.strip()
         if not content:
             return None # Skip empty content

         # --- Parse Content and Fallback ---
         parts = content.split('|', 1)
         main_content = parts[0].strip()
         fallback_str = parts[1].strip() if len(parts) > 1 else None

         if self.resolution_debug_mode: logger.debug(f"RESOLVE_CONTENT: Processing content='{main_content}'" + (f", fallback='{fallback_str}'" if fallback_str else ""))

         # --- Check Cache for the main content part ---
         # Cache key is the content string itself (e.g., "key:my_value" or "nodeA.result.data")
         if main_content in self.resolution_cache:
              if self.resolution_debug_mode: logger.debug(f"RESOLVE_CONTENT: Cache hit for content '{main_content}'")
              # Need to re-check stack even on cache hit to prevent cycles across different strings resolving the same content
              if main_content in resolution_stack:
                   cycle_path = " -> ".join(list(resolution_stack) + [main_content])
                   raise PlaceholderResolutionError(f"Circular reference detected via cache hit: {cycle_path}")
              return self.resolution_cache[main_content]

         # --- Add main_content to stack if resolving further ---
         # Note: We added the *full string* placeholder in resolve_placeholder_string.
         # Adding the *content* here helps detect cycles like {{key:A}} where A's value is {{key:A}}.
         if main_content in resolution_stack:
              cycle_path = " -> ".join(list(resolution_stack) + [main_content])
              raise PlaceholderResolutionError(f"Circular reference detected on content: {cycle_path}")

         resolution_stack.add(main_content)
         if self.resolution_debug_mode: logger.debug(f"RESOLVE_CONTENT: Added '{main_content}' to content stack: {resolution_stack}")

         resolved_value = None
         resolution_failed = False

         try:
             # --- Resolve based on prefix or structure ---
             if main_content.startswith('key:'):
                 key_name = main_content[len('key:'):].strip()
                 if not key_name:
                     logger.warning("RESOLVE_CONTENT: Placeholder used 'key:' prefix with an empty key name.")
                     resolution_failed = True
                 else:
                     if self.resolution_debug_mode: logger.debug(f"RESOLVE_CONTENT: Attempting fetch using key: '{key_name}'")
                     if key_name in self.resolved_values_by_key:
                         resolved_value = self.resolved_values_by_key[key_name]
                         if self.resolution_debug_mode: logger.debug(f"RESOLVE_CONTENT: Found key '{key_name}' in resolved_values_by_key cache.")
                         # The fetched value might itself be a placeholder string, resolve it recursively.
                         resolved_value = self.resolve_placeholders_recursively(resolved_value, resolution_stack)
                     else:
                         logger.warning(f"RESOLVE_CONTENT: Key '{key_name}' not found in resolved values cache (set by 'set' nodes).")
                         resolution_failed = True

             else: # Assume 'source_id.path.to.value' or just 'source_id'
                 source_id, path = self._split_placeholder_path(main_content)
                 if source_id == '__invalid_source__':
                      logger.warning(f"RESOLVE_CONTENT: Invalid placeholder source detected in '{main_content}'.")
                      resolution_failed = True
                 else:
                      if self.resolution_debug_mode: logger.debug(f"RESOLVE_CONTENT: Attempting fetch from source='{source_id}', path='{path}'")
                      # fetch_value handles looking in input/results and traversing the path
                      # It can return None if source/path not found
                      fetched_value = self.fetch_value(source_id, path)
                      if fetched_value is not None:
                           # The fetched value might contain further placeholders
                           resolved_value = self.resolve_placeholders_recursively(fetched_value, resolution_stack)
                      else:
                           # fetch_value returned None, indicating failure
                           resolution_failed = True
                           # Logged within fetch_value

             # --- Handle Resolution Failure & Fallback ---
             if resolution_failed:
                  if fallback_str is not None:
                       if self.resolution_debug_mode: logger.debug(f"RESOLVE_CONTENT: Resolution failed for '{main_content}', using fallback '{fallback_str}'")
                       # Parse the fallback string into a potential type
                       resolved_value = self._parse_fallback_value(fallback_str)
                       # Fallback value itself could contain placeholders - resolve them
                       resolved_value = self.resolve_placeholders_recursively(resolved_value, resolution_stack)
                  else:
                       if self.resolution_debug_mode: logger.debug(f"RESOLVE_CONTENT: Resolution failed for '{main_content}' and no fallback provided.")
                       resolved_value = None # Explicitly None if failed without fallback

         except PlaceholderResolutionError:
              raise # Propagate critical resolution errors
         except Exception as e:
              logger.error(f"RESOLVE_CONTENT: Unexpected error resolving content '{content}': {e}", exc_info=True)
              resolution_failed = True
              resolved_value = None # Ensure None on unexpected error
              # Use fallback if available even on unexpected error? Yes.
              if fallback_str is not None:
                   if self.resolution_debug_mode: logger.debug(f"RESOLVE_CONTENT: Using fallback '{fallback_str}' due to unexpected error.")
                   resolved_value = self._parse_fallback_value(fallback_str)
                   resolved_value = self.resolve_placeholders_recursively(resolved_value, resolution_stack)
         finally:
             # --- Remove content from stack and Cache ---
             resolution_stack.remove(main_content)
             if self.resolution_debug_mode: logger.debug(f"RESOLVE_CONTENT: Removed '{main_content}' from content stack: {resolution_stack}")

             # Cache the result for this specific content string
             # This caches "nodeA.result.value" -> final_value
             self.resolution_cache[main_content] = resolved_value
             if self.resolution_debug_mode: logger.debug(f"RESOLVE_CONTENT: Cached result for content '{main_content}': {self.log_safe_node_data(resolved_value)}")


         return resolved_value

    def _parse_fallback_value(self, fallback_str: str) -> Any:
        """Attempts to parse a fallback string into bool, int, float, or leaves as string."""
        fallback_str = fallback_str.strip()
        # Try boolean
        if fallback_str.lower() == 'true': return True
        if fallback_str.lower() == 'false': return False
        # Try null/None
        if fallback_str.lower() == 'null' or fallback_str.lower() == 'none': return None
        # Try int
        if re.fullmatch(r'-?\d+', fallback_str):
            try: return int(fallback_str)
            except ValueError: pass
        # Try float
        if re.fullmatch(r'-?\d+(\.\d+)?', fallback_str) or re.fullmatch(r'-?\.\d+', fallback_str):
            try: return float(fallback_str)
            except ValueError: pass
        # Try JSON decode for lists/dicts if quoted appropriately
        if (fallback_str.startswith('"') and fallback_str.endswith('"')) or \
           (fallback_str.startswith("'") and fallback_str.endswith("'")):
             try:
                 # Attempt to decode the *inner* string content as JSON
                 inner_str = fallback_str[1:-1]
                 if (inner_str.startswith('[') and inner_str.endswith(']')) or \
                    (inner_str.startswith('{') and inner_str.endswith('}')):
                      return json.loads(inner_str)
             except (json.JSONDecodeError, TypeError): pass # Ignore if not valid JSON or not string

        # Default: return the string itself (unquoted if it was quoted)
        if (fallback_str.startswith('"') and fallback_str.endswith('"')) or \
           (fallback_str.startswith("'") and fallback_str.endswith("'")):
            if len(fallback_str) >= 2:
                 return fallback_str[1:-1]
            else: # Handles empty quotes "" or ''
                 return ""

        return fallback_str # Return as string if no other type matches

    def _split_placeholder_path(self, content: str) -> Tuple[str, str]:
         """Splits 'source.path.to.value' into ('source', 'path.to.value'). Handles cases with no dot."""
         # Ensure valid characters for source ID (alphanumeric, underscore, hyphen?)
         # Simple split for now.
         parts = content.split('.', 1)
         source_id = parts[0].strip()
         path = parts[1].strip() if len(parts) > 1 else ""

         # Basic validation for source_id
         if not source_id or not re.match(r'^[a-zA-Z0-9_\-]+$', source_id):
             # Allow 'input' specifically
             if source_id == 'input':
                 pass # Valid source
             else:
                  logger.warning(f"Placeholder content '{content}' resulted in potentially invalid source_id '{source_id}'. Resolution may fail.")
                  # Return potentially invalid source_id anyway, fetch_value will handle not finding it.
                  # Or return ('__invalid_source__', path) for stricter handling? Let fetch_value decide.

         return source_id, path

    def fetch_value(self, source_id: str, path: str) -> Any:
        """
        Fetches a value from initial input ('input' source) or node results
        (using node name as source). Uses a dot-separated path to navigate
        nested dictionaries and lists. Handles list indexing.

        Args:
            source_id: 'input' or the name of a node.
            path: Dot-separated path (e.g., 'data.user.name', 'results[0].id').

        Returns:
            The fetched value, or None if the source or path is invalid/not found.
        """
        if self.resolution_debug_mode: logger.debug(f"FETCH_VALUE: Attempting fetch for source_id='{source_id}', path='{path}'")
        base_value = None

        # --- Determine Base Value Source ---
        if source_id == 'input':
            if isinstance(self.initial_input_data, dict):
                # Allow {{input}} to refer to the whole dict, or {{input.key}}
                base_value = self.initial_input_data
                if self.resolution_debug_mode: logger.debug(f"FETCH_VALUE: Source is 'input'. Base value type: {type(base_value).__name__}")
            else:
                logger.warning(f"FETCH_VALUE: Source is 'input', but self.initial_input_data is not a dictionary (type: {type(self.initial_input_data).__name__}). Cannot fetch.")
                return None

        elif source_id in self.node_results:
            # Fetch from the stored results of a previously executed node
            base_value = self.node_results[source_id]
            if self.resolution_debug_mode: logger.debug(f"FETCH_VALUE: Source is node '{source_id}'. Base value type: {type(base_value).__name__}")

        elif source_id in self.workflow_data.get('nodes', {}):
             # Node exists but hasn't run or produced a result yet
             logger.warning(f"FETCH_VALUE: Source node '{source_id}' exists in workflow but has no result available yet in self.node_results.")
             return None # Cannot fetch value if node hasn't produced output
        else:
             logger.warning(f"FETCH_VALUE: Source ID '{source_id}' not found. It's neither 'input' nor a key in node_results nor a defined node name.")
             return None

        # --- Handle Empty Path ---
        if not path:
            if self.resolution_debug_mode: logger.debug(f"FETCH_VALUE: No path specified for source '{source_id}'. Returning base value directly.")
            return base_value

        # --- Traverse Path ---
        # Split path respecting potential numeric indices in brackets like field[0]
        # This regex splits by '.' but keeps bracketed indices together.
        # It finds either non-dot sequences, or bracketed sequences.
        path_parts = re.findall(r'[^.\[\]]+|\[\d+\]', path)
        if not path_parts or "".join(path_parts).replace('[','').replace(']','') != path.replace('[','').replace(']',''):
            # Fallback to simple dot splitting if regex fails or doesn't match original structure
            # This occurs if path has mixed formats or invalid characters
            logger.warning(f"FETCH_VALUE: Complex path '{path}' detected. Falling back to simple dot splitting. Indexing like '[0]' might not work correctly.")
            path_parts = path.split('.')

        current_value = base_value
        if self.resolution_debug_mode: logger.debug(f"FETCH_VALUE: Traversing path parts: {path_parts} starting from type: {type(current_value).__name__}")

        for i, part in enumerate(path_parts):
            current_path_log = ".".join(path_parts[:i+1]) # Approximate path for logging

            if part == '': # Should not happen with regex, but possible with split('.')
                logger.warning(f"FETCH_VALUE: Empty path part encountered at '{current_path_log}'. Skipping.")
                continue

            # Check for list index access first: "[number]"
            index_match = re.fullmatch(r'\[(\d+)\]', part)
            if index_match:
                 if isinstance(current_value, list):
                      try:
                          idx = int(index_match.group(1))
                          if 0 <= idx < len(current_value):
                              current_value = current_value[idx]
                              if self.resolution_debug_mode: logger.debug(f"  FETCH_VALUE: Path '{current_path_log}': Accessed list index {idx}. New value type: {type(current_value).__name__}")
                          else:
                              logger.warning(f"FETCH_VALUE: Index {idx} out of bounds for list of length {len(current_value)} at path '{current_path_log}'.")
                              return None # Out of bounds
                      except ValueError: # Should not happen with regex
                           logger.error(f"FETCH_VALUE: Invalid number in index '{part}' at path '{current_path_log}'.")
                           return None
                 else:
                      logger.warning(f"FETCH_VALUE: Path part '{part}' looks like list index, but current value at path '{'.'.join(path_parts[:i])}' is not a list (type: {type(current_value).__name__}).")
                      return None # Cannot index non-list
            # Dictionary key access
            elif isinstance(current_value, dict):
                if part in current_value:
                    current_value = current_value[part]
                    if self.resolution_debug_mode: logger.debug(f"  FETCH_VALUE: Path '{current_path_log}': Accessed dict key '{part}'. New value type: {type(current_value).__name__}")
                else:
                    # Special case: Check if 'result' sub-key exists if base was node result
                    # This provides convenient access like {{nodeA.key}} instead of {{nodeA.result.key}}
                    # Only do this if 'result' exists and the part is not 'result' itself
                    if part != 'result' and 'result' in current_value and isinstance(current_value['result'], dict) and part in current_value['result']:
                         logger.debug(f"  FETCH_VALUE: Key '{part}' not directly in node result, checking under 'result' sub-key.")
                         current_value = current_value['result'][part]
                         if self.resolution_debug_mode: logger.debug(f"  FETCH_VALUE: Path '{current_path_log}': Accessed dict key '{part}' under 'result'. New value type: {type(current_value).__name__}")
                    else:
                        logger.warning(f"FETCH_VALUE: Key '{part}' not found in dictionary at path '{current_path_log}'. Available keys: {list(current_value.keys())}")
                        return None # Key not found

            # Simple integer index access (if part is just digits and current value is list) - less robust than [idx]
            elif isinstance(current_value, list) and part.isdigit():
                 try:
                     idx = int(part)
                     if 0 <= idx < len(current_value):
                         current_value = current_value[idx]
                         if self.resolution_debug_mode: logger.debug(f"  FETCH_VALUE: Path '{current_path_log}': Accessed list index {idx} (direct digit). New value type: {type(current_value).__name__}")
                     else:
                         logger.warning(f"FETCH_VALUE: Index {idx} (direct digit) out of bounds for list of length {len(current_value)} at path '{current_path_log}'.")
                         return None
                 except ValueError: # Should not happen
                     logger.error(f"FETCH_VALUE: Invalid integer in path part '{part}'.")
                     return None
            # Cannot traverse further
            else:
                logger.warning(f"FETCH_VALUE: Cannot traverse further. Path part '{part}' requested, but current value at path '{'.'.join(path_parts[:i])}' is of type {type(current_value).__name__} (not dict or list, or index invalid).")
                return None

            # Check if traversal resulted in None before the end of the path
            if current_value is None and i < len(path_parts) - 1:
                 logger.warning(f"FETCH_VALUE: Path traversal encountered None at '{current_path_log}'. Cannot traverse further into remaining path '{'.'.join(path_parts[i+1:])}'.")
                 return None

        # --- Traversal Successful ---
        if self.resolution_debug_mode: logger.debug(f"FETCH_VALUE: Successfully fetched value for {source_id}.{path}. Final type: {type(current_value).__name__}")
        return current_value


    # --- Utility Methods ---

    @staticmethod
    def log_safe_node_data(node_data: Any, max_depth=5, current_depth=0) -> str:
        """
        Converts data to JSON string for logging, redacting sensitive keys and handling depth.
        Handles non-serializable data gracefully.
        """
        sensitive_keys = ['api_key', 'token', 'password', 'secret', 'credentials', 'auth', 'apikey', 'access_key', 'secret_key']

        if current_depth > max_depth:
            return f"[Max Depth Exceeded: {type(node_data).__name__}]"

        def redact_recursive(data: Any, depth: int) -> Any:
            if depth > max_depth:
                 return f"[Max Depth Exceeded: {type(data).__name__}]"

            if isinstance(data, dict):
                new_dict = {}
                for k, v in data.items():
                    # Redact key based on common sensitive names (case-insensitive substring check)
                    is_sensitive_key = isinstance(k, str) and any(s in k.lower() for s in sensitive_keys)
                    # Also redact value if key is sensitive (double safety)
                    if is_sensitive_key:
                        new_dict[k] = '[REDACTED]'
                    else:
                        # Also redact value if it's a string and looks sensitive (e.g. Bearer token) - less reliable
                        is_sensitive_value = isinstance(v, str) and ('bearer ' in v.lower() or 'sk_' in v or 'pk_' in v) # Example patterns
                        new_dict[k] = '[REDACTED]' if is_sensitive_value else redact_recursive(v, depth + 1)
                return new_dict
            elif isinstance(data, list):
                # Avoid redacting indices, only check list items
                return [redact_recursive(item, depth + 1) for item in data]
            elif isinstance(data, str):
                 # Basic check for sensitive patterns in standalone strings (less common)
                 is_sensitive_value = 'bearer ' in data.lower() or 'sk_' in data or 'pk_' in data
                 return '[REDACTED]' if is_sensitive_value else data
            else:
                # Return non-container types directly (numbers, bools, None)
                 return data

        try:
            # Apply redaction first
            safe_data = redact_recursive(node_data, current_depth)

            # Attempt to serialize the redacted data
            # Use default=str to handle non-standard types like datetime
            return json.dumps(safe_data, indent=2, default=str, ensure_ascii=False, sort_keys=False)
        except (TypeError, OverflowError) as json_err:
            # Fallback if JSON serialization fails even after redaction/default=str
            logger.debug(f"Could not JSON serialize safe data (type: {type(safe_data).__name__}): {json_err}")
            return f"[Non-Serializable Data: Type {type(node_data).__name__}]"
        except Exception as e:
            # Catch other unexpected errors during logging prep
            logger.error(f"Error creating log-safe representation: {e}", exc_info=False)
            return f"[Error Logging Data - Type: {type(node_data).__name__}, Error: {e}]"

    def _snake_case(self, name: str) -> str:
        """Converts PascalCase/CamelCase to snake_case."""
        if not name: return ""
        # Insert underscore before uppercase letters preceded by lowercase/digit
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        # Insert underscore before uppercase letters preceded by another uppercase letter,
        # but followed by a lowercase letter (e.g., SimpleHTTPServer -> Simple_HTTP_Server)
        name = re.sub('([A-Z])([A-Z][a-z])', r'\1_\2', name)
        return name.lower()

    def _print_node_execution_results(self):
        """Prints a summary table of final node execution statuses using tabulate."""
        print("\n--- Final Node Execution Status Summary ---")
        if not self.node_execution_status:
            print("No node statuses were recorded during execution.")
            print("-------------------------------------------\n")
            return

        headers = ["Node Name", "Final Status", "Message / Summary"]
        table_data = []

        # Ensure all nodes defined in the workflow are included, even if not reached
        all_node_names = set(self.workflow_data.get('nodes', {}).keys())
        all_node_names.update(self.node_execution_status.keys()) # Add any potentially dynamically added nodes? (unlikely now)
        sorted_node_names = sorted(list(all_node_names))

        for node_name in sorted_node_names:
            status_info = self.node_execution_status.get(node_name)

            if status_info:
                status = status_info.get('status', 'unknown')
                message = status_info.get('message', 'N/A')
                # Try to get a summary from result if message is generic success
                if status == 'success' and (not message or message == 'Success'):
                     node_result = self.node_results.get(node_name, {}).get('result')
                     if node_result is not None:
                         summary = self.log_safe_node_data(node_result, max_depth=1) # Show shallow result structure
                     else: summary = message
                else:
                     summary = message # Use the error/warning message
            else:
                # Node was defined but never reached/status updated
                status = 'skipped'
                summary = 'Node defined but not executed'

            # Truncate long summaries/results for display
            display_summary = summary[:120] + ('...' if len(summary) > 120 else '')

            # Color coding based on status
            if status == 'success': status_symbol, color = "🟢", Fore.GREEN
            elif status == 'error': status_symbol, color = "🔴", Fore.RED
            elif status == 'warning': status_symbol, color = "🟡", Fore.YELLOW
            elif status == 'pending': status_symbol, color = "⚪", Fore.WHITE # Should not be final, but possible if crashed
            elif status == 'running': status_symbol, color = "🔵", Fore.CYAN # Should not be final
            elif status == 'skipped': status_symbol, color = "⚪", Fore.WHITE
            else: status_symbol, color = "❓", Fore.MAGENTA # Unknown status

            table_data.append([node_name, f"{color}{status_symbol} {status.upper()}{Style.RESET_ALL}", display_summary])

        try:
            # Use tabulate for a nice grid format
            table = tabulate(table_data, headers=headers, tablefmt="grid", maxcolwidths=[None, 15, 80])
        except NameError:
            logger.warning("Tabulate library not found. Using basic table format for results.")
            table = self._basic_table(table_data, headers) # Fallback to basic formatting
        except Exception as tab_err:
             logger.error(f"Error generating results table with tabulate: {tab_err}")
             table = self._basic_table(table_data, headers) # Fallback on tabulate error

        print(table)
        print("-----------------------------------------------------------------------\n")






