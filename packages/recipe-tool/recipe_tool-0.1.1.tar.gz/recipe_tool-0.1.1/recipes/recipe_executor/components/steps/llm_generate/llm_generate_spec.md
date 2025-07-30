# LLMGenerateStep Component Specification

## Purpose

The LLMGenerateStep component enables recipes to generate content using large language models (LLMs). It serves as the bridge between recipes and the LLM subsystem, handling prompt templating, model selection, MCP server tools, structured output, and storing generation results in the execution context.

## Core Requirements

- Process prompt templates using context data
- Support configurable model selection
- Support MCP server configuration for tool access
- Support multiple output formats (text, files, object, list)
- Call LLMs to generate content
- Store generated results in the context with dynamic key support
- Include appropriate logging for LLM operations

## Implementation Considerations

- Use `render_template` for templating prompts, model identifiers, mcp server configs, and output key
- Convert any MCP Server configurations to `MCPServer` instances (via `get_mcp_server`) to pass as `mcp_servers` to the LLM component
- Accept a string for `max_tokens` and convert it to an integer to pass to the LLM component
- In order to support dyanmic output keys, set the result type to `Any` prior to determining the output format and then set the output key immediately after the LLM call
- If `output_format` is an object (JSON schema) or list:
  - Use `json_object_to_pydantic_model` to create a dynamic Pydantic model from the JSON schema
  - Pass the dynamic model to the LLM call as the `output_type` parameter
  - After receiving the results, convert the output to a Dict[str, Any] and store it in the context
- If `output_format` is a list:
  - Wrap the list in an object with a root key `items`:
    ```python
    object_schema = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": // Define the item schema here
            }
        }
    }
    ```
  - Use `json_object_to_pydantic_model` to create a dynamic Pydantic model from the JSON schema
  - Pass the dynamic model to the LLM call as the `output_type` parameter
  - After receiving the results, convert the output to a Dict[str, Any] and store the `items` list in the context
- If `output_format` is "files":
  - Pass the following `FileSpecCollection` model to the LLM call:
    ```python
    class FileSpecCollection(BaseModel):
        files: List[FileSpec]
    ```
  - After receiving the results, store the `files` value (not the entire `FileSpecCollection`) in the context
- Instantiate the `LLM` component with optional MCP servers from context config:
  ```python
  mcp_server_configs = context.get_config().get("mcp_servers", [])
  mcp_servers = [get_mcp_server(logger=self.logger, config=mcp_server_config) for mcp_server_config in mcp_server_configs]
  llm = LLM(logger, model=config.model, mcp_servers=mcp_servers)
  ```
- Use `await llm.generate(prompt, output_type=...)` to perform the generation call

## Logging

- Debug: Log when an LLM call is being made (details of the call are handled by the LLM component)
- Info: None

## Component Dependencies

### Internal Components

- **Protocols**: Uses ContextProtocol for context data access and StepProtocol for the step interface (decouples from concrete Context and BaseStep classes)
- **Step Interface**: Implements the step behavior via `StepProtocol`
- **Context**: Uses a context implementing `ContextProtocol` to retrieve input values and store generation output
- **Models**: Uses the `FileSpec` model for file generation output
- **LLM**: Uses the LLM component class `LLM` from `llm_utils.llm` to interact with language models and optional MCP servers
- **MCP**: Uses the `get_mcp_server` function to convert MCP server configurations to `MCPServer` instances
- **Utils/Models**: Uses `json_object_to_pydantic_model` to create dynamic Pydantic models from JSON objects, after receiving the results from the LLM use `.model_dump()` to convert the Pydantic model to a dictionary
- **Utils/Templates**: Uses `render_template` for dynamic content resolution in prompts and model identifiers

### External Libraries

- **Pydantic**: For BaseModel creation

### Configuration Dependencies

None

## Error Handling

- Handle LLM-related errors gracefully
- Log LLM call failures with meaningful context
- Ensure proper error propagation for debugging
- Validate configuration before making LLM calls

## Output Files

- `recipe_executor/steps/llm_generate.py`
