import json
from jsonschema import validate, ValidationError


class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register_tool(self, tool_name, schema, function):
        """
        Registers a tool with schema + implementation
        """
        self.tools[tool_name] = {
            "schema": schema,
            "function": function
        }

    def list_tools(self):
        """
        Returns all available tools
        """
        return list(self.tools.keys())

    def validate_inputs(self, tool_name, parameters):
        """
        Validates tool input parameters
        before execution
        """

        # check if tool exists
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' is not registered.")

        schema = self.tools[tool_name]["schema"]

        try:
            validate(
                instance=parameters,
                schema=schema["parameters"]
            )

            print(f"Validation passed for {tool_name}")
            return True

        except ValidationError as e:
            raise ValueError(
                f"Validation failed for {tool_name}: {e.message}"
            )

    def execute_tool(self, tool_name, parameters):
        """
        Validates first, then executes tool
        """

        # Step 1 validate
        self.validate_inputs(tool_name, parameters)

        # Step 2 execute
        tool_function = self.tools[tool_name]["function"]

        result = tool_function(parameters)

        return result