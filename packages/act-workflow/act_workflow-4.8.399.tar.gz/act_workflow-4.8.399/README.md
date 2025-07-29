I. Control Flow Nodes (Controlling the execution path)

If: (As implemented) Conditionally executes different paths based on a boolean comparison.

Switch: Multi-way branching based on the value of an input (like a case statement). Takes an input value and routes to different outputs based on matching cases, plus a default path.

ForEach (Item): Iterates over a list input, executing a sub-path for each item in the list. Outputs the results from each iteration.

ForEach (Index): Similar to ForEach (Item), but also provides the current index to the sub-path.

While Loop: Executes a sub-path repeatedly while a specified condition (checked at the start) remains true. Requires careful design to avoid infinite loops.

Do While Loop: Executes a sub-path once, and then repeatedly while a specified condition (checked at the end) remains true.

Merge: Waits for one of multiple incoming paths to complete and then continues the flow. Useful after an If/Switch.

Join (Wait All): Waits for all of multiple incoming paths (e.g., from a parallel execution) to complete before continuing. Often outputs combined results.

Fork (Parallel): Executes multiple downstream paths concurrently. Often paired with a Join node later.

Delay: Pauses the workflow execution for a specified duration (e.g., seconds, milliseconds).

Terminate Workflow: Explicitly stops the workflow execution, optionally setting a final status (success/failure) and message/output.

Sub-Workflow / Call Workflow: Executes another defined Actfile workflow, potentially passing inputs and receiving outputs.

Try/Catch: Defines a block of nodes to execute. If an error occurs within the 'try' path, execution jumps to a 'catch' path, providing error details. A 'finally' path could also be added.

Rate Limit: Limits the execution frequency of a downstream path (e.g., max 5 times per second).

II. Data Manipulation Nodes (Transforming and managing data)

Set Variable: (As implemented) Explicitly stores a value (static or from input/placeholders) under a specific key name in its result, making it easily accessible later.

Get Variable: (Could be implicit via placeholders, but explicit might be useful) Retrieves a value previously stored by a Set Variable node or from the initial input. Often redundant if placeholder resolution is robust.

Delete Variable: Removes a variable from the context (less common, might complicate state).

Transform (JSONata): Transforms input data (usually JSON/dict) using the powerful JSONata query and transformation language.

Template: Renders a string using a templating engine (like Jinja2) and input data, useful for creating dynamic messages, code snippets, or configurations.

Merge Dictionaries: Combines two or more input dictionaries into one. Needs options for handling duplicate keys (overwrite, error, ignore).

Merge Lists: Concatenates two or more input lists into one.

Append To List: Adds one or more items to an existing list.

Get List Item: Retrieves an item from a list by its index (e.g., 0, -1).

Get List Slice: Extracts a sub-section of a list based on start/end indices.

List Length: Returns the number of items in a list.

Split String: Splits a string into a list based on a delimiter.

Join List: Joins items of a list into a single string using a specified separator.

Select Path (JSONPath): Extracts specific data from a JSON object/dict using a JSONPath expression.

Parse JSON: Converts a JSON string input into a structured object/dictionary or list.

Stringify JSON: Converts a structured object/dictionary or list into a JSON string representation.

Format Date/Time: Formats a date/time input (e.g., ISO string, timestamp) into a specified string format.

Format Number: Formats a number input (e.g., adding commas, setting decimal places).

Convert Type: Explicitly converts a value from one basic type to another (e.g., string to integer, integer to boolean). Needs error handling for invalid conversions.

Regex Extract: Extracts parts of a string that match a regular expression pattern (using capture groups).

Regex Match: Checks if an input string fully matches a regular expression pattern (returns boolean).

Create Dictionary: Creates a new dictionary object from specified key-value pairs.

Get Dictionary Value: Retrieves the value associated with a specific key in a dictionary. Handles missing keys gracefully (e.g., return null or default).

Set Dictionary Value: Adds or updates a key-value pair within an existing dictionary.

III. Utility Nodes (General purpose helpers)

Log Message: (As implemented) Logs a message to the system logs at a specified level.

Comment / No-Op: Does nothing functionally but allows adding documentation or breakpoints directly within the workflow graph.

Generate Error: Intentionally throws an error with a specified message. Useful for testing error handling paths (Try/Catch).

Timestamp: Outputs the current date/time in a specified format (e.g., ISO 8601, Unix timestamp).

Basic Math: Performs simple arithmetic operations (+, -, *, /, %, power) on numeric inputs.

String Operation: Performs common string manipulations (upper, lower, trim, length, substring, replace).

Random Number: Generates a random number within a specified range.

Random String: Generates a random string of a specified length and character set.

Generate UUID: Generates a universally unique identifier (UUID).

Hash Data: Computes a hash (e.g., MD5, SHA-256) of an input string or data.

Validate Schema: Validates input data against a provided JSON Schema definition. Returns boolean or throws error on failure.

Get Data Type: Returns the data type of an input value as a string (e.g., "string", "number", "list", "object", "boolean", "null").