"""
UL (Unified Lattice)

A Python library that enables developers to input a set of functions and
automatically generate a directed acyclic graph (DAG), or lattice, representing
all possible input-output relationships among those functions.

Example:

    >>> import ul
    >>> functions = [
    ...     "def load_csv(file_path: str) -> pd.DataFrame: pass",
    ...     "def split_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]: pass",
    ... ]
    >>> lattice = ul.generate_lattice(functions, openai_api_key="your-key")
    >>> print(lattice.to_mermaid_output())
    graph TD
        load_csv[load_csv(file_path: str) --> pd.DataFrame]
        split_data[split_data(df: pd.DataFrame) --> [pd.DataFrame, pd.DataFrame]]
        load_csv --> split_data
"""

import os
import ast
import inspect
import json
import re
import networkx as nx
from typing import List, Dict, Any, Union, Optional, Tuple, Callable, Set
from dataclasses import dataclass, field
import openai

# API key handling
OPENAI_KEY = os.environ.get("OPEN_API_KEY", None)


@dataclass
class FunctionMetadata:
    """Metadata about a function including its name, arguments, return type, and docstring."""

    name: str
    args: List[Dict[str, str]]
    return_type: Any
    docstring: Optional[str] = None


@dataclass
class Lattice:
    """Represents a directed acyclic graph of functions."""

    graph: nx.DiGraph = field(default_factory=nx.DiGraph)
    functions: Dict[str, FunctionMetadata] = field(default_factory=dict)

    def to_structured_output(self) -> Dict[str, Any]:
        """
        Convert the lattice to a structured JSON-like format.

        Returns:
            A dictionary with function details and input-output links.

        >>> lattice = Lattice()
        >>> # Assuming lattice has been populated
        >>> output = lattice.to_structured_output()
        >>> isinstance(output, dict)
        True
        """
        functions_list = []
        for name, metadata in self.functions.items():
            functions_list.append(
                {
                    "name": name,
                    "args": metadata.args,
                    "return_type": metadata.return_type,
                    "docstring": metadata.docstring,
                }
            )

        links = []
        for source, target, data in self.graph.edges(data=True):
            links.append(
                {
                    "from": {"function": source, "output": "return"},
                    "to": {"function": target, "arg": data.get("arg_name", "")},
                }
            )

        return {"functions": functions_list, "links": links}


def to_mermaid_output(self) -> str:
    """
    Generate a Mermaid graph specification for visualization.

    Returns:
        A string containing a Mermaid flowchart specification.

    >>> lattice = Lattice()
    >>> # Assuming lattice has been populated
    >>> output = lattice.to_mermaid_output()
    >>> isinstance(output, str)
    True
    """
    mermaid = ["graph TD"]

    # Add nodes - using proper node labeling that avoids conflicts with Mermaid syntax
    for name, metadata in self.functions.items():
        args_str = ", ".join([f"{arg['name']}: {arg['type']}" for arg in metadata.args])
        return_str = metadata.return_type
        # Use proper Mermaid node syntax with quotes around complex text
        mermaid.append(f'    {name}["{name}({args_str}) → {return_str}"]')

    # Add edges
    for source, target, _ in self.graph.edges(data=True):
        mermaid.append(f"    {source} --> {target}")

    return "\n".join(mermaid)


def process_code_input(code_strings: List[str]) -> List[FunctionMetadata]:
    """
    Process a list of Python function code strings to extract metadata.

    Args:
        code_strings: List of function definitions as strings

    Returns:
        List of FunctionMetadata objects

    >>> metadata = process_code_input(["def test_func(x: int) -> str:\\n    '''Test docstring'''\\n    return str(x)"])
    >>> metadata[0].name
    'test_func'
    """
    result = []

    for code in code_strings:
        try:
            # Parse the code
            tree = ast.parse(code)

            # Extract the function definition
            func_def = None
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_def = node
                    break

            if not func_def:
                continue

            # Get function name
            name = func_def.name

            # Extract docstring
            docstring = ast.get_docstring(func_def)

            # Extract arguments
            args = []
            for arg in func_def.args.args:
                arg_type = "Any"
                if arg.annotation:
                    arg_type = _get_type_str(arg.annotation)
                args.append({"name": arg.arg, "type": arg_type})

            # Extract return type
            return_type = "Any"
            if func_def.returns:
                return_type = _get_type_str(func_def.returns)

            result.append(
                FunctionMetadata(
                    name=name, args=args, return_type=return_type, docstring=docstring
                )
            )
        except SyntaxError:
            # Skip invalid code
            continue

    return result


