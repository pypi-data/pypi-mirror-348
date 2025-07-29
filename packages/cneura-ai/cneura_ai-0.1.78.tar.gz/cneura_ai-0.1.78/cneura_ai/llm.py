from abc import ABC, abstractmethod
import os
import json
import re
from typing import Union, Dict, Any, List, Type
from langchain_google_genai import GoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, create_model, ValidationError


class LLMInterface(ABC):
    @abstractmethod
    def query(self, prompt: str) -> dict:
        """Send a prompt to the LLM and return the structured response"""
        pass


class GeminiLLM(LLMInterface):
    def __init__(self, api_key: str = None, model: str = "gemini-2.0-flash-exp", schema: Dict = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required")

        self.model = GoogleGenerativeAI(model=model, google_api_key=self.api_key)

        if schema:
            self.pydantic_model = self._build_pydantic_model(schema)
            self.parser = PydanticOutputParser(pydantic_object=self.pydantic_model)
        else:
            self.pydantic_model = None
            self.parser = None

    def _build_pydantic_model(self, schema: Dict, model_name="DynamicModel") -> Type[BaseModel]:
        if schema.get("type") == "object":
            properties = schema.get("properties", {})
        else:
            properties = schema  # assume it's already a properties dict

        fields = {}

        for field, config in properties.items():
            if not isinstance(config, dict):
                raise TypeError(f"Invalid config for field '{field}': expected dict, got {type(config).__name__}")

            field_type_str = config.get("type", "string")
            optional = config.get("optional", False)

            if field_type_str == "string":
                field_type = str
            elif field_type_str == "integer":
                field_type = int
            elif field_type_str == "number":
                field_type = float
            elif field_type_str == "boolean":
                field_type = bool
            elif field_type_str == "array":
                item_schema = config.get("items", {"type": "string"})
                item_model = self._build_pydantic_model({"item": item_schema}, model_name + "_" + field)
                item_type = item_model.__annotations__.get("item", Any)
                field_type = List[item_type]
            elif field_type_str == "object":
                nested_schema = {"type": "object", "properties": config.get("properties", {})}
                field_type = self._build_pydantic_model(nested_schema, model_name + "_" + field)
            else:
                field_type = str  # fallback

            default = None if optional else ...
            description = config.get("description", "")
            fields[field] = (field_type, Field(default, description=description))

        return create_model(model_name, **fields)

    def _extract_and_parse_json(self, response: str) -> Union[dict, str]:
        """Extract JSON content from raw LLM response."""
        try:
            match = re.search(r"```json(.*?)```", response, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                return json.loads(json_str)

            json_match = re.search(r"{.*}", response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())

            return json.loads(response)
        except json.JSONDecodeError:
            return response

    def _generate_custom_format_prompt(self, schema: Dict = None) -> str:
        if not schema or "properties" not in schema:
            return ""

        def build_example_value(field_type: str) -> str:
            return {
                "string": "\"example string\"",
                "integer": "123",
                "number": "3.14",
                "boolean": "true",
                "array": "[...]",
                "object": "{...}"
            }.get(field_type, "\"example\"")

        example_items = []
        for field, config in schema.get("properties", {}).items():
            field_type = config.get("type", "string")
            example_items.append(f'    "{field}": {build_example_value(field_type)}')

        example_json = "{\n" + ",\n".join(example_items) + "\n}"

        instructions = (
            "Instruction:\n"
            "* Return only a valid JSON object with the following structure, and nothing else:\n"
            f"{example_json}\n\n"
            "- Do not include Markdown code blocks like ```python or ```json.\n"
            "- Do not include the raw JSON schema.\n"
            "- Do not include any explanations or comments outside the JSON.\n"
            "- The JSON must be valid and parseable by json.loads().\n"
        )
        return instructions

    def query(self, prompts: Union[str, List[Union[str, tuple]]], schema: Dict = None) -> dict:
        parser = None
        if schema:
            model = self._build_pydantic_model(schema)
            parser = PydanticOutputParser(pydantic_object=model)
        elif self.parser:
            parser = self.parser

        if isinstance(prompts, str):
            prompts = [prompts]

        format_instructions = parser.get_format_instructions() if parser else ""
        custom_format_prompt = self._generate_custom_format_prompt(schema)

        formatted_prompts = []
        for prompt in prompts:
            if isinstance(prompt, tuple):
                role, content = prompt
                prompt = f"{role}: {content}"
            elif not isinstance(prompt, str):
                raise ValueError(f"Each prompt must be a string or (role, content) tuple, got: {type(prompt)}")

            full_prompt = f"{prompt.strip()}\n{custom_format_prompt}\n{format_instructions}".strip()
            formatted_prompts.append(full_prompt)

        full_input = "\n".join(formatted_prompts)
        response = self.model.invoke(full_input)
        # print(response)

        if not response:
            return {"success": False, "error": "No response from LLM"}

        response_text = response.content if hasattr(response, "content") else str(response)

        if schema:
            parsed = self._extract_and_parse_json(response_text)
            if isinstance(parsed, dict) and parser:
                try:
                    validated = parser.pydantic_object.parse_obj(parsed)
                    return {"success": True, "data": validated.dict()}
                except ValidationError as e:
                    return {"success": False, "error": str(e), "raw": parsed}
            return {"success": True, "data": parsed}

        return {"success": True, "data": response_text}
