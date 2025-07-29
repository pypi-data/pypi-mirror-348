import inspect
import json
import logging
from dataclasses import fields, is_dataclass
from typing import (
    Any,
    Awaitable,
    Callable,
    Concatenate,
    Dict,
    List,
    Optional,
    ParamSpec,
    Type,
    TypeVar,
    Union,
)

logger = logging.getLogger(__name__)

# Define a TypeVar for dataclass types
T = TypeVar("T")
# Define a ParamSpec for user llm function signatures
P = ParamSpec("P")


class Agent:
    """
    A lightweight Agent class that implements agent functionality for any LLM backend.
    The Agent represents an intelligent entity with its own prompts, memory, tool-calling capabilities,
    and structured output abilities.
    """

    def __init__(
        self,
        llm_interaction_func: Callable[
            Concatenate[List[Dict[str, str]], P], Awaitable[str]
        ],
        initial_prompt: Optional[List[Dict[str, str]]] = None,
        tools: Optional[List[Callable[[str], Awaitable[str]]]] = None,
        default_temperature: Optional[float] = None,
        default_max_tokens: Optional[int] = None,
        max_iterations: int = 5,
        tool_selection_prompt_type: str = "json_string",
    ):
        """
        Initialize an Agent object.

        Parameters:
            llm_interaction_func: Async function for LLM interaction. Takes a list of messages following OpenAI format and returns LLM's response string
            initial_prompt: Initial prompt list following OpenAI message format
            tools: List of tool functions. Each tool is an async function that takes a string parameter and returns a string result.
                  The tool's __name__ attribute is used as the tool name, and __doc__ as the tool description
            temperature: Optional temperature parameter for LLM (implementation depends on llm_interaction_func)
            max_tokens: Optional maximum number of tokens for LLM (implementation depends on llm_interaction_func)
            max_iterations: Maximum number of iterations for tool interactions or internal reasoning in one query call
            tool_selection_prompt_type: Type of tool selection prompt.
                                      "json_string": Prompts LLM to output JSON string with tool name and parameters
                                      "function_call_object": Prompts LLM to output OpenAI-like function call object
                                      (Note: This is still implemented via prompting, not relying on LLM's built-in features)
        """
        self.llm_interaction_func = llm_interaction_func
        self.initial_prompt = initial_prompt.copy() if initial_prompt else []
        self.memory: List[Dict[str, str]] = self.initial_prompt.copy()
        self.tools = tools if tools else []
        self.tool_map: Dict[str, Callable[[str], Awaitable[str]]] = {
            tool.__name__: tool for tool in self.tools
        }
        self.temperature = default_temperature
        self.max_tokens = default_max_tokens
        self.max_iterations = max_iterations
        self.tool_selection_prompt_type = tool_selection_prompt_type

        self._system_prompt_parts: List[str] = []
        self._build_system_prompt()

    def _build_system_prompt(self, structured_output_type: Optional[Type[T]] = None):
        """
        Build system prompt including tool descriptions and structured output instructions.

        Parameters:
            structured_output_type: Optional structured output type
        """
        self._system_prompt_parts = []

        # 1. 工具提示
        if self.tools:
            tool_descriptions = []
            for tool in self.tools:
                tool_name = tool.__name__
                tool_doc = (
                    inspect.getdoc(tool) or "No description available for this tool."
                )
                # 尝试从类型提示获取参数信息 (简化版，只获取第一个参数名)
                try:
                    sig = inspect.signature(tool)
                    param_name = next(iter(sig.parameters.keys()), "input")
                except Exception:
                    param_name = "input"

                if self.tool_selection_prompt_type == "json_string":
                    tool_descriptions.append(
                        f'- "{tool_name}": {tool_doc} Call with JSON: {{"tool_name": "{tool_name}", "tool_input": "<value>"}}'
                    )
                elif self.tool_selection_prompt_type == "function_call_object":
                    tool_descriptions.append(
                        f"""{{
    "name": "{tool_name}",
    "description": "{tool_doc}",
    "parameters": {{
        "type": "object",
        "properties": {{
            "{param_name}": {{
                "type": "string",
                "description": "The input string for the tool."
            }}
        }},
        "required": ["{param_name}"]
    }}
}}"""
                    )

            if self.tool_selection_prompt_type == "json_string":
                self._system_prompt_parts.append(
                    "You have access to the following tools. "
                    "If you need to use a tool, respond ONLY with a single JSON string matching the tool's call format. "
                    "Do not include any other text or explanation before or after the JSON. "
                    "If you don't need to use a tool, respond to the user directly.\n"
                    "Available tools:\n" + "\n".join(tool_descriptions)
                )
            elif self.tool_selection_prompt_type == "function_call_object":
                self._system_prompt_parts.append(
                    "You have access to the following tools. "
                    "If you decide to use a tool, respond ONLY with a JSON object in the following format, "
                    "containing 'tool_name' and 'arguments' (which itself is an object). "
                    "Do not include any other text or explanation before or after the JSON.\n"
                    'Example: {"tool_name": "tool_name_example", "arguments": {"arg_name": "value"}}\n'
                    "Available tool schemas:\n[\n"
                    + ",\n".join(tool_descriptions)
                    + "\n]\n"
                    "If you don't need to use a tool, respond to the user directly."
                )

        # 2. 结构化输出提示 (如果最终答案需要结构化)
        if structured_output_type:
            if not is_dataclass(structured_output_type):
                raise ValueError("structured_output_type must be a dataclass.")

            field_details = []
            example_json_parts = []
            for f in fields(structured_output_type):
                field_type_name = (
                    f.type.__name__ if hasattr(f.type, "__name__") else str(f.type)
                )
                field_details.append(f'  "{f.name}": "{field_type_name}"')
                # 为示例生成一个简单的占位符值
                if field_type_name == "str":
                    example_value = f"example {f.name}"
                elif field_type_name == "int":
                    example_value = 0
                elif field_type_name == "float":
                    example_value = 0.0
                elif field_type_name == "bool":
                    example_value = False
                elif field_type_name.startswith("List") or field_type_name.startswith(
                    "list"
                ):
                    example_value = []
                elif field_type_name.startswith("Dict") or field_type_name.startswith(
                    "dict"
                ):
                    example_value = {}
                else:
                    example_value = "..."  # 泛型或复杂类型
                example_json_parts.append(f'    "{f.name}": "{example_value}"')

            json_schema_desc = "{\n" + ",\n".join(field_details) + "\n}"
            example_json = "{\n" + ",\n".join(example_json_parts) + "\n  }"

            self._system_prompt_parts.append(
                f"\nWhen you provide your final answer, and you are not using a tool, "
                f"you MUST format your response as a single JSON object conforming to the following structure. "
                f"Do not include any other text, explanations, or markdown formatting before or after the JSON object. "
                f"Ensure all specified fields are present.\n"
                f"Structure:\n{json_schema_desc}\n"
                f"Example:\n{example_json}"
            )

    def _get_current_messages_with_system_prompt(self) -> List[Dict[str, str]]:
        """
        Combine system prompt with current memory for sending to LLM.
        """
        # 确保系统提示在最前面，并且只有一个
        # 如果内存中已经有系统提示，我们可能会选择替换它或附加到它
        # 这里采用简单策略：如果内存为空或第一个不是系统提示，则添加新的系统提示
        current_messages = self.memory.copy()
        system_prompt_str = "\n\n".join(self._system_prompt_parts)

        if not system_prompt_str:
            return current_messages

        if not current_messages or current_messages[0].get("role") != "system":
            current_messages.insert(0, {"role": "system", "content": system_prompt_str})
        else:
            # 如果已经有系统消息，可以选择合并或替换。这里我们替换。
            current_messages[0]["content"] = system_prompt_str

        return current_messages

    async def query(
        self,
        user_input: str,
        structured_output_type: Optional[Type[T]] = None,
        **kwargs: Any,
    ) -> Union[str, T, Dict[str, Any]]:
        """
        Run an Agent query.

        Parameters:
            user_input: User's input string
            structured_output_type: Optional structured output type
            **kwargs: Additional keyword arguments to pass to llm_interaction_func.
                     These will override any matching parameters set during initialization.

        Returns:
            Response in the appropriate type based on structured_output_type
        """
        # Rebuild system prompt to include new structured output type
        self._build_system_prompt(structured_output_type)

        self.memory.append({"role": "user", "content": user_input})

        # 准备 LLM 调用参数
        llm_kwargs = {}
        if self.temperature is not None:
            llm_kwargs["temperature"] = self.temperature
        if self.max_tokens is not None:
            llm_kwargs["max_tokens"] = self.max_tokens
        # 用户提供的参数优先级更高
        llm_kwargs.update(kwargs)

        for iteration in range(self.max_iterations):
            messages_for_llm = self._get_current_messages_with_system_prompt()

            # Log messages being sent to LLM
            logger.debug(f"--- Iteration {iteration + 1} ---")
            logger.debug("--- Sending to LLM ---")
            for msg in messages_for_llm:
                logger.debug(
                    f"{msg['role']}: {msg['content'][:200]}{'...' if len(msg['content']) > 200 else ''}"
                )

            try:
                # 尝试使用额外参数调用
                llm_response_text = await self.llm_interaction_func(
                    messages_for_llm, **llm_kwargs
                )  # type: ignore
            except TypeError:
                # 如果函数不接受额外参数，则使用基本调用
                llm_response_text = await self.llm_interaction_func(messages_for_llm)  # type: ignore

            # Try parsing tool calls
            if self.tools:
                try:
                    potential_tool_call = json.loads(llm_response_text)
                    tool_name = None
                    tool_input_str = None

                    if (
                        self.tool_selection_prompt_type == "json_string"
                        and isinstance(potential_tool_call, dict)
                        and "tool_name" in potential_tool_call
                        and "tool_input" in potential_tool_call
                    ):
                        tool_name = potential_tool_call["tool_name"]
                        tool_input_obj = potential_tool_call["tool_input"]
                        if isinstance(tool_input_obj, (dict, list)):
                            tool_input_str = json.dumps(tool_input_obj)
                        else:
                            tool_input_str = str(tool_input_obj)

                    elif (
                        self.tool_selection_prompt_type == "function_call_object"
                        and isinstance(potential_tool_call, dict)
                        and "tool_name" in potential_tool_call
                        and "arguments" in potential_tool_call
                        and isinstance(potential_tool_call["arguments"], dict)
                    ):
                        tool_name = potential_tool_call["tool_name"]
                        if potential_tool_call["arguments"]:
                            first_arg_value = next(
                                iter(potential_tool_call["arguments"].values())
                            )
                            if isinstance(first_arg_value, (dict, list)):
                                tool_input_str = json.dumps(first_arg_value)
                            else:
                                tool_input_str = str(first_arg_value)
                        else:
                            tool_input_str = ""

                    if tool_name and tool_name in self.tool_map:
                        self.memory.append(
                            {
                                "role": "assistant",
                                "content": llm_response_text,
                            }
                        )

                        tool_function = self.tool_map[tool_name]
                        try:
                            tool_result = await tool_function(
                                tool_input_str if tool_input_str is not None else ""
                            )
                        except Exception as e:
                            tool_result = f"Error executing tool {tool_name}: {e}"
                            logger.error(f"Error during tool execution: {tool_result}")

                        self.memory.append(
                            {
                                "role": "tool",
                                "name": tool_name,
                                "content": tool_result,
                            }
                        )
                        continue

                except json.JSONDecodeError:
                    pass
                except Exception as e:
                    logger.error(f"Error processing potential tool call: {e}")
                    pass

            self.memory.append({"role": "assistant", "content": llm_response_text})

            if structured_output_type:
                try:
                    parsed_json = json.loads(llm_response_text)
                    structured_object = structured_output_type(**parsed_json)
                    return structured_object
                except json.JSONDecodeError:
                    logger.debug(
                        f"Failed to parse LLM response into structured_output_type (JSONDecodeError). Response: {llm_response_text}"
                    )
                    if iteration == self.max_iterations - 1:
                        return llm_response_text
                except TypeError as e:
                    logger.debug(
                        f"Failed to instantiate dataclass from JSON (TypeError): {e}. Response: {llm_response_text}"
                    )
                    if iteration == self.max_iterations - 1:
                        return llm_response_text
                except ValueError as e:
                    logger.debug(
                        f"Failed to validate JSON against dataclass (ValueError): {e}. Response: {llm_response_text}"
                    )
                    if iteration == self.max_iterations - 1:
                        return llm_response_text
            else:
                return llm_response_text

        final_response = (
            self.memory[-1]["content"]
            if self.memory and self.memory[-1]["role"] == "assistant"
            else "Max iterations reached without a final response."
        )
        logger.debug(
            f"Max iterations reached. Returning last assistant message or fallback: {final_response}"
        )
        return final_response

    def clear_memory(self):
        """
        Clear Agent's memory and reset it to initial prompt state.
        """
        self.memory = self.initial_prompt.copy()
        logger.debug("Memory cleared.")