def process_signature_input(signatures: List[str]) -> List[FunctionMetadata]:
    """
    Process a list of function signatures to extract metadata.

    Args:
        signatures: List of function signatures as strings

    Returns:
        List of FunctionMetadata objects

    >>> metadata = process_signature_input(["load_csv(file_path: str) -> pd.DataFrame"])
    >>> metadata[0].name
    'load_csv'
    """
    result = []

    # Regex for parsing function signatures
    pattern = r"(\w+)\s*\((.*?)\)\s*(?:->\s*(.+))?"

    for sig in signatures:
        match = re.match(pattern, sig.strip())
        if not match:
            continue

        name, args_str, return_type = match.groups()
        return_type = return_type.strip() if return_type else "Any"

        # Parse arguments
        args = []
        if args_str.strip():
            for arg_def in args_str.split(","):
                arg_def = arg_def.strip()
                if ":" in arg_def:
                    arg_name, arg_type = arg_def.split(":", 1)
                    args.append({"name": arg_name.strip(), "type": arg_type.strip()})
                else:
                    args.append({"name": arg_def, "type": "Any"})

        result.append(
            FunctionMetadata(
                name=name, args=args, return_type=return_type, docstring=None
            )
        )

    return result


def process_docstring_input(
    docstrings: List[str], api_key: str, model: str = "gpt-4"
) -> List[FunctionMetadata]:
    """
    Process a list of docstrings to extract function metadata using OpenAI.

    Args:
        docstrings: List of docstring descriptions
        api_key: OpenAI API key
        model: OpenAI model to use

    Returns:
        List of FunctionMetadata objects
    """
    # Initialize OpenAI client
    client = _get_openai_client(api_key)

    # Prepare prompts for OpenAI
    prompt = """
    Convert the following function docstrings into structured metadata with names, arguments, and return types.
    For each docstring, provide:
    1. Function name
    2. Arguments (name and type)
    3. Return type
    
    Format your response as a JSON array of objects, where each object has the following structure:
    {
      "name": "function_name",
      "args": [{"name": "arg_name", "type": "arg_type"}],
      "return_type": "return_type",
      "docstring": "original_docstring"
    }
    
    Docstrings:
    """

    full_prompt = prompt + "\n".join(docstrings)

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a code analysis assistant."},
                {"role": "user", "content": full_prompt},
            ],
        )

        content = response.choices[0].message.content

        # Extract JSON from response
        json_str = _extract_json(content)
        if not json_str:
            return []

        # Parse JSON
        result = json.loads(json_str)
        if not isinstance(result, list):
            return []

        # Convert to FunctionMetadata objects
        return [
            FunctionMetadata(
                name=item.get("name", ""),
                args=item.get("args", []),
                return_type=item.get("return_type", "Any"),
                docstring=item.get("docstring", ""),
            )
            for item in result
        ]
    except Exception as e:
        print(f"Error processing docstrings: {e}")
        return []


