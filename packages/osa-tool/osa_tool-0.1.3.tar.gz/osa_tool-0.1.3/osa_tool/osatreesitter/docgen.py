import re
import black
from pathlib import Path

import dotenv
import tiktoken

from osa_tool.config.settings import ConfigLoader
from osa_tool.models.models import ModelHandler, ModelHandlerFactory
from osa_tool.utils import logger

dotenv.load_dotenv()


class DocGen(object):
    """
    This class is a utility for generating Python docstrings using OpenAI's GPT model. It includes methods
    for generating docstrings for a class, a single method, formatting the structure of Python files,
    counting the number of tokens in a given prompt, extracting the docstring from GPT's response,
    inserting a generated docstring into the source code and also processing a Python file by generating
    and inserting missing docstrings.

    Methods:
        __init__(self)
            Initializes the class instance by setting the 'api_key' attribute to the value of the
            'OPENAI_API_KEY' environment variable.

        format_structure_openai(structure)
            Formats the structure of Python files in a readable string format by iterating over the given
            'structure' dictionary and generating a formatted string.

        count_tokens(prompt, model)
            Counts the number of tokens in a given prompt using a specified model.

        generate_class_documentation(class_details, model)
            Generates documentation for a class using OpenAI GPT.

        generate_method_documentation()
            Generates documentation for a single method using OpenAI GPT.

        extract_pure_docstring(gpt_response)
            Extracts only the docstring from the GPT-4 response while keeping triple quotes.

        insert_docstring_in_code(source_code, method_details, generated_docstring)
            Inserts a generated docstring into the specified location in the source code.

        insert_cls_docstring_in_code(source_code, class_details, generated_docstring)
            Inserts a generated class docstring into the class definition and returns the updated source code.

        process_python_file(parsed_structure, file_path)
            Processes a Python file by generating and inserting missing docstrings and updates the source file
            with the new docstrings.

        generate_documentation_openai(file_structure, model)
            Generates the documentation for a given file structure using OpenAI's API by traversing the given
            file structure and for each class or standalone function, generating its documentation.
    """

    def __init__(self, config_loader: ConfigLoader):
        """
        Instantiates the object of the class.

        This method is a constructor that initializes the object by setting the 'api_key' attribute to the value of the 'OPENAI_API_KEY' environment variable.
        """
        self.config = config_loader.config
        self.model_handler: ModelHandler = ModelHandlerFactory.build(self.config)

    @staticmethod
    def format_structure_openai(structure: dict) -> str:
        """
        Formats the structure of Python files in a readable string format.

        This method iterates over the given dictionary 'structure' and generates a formatted string where it describes
        each file, its classes and functions along with their details such as line number, arguments, return type,
        source code and docstrings if available.

        Args:
            structure: A dictionary containing details of the Python files structure. The dictionary should
            have filenames as keys and values as lists of dictionaries. Each dictionary in the list represents a
            class or function and should contain keys like 'type', 'name', 'start_line', 'docstring', 'methods'
            (for classes), 'details' (for functions) etc. Each 'methods' or 'details' is also a dictionary that
            includes detailed information about the method or function.

        Returns:
            A formatted string representing the structure of the Python files.
        """
        formatted_structure = "The following is the structure of the Python files:\n\n"

        for filename, structures in structure.items():
            formatted_structure += f"File: {filename}\n"
            for item in structures:
                if item["type"] == "class":
                    formatted_structure += DocGen._format_class(item)
                elif item["type"] == "function":
                    formatted_structure += DocGen._format_function(item)

        return formatted_structure

    @staticmethod
    def _format_class(item: dict) -> str:
        """Formats class details."""
        class_str = f"  - Class: {item['name']}, line {item['start_line']}\n"
        if item["docstring"]:
            class_str += f"      Docstring: {item['docstring']}\n"
        for method in item["methods"]:
            class_str += DocGen._format_method(method)
        return class_str

    @staticmethod
    def _format_method(method: dict) -> str:
        """Formats method details."""
        method_str = f"      - Method: {method['method_name']}, Args: {method['arguments']}, Return: {method['return_type']}, line {method['start_line']}\n"
        if method["docstring"]:
            method_str += f"          Docstring:\n        {method['docstring']}\n"
        method_str += f"        Source:\n{method['source_code']}\n"
        return method_str

    @staticmethod
    def _format_function(item: dict) -> str:
        """Formats function details."""
        details = item["details"]
        function_str = f"  - Function: {details['method_name']}, Args: {details['arguments']}, Return: {details['return_type']}, line {details['start_line']}\n"
        if details["docstring"]:
            function_str += f"          Docstring:\n    {details['docstring']}\n"
        function_str += f"        Source:\n{details['source_code']}\n"
        return function_str

    def count_tokens(self, prompt: str) -> int:
        """
        Counts the number of tokens in a given prompt using a specified model.

        Args:
            prompt: The text for which to count the tokens.

        Returns:
            The number of tokens in the prompt.
        """
        enc = tiktoken.encoding_for_model(self.config.llm.model)
        tokens = enc.encode(prompt)
        return len(tokens)

    def generate_class_documentation(self, class_details: dict) -> str:
        """
        Generate documentation for a class.

        Args:
            class_details: A list of dictionaries containing method names and their docstrings.

        Returns:
            The generated class docstring.
        """
        # Construct a structured prompt
        prompt = f"""
        Generate a single Python docstring for the following class {class_details[0]}. The docstring should follow Google-style format and include:
        - A short summary of what the class does.
        - A list of its methods without details if class has them otherwise do not mention a list of methods.
        - A list of its attributes without types if class has them otherwise do not mention a list of attributes.
        - A brief summary of what its methods and attributes do if one has them for.
        """
        if len(class_details[1]) > 0:
            prompt += f"\nClass Attributes:\n"
            for attr in class_details[1]:
                prompt += f"- {attr}\n"

        if len(class_details[2:]) > 0:
            prompt += f"\nClass Methods:\n"
            for method in class_details[2:]:
                prompt += f"- {method['method_name']}: {method['docstring']}\n"

        return self.model_handler.send_request(prompt)

    def generate_method_documentation(
        self, method_details: dict, context_code: str = None
    ) -> str:
        """
        Generate documentation for a single method.
        """
        prompt = f"""
        Generate a Python docstring for the following method. The docstring should follow Google-style format and include:
        - A short summary of what the method does.
        - A description of its parameters without types.
        - The return type and description.
        {"- Use provided source code of imported methods, functions to describe their usage." if context_code else ""}

        Method Details:
        - Method Name: {method_details["method_name"]}
        - Method decorators: {method_details["decorators"]}
        - Source Code:
        ```
        {method_details["source_code"]}
        ```
        {"- Imported methods source code:" if context_code else ""}
        {context_code if context_code else ""}
        """
        return self.model_handler.send_request(prompt)

    def extract_pure_docstring(self, gpt_response: str) -> str:
        """
        Extracts only the docstring from the GPT-4 response while keeping triple quotes.

        Args:
            gpt_response: The full response from GPT-4.

        Returns:
            The properly formatted docstring including triple quotes.
        """
        # Regex to capture the full docstring with triple quotes
        match = re.search(r'("""+)\n?(.*?)\n?\1', gpt_response, re.DOTALL)

        if match:
            triple_quotes = match.group(1)  # Keep the triple quotes (""" or """)
            extracted_docstring = match.group(
                2
            )  # Extract only the content inside the docstring
            cleaned_content = re.sub(
                r"^\s*def\s+\w+\(.*?\):\s*", "", extracted_docstring, flags=re.MULTILINE
            )

            return f"{triple_quotes}\n{cleaned_content}{triple_quotes}"

        return '"""No valid docstring found."""'  # Return a placeholder if no docstring was found

    def insert_docstring_in_code(
        self, source_code: str, method_details: dict, generated_docstring: str
    ) -> str:
        """
        This method inserts a generated docstring into the specified location in the source code.

        Args:
            source_code: The source code where the docstring should be inserted.
            method_details: A dictionary containing details about the method.
                It should have a key 'method_name' with the name of the method where the docstring should be inserted.
            generated_docstring: The docstring that should be inserted into the source code.

        Returns:
            None
        """
        # Matches a method definition with the given name,
        # including an optional return type. Ensures no docstring follows.
        method_pattern = rf"((?:@\w+(?:\([^)]*\))?\s*\n)*\s*(?:async\s+)?def\s+{method_details['method_name']}\s*\((?:[^)(]|\((?:[^)(]*|\([^)(]*\))*\))*\)\s*(->\s*[a-zA-Z0-9_\[\],. |]+)?\s*:\n)(\s*)(?!\s*\"\"\")"
        """
        (
            (?:@\w+(?:\([^)]*\))?\s*\n)*                # Optional decorators: e.g. @decorator or @decorator(args), each followed by newline
            \s*                                         # Optional whitespace before function definition
            (?:async\s+)?                               # Optional 'async' keyword followed by whitespace
            def\s+{method_details['method_name']}\s*    # 'def' keyword followed by the specific method name and optional spaces
            \(                                          # Opening parenthesis for the parameter list
                (?:                                     # Non-capturing group to match parameters inside parentheses
                    [^)(]                               # Match any character except parentheses (simple parameter)
                    |                                   # OR
                    \(                                  # Opening a nested parenthesis
                        (?:[^)(]*|\([^)(]*\))*          # Recursively match nested parentheses content
                    \)                                  # Closing the nested parenthesis
                )*                                      # Repeat zero or more times (all parameters)
            \)                                          # Closing parenthesis of the parameter list
            \s*                                         # Optional whitespace after parameters
            (->\s*[a-zA-Z0-9_\[\],. |]+)?               # Optional return type annotation (e.g. -> int, -> dict[str, Any])
            \s*:\n                                      # Colon ending the function header followed by newline
        )
        (\s*)                                          # Capture indentation (spaces/tabs) of the next line (function body)
        (?!\s*\"\"\")                                  # Negative lookahead: ensure the next non-space characters are NOT triple quotes (no docstring yet)
        """

        docstring_with_format = self.extract_pure_docstring(generated_docstring)
        updated_code = re.sub(
            method_pattern, rf"\1\3{docstring_with_format}\n\3", source_code, count=1
        )

        return updated_code

    def insert_cls_docstring_in_code(
        self, source_code: str, class_name: str, generated_docstring: str
    ) -> str:
        """
        Inserts a generated class docstring into the class definition.

        Args:

            source_code: The source code where the docstring should be inserted.
            class_name: Class name.
            generated_docstring: The docstring that should be inserted.

        Returns:
            The updated source code with the class docstring inserted.
        """

        # Matches a class definition with the given name,
        # including optional parentheses. Ensures no docstring follows.
        class_pattern = (
            rf"(class\s+{class_name}\s*(\([^)]*\))?\s*:\n)(\s*)(?!\s*\"\"\")"
        )

        # Ensure we keep only the extracted docstring
        docstring_with_format = self.extract_pure_docstring(generated_docstring)

        updated_code = re.sub(
            class_pattern, rf"\1\3{docstring_with_format}\n\3", source_code, count=1
        )

        return updated_code

    def context_extractor(self, method_details: dict, structure: dict) -> str:
        """
            Extracts the context of method calls and functions from given method_details and code structure.

            Parameters:
            - method_details: A dictionary containing details about the method calls.
            - structure: A dictionary representing the code structure.

            Returns:
            A string containing the context of the method calls and functions in the format:
            - If a method call is found:
              "# Method {method_name} in class {class_name}
        {source_code}"
            - If a function call is found:
              "# Function {class_name}
        {source_code}"

            Note:
            - This method iterates over the method calls in method_details and searches for the corresponding methods and functions
              in the code structure. It constructs the context of the found methods and functions by appending their source code
              along with indicator comments.
            - The returned string contains the structured context of all the detected methods and functions.
        """

        def is_target_class(item, call):
            return item["type"] == "class" and item["name"] == call["class"]

        def is_target_method(method, call):
            return method["method_name"] == call["function"]

        def is_constructor(method, call):
            return method["method_name"] == "__init__" and call["function"] is None

        def is_target_function(item, call):
            return (
                item["type"] == "function"
                and item["details"]["method_name"] == call["class"]
            )

        context = []

        for call in method_details.get("method_calls", []):
            file_data = structure.get(call["path"], {})
            if not file_data:
                continue

            for item in file_data.get("structure", []):
                if is_target_class(item, call):
                    for method in item.get("methods", []):
                        if is_target_method(method, call) or is_constructor(
                            method, call
                        ):
                            method_name = (
                                call["function"] if call["function"] else "__init__"
                            )
                            context.append(
                                f"# Method {method_name} in class {call['class']}\n"
                                + method.get("source_code", "")
                            )
                elif is_target_function(item, call):
                    context.append(
                        f"# Function {call['class']}\n"
                        + item["details"].get("source_code", "")
                    )

        return "\n".join(context)

    def format_with_black(self, filename):
        """
        Formats a Python source code file using the `black` code formatter.

        This method takes a filename as input and formats the code in the specified file using the `black` code formatter.

        Parameters:
            - filename: The path to the Python source code file to be formatted.

        Returns:
            None
        """
        black.format_file_in_place(
            Path(filename),
            fast=True,
            mode=black.FileMode(),
            write_back=black.WriteBack.YES,
        )

    def process_python_file(self, parsed_structure: dict) -> None:
        """
        Processes a Python file by generating and inserting missing docstrings.

        This method iterates over the given parsed structure of a Python codebase, checks each class method for missing
        docstrings, and generates and inserts them if missing. The method updates the source file with the new docstrings
        and logs the path of the updated file.

        Args:
            parsed_structure: A dictionary representing the parsed structure of the Python codebase.
                The dictionary keys are filenames and the values are lists of dictionaries representing
                classes and their methods.

        Returns:
            None
        """
        for filename, structure in parsed_structure.items():
            self.format_with_black(filename)
            with open(filename, "r", encoding="utf-8") as f:
                source_code = f.read()
            for item in structure["structure"]:
                if item["type"] == "class":
                    for method in item["methods"]:
                        if method["docstring"] == None:  # If docstring is missing
                            logger.info(
                                f"Generating docstring for method: {method['method_name']} in class {item['name']} at {filename}"
                            )
                            method_context = self.context_extractor(
                                method, parsed_structure
                            )
                            generated_docstring = self.generate_method_documentation(
                                method, method_context
                            )
                            if item["docstring"] == None:
                                method["docstring"] = self.extract_pure_docstring(
                                    generated_docstring
                                )
                            source_code = self.insert_docstring_in_code(
                                source_code, method, generated_docstring
                            )
                if item["type"] == "function":
                    func_details = item["details"]
                    if func_details["docstring"] == None:
                        logger.info(
                            f"Generating docstring for a function: {func_details['method_name']} at {filename}"
                        )
                        generated_docstring = self.generate_method_documentation(
                            func_details
                        )
                        source_code = self.insert_docstring_in_code(
                            source_code, func_details, generated_docstring
                        )

            for item in structure["structure"]:
                if item["type"] == "class" and item["docstring"] == None:
                    class_name = item["name"]
                    cls_structure = []
                    cls_structure.append(class_name)
                    cls_structure.append(item["attributes"])
                    for method in item["methods"]:
                        cls_structure.append(
                            {
                                "method_name": method["method_name"],
                                "docstring": method["docstring"],
                            }
                        )
                    logger.info(
                        f"Generating docstring for class: {item['name']} in class at {filename}"
                    )
                    generated_cls_docstring = self.generate_class_documentation(
                        cls_structure
                    )
                    source_code = self.insert_cls_docstring_in_code(
                        source_code, class_name, generated_cls_docstring
                    )
            with open(filename, "w", encoding="utf-8") as f:
                f.write(source_code)
            self.format_with_black(filename)
            logger.info(f"Updated file: {filename}")

    def generate_method_documentation_md(self, method_details: dict) -> str:
        """
        Generate documentation for a single method using OpenAI GPT.
        """
        prompt = f"""
        Generate detailed documentation for the following Python method. Include:
        - Method name.
        - Arguments and their purposes.
        - Return type and its purpose.
        - A high-level explanation of what the method does.
        - Include the provided source code in the documentation.

        Method Details:
        - Method Name: {method_details["method_name"]}
        - Arguments: {method_details["arguments"]}
        - Return Type: {method_details["return_type"]}
        - Docstring: {method_details["docstring"]}
        - Source Code:
        ```
        {method_details["source_code"]}
        ```
        """

        return self.model_handler.send_request(prompt)

    def generate_documentation_openai(self, file_structure: dict) -> str:
        """
        Generates the documentation for a given file structure using OpenAI's API.

        This method traverses the given file structure and for each class or standalone function, it generates
        its documentation. If the documentation is not available, it attempts to generate it using the OpenAI's API.
        The generated documentation is returned as a string.

        Args:
            self: The instance of the class where this method is defined.
            file_structure: A dictionary where keys are filenames and values are lists of dictionaries.
                Each dictionary represents a class or a standalone function in the file and contains information
                like its name, type (class or function), docstring, and methods (in case of a class).

        Returns:
            The final documentation as a string.
        """
        final_documentation = ""

        for filename, structure in file_structure.items():
            final_documentation += self._format_file_header(filename)

            for item in structure:
                if item["type"] == "class":
                    final_documentation += self._format_class_doc(item)
                elif item["type"] == "function":
                    final_documentation += self._format_function_doc(item)

        return final_documentation

    def _format_file_header(self, filename: str) -> str:
        """Formats the header for a file in documentation."""
        return f"# Documentation for {filename}\n\n"

    def _format_class_doc(self, item: dict) -> str:
        """Formats documentation for a class."""
        class_doc = f"## Class: {item['name']}\n\n{item['docstring'] or 'No docstring provided'}\n\n"
        for method in item["methods"]:
            class_doc += self._generate_method_doc(method)
        return class_doc

    def _format_function_doc(self, item: dict) -> str:
        """Formats documentation for a standalone function."""
        function_details = item["details"]
        return self._generate_method_doc(function_details, is_function=True)

    def _generate_method_doc(self, method_details: dict, is_function=False) -> str:
        """Generates documentation for a method or function."""
        doc_type = "Function" if is_function else "Method"
        try:
            logger.info(
                f"{doc_type} {method_details['method_name']}'s docstring is generating"
            )
            method_doc = self.generate_method_documentation_md(
                method_details=method_details
            )
            return (
                f"### {doc_type}: {method_details['method_name']}\n\n{method_doc}\n\n"
            )
        except Exception as e:
            logger.error(e, exc_info=True)
            return f"### {doc_type}: {method_details['method_name']}\n\nFailed to generate documentation.\n\n"
