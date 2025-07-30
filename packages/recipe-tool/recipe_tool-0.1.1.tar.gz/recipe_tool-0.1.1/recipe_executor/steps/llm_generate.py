import logging
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from recipe_executor.llm_utils.llm import LLM
from recipe_executor.llm_utils.mcp import get_mcp_server
from recipe_executor.models import FileSpec
from recipe_executor.protocols import ContextProtocol
from recipe_executor.steps.base import BaseStep, StepConfig
from recipe_executor.utils.models import json_object_to_pydantic_model
from recipe_executor.utils.templates import render_template


class LLMGenerateConfig(StepConfig):
    """
    Config for LLMGenerateStep.

    Fields:
        prompt: The prompt to send to the LLM (templated beforehand).
        model: The model identifier to use (provider/model_name format).
        max_tokens: The maximum number of tokens for the LLM response.
        mcp_servers: List of MCP server configurations for access to tools.
        output_format: The format of the LLM output (text, files, or JSON/list schemas).
        output_key: The name under which to store the LLM output in context.
    """

    prompt: str
    model: str = "openai/gpt-4o"
    max_tokens: Optional[Union[str, int]] = None
    mcp_servers: Optional[List[Dict[str, Any]]] = None
    output_format: Union[str, Dict[str, Any], List[Any]]
    output_key: str = "llm_output"


class FileSpecCollection(BaseModel):
    files: List[FileSpec]


def _render_config(config: Dict[str, Any], context: ContextProtocol) -> Dict[str, Any]:
    """
    Recursively render templated strings in a dict.
    """
    result: Dict[str, Any] = {}
    for key, value in config.items():
        if isinstance(value, str):
            result[key] = render_template(value, context)
        elif isinstance(value, dict):
            result[key] = _render_config(value, context)
        elif isinstance(value, list):
            items: List[Any] = []
            for item in value:
                if isinstance(item, dict):
                    items.append(_render_config(item, context))
                else:
                    items.append(item)
            result[key] = items
        else:
            result[key] = value
    return result


class LLMGenerateStep(BaseStep[LLMGenerateConfig]):
    """
    Step to generate content via a large language model (LLM).
    """

    def __init__(self, logger: logging.Logger, config: Dict[str, Any]) -> None:
        super().__init__(logger, LLMGenerateConfig(**config))

    async def execute(self, context: ContextProtocol) -> None:
        # Render templates for core inputs
        prompt: str = render_template(self.config.prompt, context)
        model_id: str = render_template(self.config.model, context)
        output_key: str = render_template(self.config.output_key, context)

        # Prepare max_tokens
        raw_max = self.config.max_tokens
        max_tokens: Optional[int] = None
        if raw_max is not None:
            max_str = render_template(str(raw_max), context)
            try:
                max_tokens = int(max_str)
            except ValueError:
                raise ValueError(f"Invalid max_tokens value: {raw_max!r}")

        # Collect MCP server configurations
        mcp_cfgs: List[Dict[str, Any]] = []
        if self.config.mcp_servers:
            mcp_cfgs.extend(self.config.mcp_servers)
        ctx_mcp = context.get_config().get("mcp_servers") or []
        if isinstance(ctx_mcp, list):
            mcp_cfgs.extend(ctx_mcp)

        mcp_servers: List[Any] = []
        for cfg in mcp_cfgs:
            rendered = _render_config(cfg, context)
            server = get_mcp_server(logger=self.logger, config=rendered)
            mcp_servers.append(server)

        # Initialize LLM client
        llm = LLM(
            logger=self.logger,
            model=model_id,
            mcp_servers=mcp_servers or None,
        )
        output_format = self.config.output_format
        result: Any = None

        try:
            self.logger.debug(
                "Calling LLM: model=%s, format=%r, max_tokens=%s, mcp_servers=%r",
                model_id,
                output_format,
                max_tokens,
                mcp_servers,
            )
            # Text output
            if output_format == "text":  # type: ignore
                kwargs: Dict[str, Any] = {"output_type": str}
                if max_tokens is not None:
                    kwargs["max_tokens"] = max_tokens
                result = await llm.generate(prompt, **kwargs)
                context[output_key] = result

            # Files output
            elif output_format == "files":  # type: ignore
                kwargs = {"output_type": FileSpecCollection}
                if max_tokens is not None:
                    kwargs["max_tokens"] = max_tokens
                result = await llm.generate(prompt, **kwargs)
                # Store only the list of FileSpec
                context[output_key] = result.files

            # JSON object schema
            elif isinstance(output_format, dict):
                schema_model = json_object_to_pydantic_model(output_format, model_name="LLMObject")
                kwargs = {"output_type": schema_model}
                if max_tokens is not None:
                    kwargs["max_tokens"] = max_tokens
                result = await llm.generate(prompt, **kwargs)
                context[output_key] = result.model_dump()

            # List schema
            elif isinstance(output_format, list):  # type: ignore
                if len(output_format) != 1 or not isinstance(output_format[0], dict):
                    raise ValueError(
                        "When output_format is a list, it must be a single-item list containing a schema object."
                    )
                item_schema = output_format[0]
                wrapper_schema: Dict[str, Any] = {
                    "type": "object",
                    "properties": {"items": {"type": "array", "items": item_schema}},
                    "required": ["items"],
                }
                schema_model = json_object_to_pydantic_model(wrapper_schema, model_name="LLMListWrapper")
                kwargs = {"output_type": schema_model}
                if max_tokens is not None:
                    kwargs["max_tokens"] = max_tokens
                result = await llm.generate(prompt, **kwargs)
                wrapper = result.model_dump()
                context[output_key] = wrapper.get("items", [])

            else:
                raise ValueError(f"Unsupported output_format: {output_format!r}")

        except Exception as exc:
            self.logger.error("LLM generate failed: %r", exc, exc_info=True)
            raise