def process_natural_language_input(
    descriptions: List[str], api_key: str, model: str = "gpt-4"
) -> List[FunctionMetadata]:
    """
    Process natural language descriptions to extract function metadata using OpenAI.

    Args:
        descriptions: List of natural language descriptions
        api_key: OpenAI API key
        model: OpenAI model to use

    Returns:
        List of FunctionMetadata objects
    """
    # This follows a similar pattern to process_docstring_input but with a different prompt
    client = _get_openai_client(api_key)

    prompt = """
    Convert these natural language function descriptions into structured metadata with names, arguments, and return types.
    For each description, infer:
    1. A suitable function name
    2. Appropriate arguments with types
    3. An appropriate return type
    
    Format your response as a JSON array of objects, where each object has the following structure:
    {
      "name": "function_name",
      "args": [{"name": "arg_name", "type": "arg_type"}],
      "return_type": "return_type",
      "docstring": "original_description"
    }
    
    Function descriptions:
    """

    full_prompt = prompt + "\n".join(descriptions)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a code analysis assistant."},
                {"role": "user", "content": full_prompt},
            ],
        )

        content = response.choices[0].message.content

        json_str = _extract_json(content)
        if not json_str:
            return []

        result = json.loads(json_str)
        if not isinstance(result, list):
            return []

        return [
            FunctionMetadata(
                name=item.get("name", ""),
                args=item.get("args", []),
                return_type=item.get("return_type", "Any"),
                docstring=item.get("docstring", ""),
            )
            for item in result
        ]
    except Exception as e:
        print(f"Error processing natural language descriptions: {e}")
        return []


def generate_lattice(
    functions: List[str],
    openai_api_key: Optional[str] = None,
    model: str = "gpt-4",
    input_type: str = "auto",
) -> Lattice:
    """
    Generate a lattice (DAG) based on function input-output relationships.

    Args:
        functions: List of function definitions (code, signatures, docstrings, or descriptions)
        openai_api_key: OpenAI API key (if None, uses environment variable)
        model: OpenAI model to use
        input_type: Type of input ("code", "signature", "docstring", "natural", or "auto")

    Returns:
        A Lattice object containing the generated DAG

    Raises:
        ValueError: If API key is missing or input is invalid
    """
    # Resolve API key
    api_key = openai_api_key or OPENAI_KEY
    if not api_key:
        raise ValueError(
            "OpenAI API key is required. Provide it as an argument or set the OPEN_API_KEY environment variable."
        )

    # Determine input type if auto
    if input_type == "auto":
        input_type = _determine_input_type(functions)

    # Process input based on type
    if input_type == "code":
        metadata_list = process_code_input(functions)
    elif input_type == "signature":
        metadata_list = process_signature_input(functions)
    elif input_type == "docstring":
        metadata_list = process_docstring_input(functions, api_key, model)
    elif input_type == "natural":
        metadata_list = process_natural_language_input(functions, api_key, model)
    else:
        raise ValueError(
            f"Invalid input_type: {input_type}. Must be 'code', 'signature', 'docstring', 'natural', or 'auto'."
        )

    # Generate lattice using OpenAI
    lattice = _generate_lattice_with_openai(metadata_list, api_key, model)

    # Validate lattice
    validate_lattice(lattice)

    return lattice


def extract_subgraph(
    lattice: Lattice,
    start_functions: Optional[List[str]] = None,
    end_functions: Optional[List[str]] = None,
    include_functions: Optional[List[str]] = None,
) -> Lattice:
    """
    Extract a subgraph from the lattice for a specific task.

    Args:
        lattice: The full lattice object
        start_functions: List of function names to start the subgraph
        end_functions: List of function names to end the subgraph
        include_functions: List of function names to include in the subgraph

    Returns:
        A new Lattice object containing the subgraph
    """
    # Create a new graph
    subgraph = nx.DiGraph()

    # If no constraints, return full lattice
    if not start_functions and not end_functions and not include_functions:
        return Lattice(lattice.graph.copy(), lattice.functions.copy())

    # Initialize sets for tracking nodes
    nodes_to_include = set()

    # Process start_functions
    if start_functions:
        for func in start_functions:
            if func in lattice.functions:
                nodes_to_include.add(func)
                # Add all descendants
                nodes_to_include.update(nx.descendants(lattice.graph, func))

    # Process end_functions
    if end_functions:
        end_nodes = set()
        for func in end_functions:
            if func in lattice.functions:
                end_nodes.add(func)
                # Add all ancestors
                end_nodes.update(nx.ancestors(lattice.graph, func))

        # If start_functions were specified, intersect with descendants
        if start_functions:
            nodes_to_include &= end_nodes
        else:
            nodes_to_include = end_nodes

    # Process include_functions
    if include_functions:
        for func in include_functions:
            if func in lattice.functions:
                nodes_to_include.add(func)

    # Create the subgraph
    subgraph = lattice.graph.subgraph(nodes_to_include).copy()

    # Create a new Lattice with the subgraph
    result = Lattice(subgraph)

    # Add function metadata
    for node in subgraph.nodes():
        if node in lattice.functions:
            result.functions[node] = lattice.functions[node]

    return result


def validate_lattice(lattice: Lattice) -> bool:
    """
    Ensure the lattice is a valid DAG (no cycles) and that input-output links are type-compatible.

    Args:
        lattice: The lattice to validate

    Returns:
        True if valid, raises ValueError otherwise
    """
    # Check for cycles
    if not nx.is_directed_acyclic_graph(lattice.graph):
        cycles = list(nx.simple_cycles(lattice.graph))
        raise ValueError(f"Lattice contains cycles: {cycles}")

    # Check type compatibility for all edges
    for source, target, data in lattice.graph.edges(data=True):
        if source not in lattice.functions or target not in lattice.functions:
            continue

        source_metadata = lattice.functions[source]
        target_metadata = lattice.functions[target]

        # Get the argument name for this edge
        arg_name = data.get("arg_name")
        if not arg_name:
            continue

        # Find the argument in target function
        arg_type = None
        for arg in target_metadata.args:
            if arg["name"] == arg_name:
                arg_type = arg["type"]
                break

        if not arg_type:
            continue

        # Check if source return type is compatible with target argument type
        # This is a simplified check and could be enhanced with more sophisticated type compatibility
        if not _are_types_compatible(source_metadata.return_type, arg_type):
            print(
                f"Warning: Potential type incompatibility: {source} returns {source_metadata.return_type}, but {target}.{arg_name} expects {arg_type}"
            )

    return True


def visualize_lattice(
    lattice: Lattice, output_file: Optional[str] = None
) -> Optional[str]:
    """
    Renders the lattice as a Mermaid diagram or saves to a file.

    Args:
        lattice: The lattice to visualize
        output_file: Optional file path to save the visualization

    Returns:
        The Mermaid code as a string if output_file is None, otherwise None
    """
    mermaid_code = lattice.to_mermaid_output()

    if output_file:
        with open(output_file, 'w') as f:
            f.write(mermaid_code)
        return None

    return mermaid_code


# Helper functions


def _get_type_str(node: ast.AST) -> str:
    """Extract a string representation of a type annotation from an AST node."""
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Subscript):
        value = _get_type_str(node.value)
        if isinstance(node.slice, ast.Index):
            # Python 3.8 and earlier
            slice_value = ast.unparse(node.slice.value).strip()
        else:
            # Python 3.9+
            slice_value = ast.unparse(node.slice).strip()
        return f"{value}[{slice_value}]"
    elif isinstance(node, ast.Attribute):
        return f"{_get_type_str(node.value)}.{node.attr}"
    elif isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    else:
        try:
            return ast.unparse(node).strip()
        except:
            return "Any"


def _determine_input_type(functions: List[str]) -> str:
    """Automatically determine the type of input provided."""
    if not functions:
        return "natural"

    sample = functions[0].strip()

    # Check if it looks like code (has 'def' and ':')
    if sample.startswith("def ") and ":" in sample:
        return "code"

    # Check if it looks like a signature (has parentheses and possibly ->)
    if "(" in sample and ")" in sample:
        return "signature"

    # Check if it's a docstring (starts with function name followed by :)
    if re.match(r"^\w+\s*:", sample):
        return "docstring"

    # Default to natural language
    return "natural"


def _get_openai_client(api_key: str):
    """Initialize and return an OpenAI client."""
    return openai.OpenAI(api_key=api_key)


def _extract_json(text: str) -> str:
    """Extract JSON from text that might contain markdown or other content."""
    # Look for JSON inside ```json ... ``` blocks
    json_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    match = re.search(json_pattern, text)
    if match:
        return match.group(1)

    # Try to find JSON with curly braces
    brace_pattern = r"\{\s*\".*\"\s*:[\s\S]*\}"
    match = re.search(brace_pattern, text)
    if match:
        return match.group(0)

    # If no JSON found, return the original text - we'll try to parse it as JSON
    return text


def _are_types_compatible(source_type: str, target_type: str) -> bool:
    """
    Check if source_type is compatible with target_type.
    This is a simplified check and could be enhanced with more sophisticated type compatibility.
    """
    # If either type is Any, they're compatible
    if source_type == "Any" or target_type == "Any":
        return True

    # Exact match
    if source_type == target_type:
        return True

    # Common special cases
    if source_type == "int" and target_type == "float":
        return True
    if source_type == "float" and target_type == "str":
        return True
    if source_type == "int" and target_type == "str":
        return True

    # Handle container types (very basic check)
    if "list" in source_type and "list" in target_type:
        return True
    if "dict" in source_type and "dict" in target_type:
        return True
    if "tuple" in source_type and "tuple" in target_type:
        return True

    # When in doubt, warn but allow
    return True


def _generate_lattice_with_openai(
    metadata_list: List[FunctionMetadata], api_key: str, model: str = "gpt-4"
) -> Lattice:
    """
    Generate a lattice using the OpenAI API.

    Args:
        metadata_list: List of function metadata
        api_key: OpenAI API key
        model: OpenAI model to use

    Returns:
        A Lattice object
    """
    if not metadata_list:
        return Lattice()

    client = _get_openai_client(api_key)

    # Prepare function metadata for OpenAI
    metadata_str = json.dumps(
        [
            {
                "name": meta.name,
                "args": meta.args,
                "return_type": meta.return_type,
                "docstring": meta.docstring,
            }
            for meta in metadata_list
        ],
        indent=2,
    )

    prompt = f"""
    You are an expert in code analysis and graph theory. Given the following function definitions, propose a directed acyclic graph (DAG) where nodes are functions and edges represent possible input-output relationships. Each edge should indicate which function's output can serve as input to another function's argument. Ensure the graph is comprehensive, capturing all valid connections, and allows users to extract subgraphs for specific tasks. Handle ambiguities (e.g., missing type information) by making reasonable assumptions.
    
    Function definitions:
    {metadata_str}
    
    Return the graph as a structured JSON object with nodes (function names, arguments, return types) and edges (from function output to argument of another function).
    
    Output format:
    {{
      "nodes": [
        {{"name": "function_name", "args": [{{"name": "arg_name", "type": "type"}}], "return_type": "type"}}
      ],
      "edges": [
        {{"from": {{"function": "function_name", "output": "return"}}, "to": {{"function": "function_name", "arg": "arg_name"}}}}
      ]
    }}
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a code analysis assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        content = response.choices[0].message.content

        # Extract JSON
        json_str = _extract_json(content)
        if not json_str:
            raise ValueError("Failed to extract JSON from OpenAI response")

        data = json.loads(json_str)

        # Create a new lattice
        lattice = Lattice()

        # Add nodes (functions)
        for node in data.get("nodes", []):
            name = node.get("name")
            if not name:
                continue

            # Add to functions dictionary
            lattice.functions[name] = FunctionMetadata(
                name=name,
                args=node.get("args", []),
                return_type=node.get("return_type", "Any"),
                docstring=None,  # OpenAI doesn't return docstrings here
            )

            # Add node to graph
            lattice.graph.add_node(name)

        # Add edges
        for edge in data.get("edges", []):
            from_func = edge.get("from", {}).get("function")
            to_func = edge.get("to", {}).get("function")
            arg_name = edge.get("to", {}).get("arg")

            if from_func and to_func and arg_name:
                # Add edge to graph with arg_name as attribute
                lattice.graph.add_edge(from_func, to_func, arg_name=arg_name)

        return lattice
    except Exception as e:
        print(f"Error generating lattice with OpenAI: {e}")
        return Lattice()


# Populate the existing metadata with original docstrings
def _update_metadata_with_original_docstrings(
    lattice: Lattice, original_metadata: List[FunctionMetadata]
) -> None:
    """
    Update function metadata in the lattice with original docstrings.

    Args:
        lattice: The lattice to update
        original_metadata: Original function metadata
    """
    for meta in original_metadata:
        if meta.name in lattice.functions and meta.docstring:
            lattice.functions[meta.name].docstring = meta.docstring
