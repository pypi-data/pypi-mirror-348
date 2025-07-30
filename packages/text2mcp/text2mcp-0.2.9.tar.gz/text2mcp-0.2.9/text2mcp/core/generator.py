"""
Code generator module, used to generate MCP service code from natural language descriptions
"""
import os
import re
import logging
from typing import Optional, Dict, Any, Union, List

# Add conditional import for yaml
try:
    import yaml
except ImportError:
    logging.warning("PyYAML library not installed, YAML front matter functionality in Markdown templates will not be available")
    yaml = None

from text2mcp.utils.config import load_config, LLMConfig
from text2mcp.utils.llm_client import LLMClientFactory

logger = logging.getLogger(__name__)

class CodeGenerator:
    """
    Code generator class, responsible for converting natural language descriptions into MCP service code
    """
    
    def __init__(self, config_file: Optional[str] = None, api_key: Optional[str] = None, 
                 model: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the code generator
        
        Args:
            config_file: Optional configuration file path, if not provided, default configuration lookup logic is used
            api_key: Optional OpenAI API key, directly passed parameters have highest priority
            model: Optional LLM model name, directly passed parameters have highest priority
            base_url: Optional OpenAI compatible interface base URL, directly passed parameters have highest priority
        """
        # Load configuration
        self.config = load_config(config_file)
        self.llm_config: LLMConfig = self.config.get("llm_config")
        self.llm_client = None
        self.model = None
        
        # If parameters are passed directly, override the settings in the configuration
        if api_key or model or base_url:
            if not self.llm_config:
                # If there is no configuration, create a new one
                self.llm_config = LLMConfig(
                    api_key=api_key or "",
                    model=model or "gpt-3.5-turbo",
                    base_url=base_url
                )
                self.config["llm_config"] = self.llm_config
            else:
                # Use the passed parameters to override the existing configuration
                if api_key:
                    self.llm_config.api_key = api_key
                if model:
                    self.llm_config.model = model
                if base_url is not None:  # Allow explicit setting to None
                    self.llm_config.base_url = base_url
        
        if not self.llm_config:
            logger.warning("LLM configuration not found, code generation functionality will not be available")
        else:
            self.model = self.llm_config.model
            logger.info(f"Using model: {self.model}")
            
            # Initialize LLM client
            self.llm_client = LLMClientFactory.create_client(self.llm_config)
            if self.llm_client:
                logger.info(f"OpenAI client initialization successful")
            else:
                logger.warning("LLM client initialization failed")
    
    def _fill_template_slots(self, template: str, replacements: Dict[str, str], default_values: Optional[Dict[str, str]] = None) -> str:
        """
        Fill template slots with provided replacements
        
        Args:
            template: Template string with {{slot}} placeholders
            replacements: Dictionary of slot names and their replacement values
            default_values: Optional dictionary of default values for slots
            
        Returns:
            str: Template with slots filled
        """
        result = template
        
        # Find all slots in the template
        slots = re.findall(r'\{\{(\w+)\}\}', template)
        
        # Track unfilled slots
        unfilled_slots = []
        
        # Replace each slot
        for slot in slots:
            replacement = replacements.get(slot)
            
            if replacement is not None:
                result = result.replace(f"{{{{{slot}}}}}", replacement)
            elif default_values and slot in default_values:
                result = result.replace(f"{{{{{slot}}}}}", default_values[slot])
                logger.debug(f"Used default value for slot '{slot}'")
            else:
                unfilled_slots.append(slot)
        
        # Log unfilled slots
        if unfilled_slots:
            logger.warning(f"The following template slots were not filled: {', '.join(unfilled_slots)}")
        
        return result
    
    def _call_llm(self, prompt: str) -> str:
        """
        Call LLM API to generate code
        
        Args:
            prompt: Prompt text
            
        Returns:
            str: LLM response text
        """
        logger.info("Sending request to LLM...")
        try:
            # Call LLM API
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an assistant specialized in generating Python code. Output only the raw Python code based on the user's request, wrapped in ```python markdown blocks."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Adjust the balance between creativity and determinism
            )
            logger.debug(f"LLM response: {response}")
            response_text = response.choices[0].message.content
            return response_text
        except Exception as e:
            logger.error(f"Error occurred when calling LLM: {e}", exc_info=True)
            return f"# Error calling LLM: {e}"
    
    def _extract_code(self, response: str) -> str:
        """
        Extract code blocks from LLM response
        
        Args:
            response: LLM response text
            
        Returns:
            str: Extracted code
        """
        # Extract code from markdown format
        code_pattern = r"```(?:python)?\s*([\s\S]*?)\s*```"
        matches = re.findall(code_pattern, response)
        
        if matches:
            # If multiple code blocks present, join them
            code = "\n\n".join(matches)
            return code
        else:
            logger.warning("No code blocks found in LLM response, using raw response")
            return response
    
    def _extract_code_from_markdown(self, markdown_content: str) -> str:
        """
        Extract Python code blocks from Markdown content and integrate them
        
        Args:
            markdown_content: Markdown formatted content
            
        Returns:
            str: Integrated Python code
        """
        # Extract all Python code blocks
        code_blocks = re.findall(r"```(?:python|Python)\s*([\s\S]*?)\s*```", markdown_content)
        
        if not code_blocks:
            logger.warning("No Python code blocks found in the Markdown template")
            return self._get_default_template()
        
        # Try to extract YAML front matter
        yaml_metadata = {}
        yaml_match = re.match(r"---\s*([\s\S]*?)\s*---", markdown_content)
        metadata_comment = ["# Template metadata:"]
        
        if yaml_match:
            try:
                if yaml:  # Ensure yaml module is imported
                    yaml_metadata = yaml.safe_load(yaml_match.group(1))
                    # Add metadata as comments
                    if yaml_metadata and isinstance(yaml_metadata, dict):
                        for key, value in yaml_metadata.items():
                            metadata_comment.append(f"# {key}: {value}")
                    logger.info(f"Extracted metadata from Markdown template: {yaml_metadata}")
            except Exception as e:
                logger.warning(f"Error parsing YAML metadata: {e}")
        
        # Integrate all code blocks
        combined_code = []
        combined_code.append("\n".join(metadata_comment) + "\n")
        
        # Check if there are specific section markers in the Markdown
        sections = re.findall(r"#+\s*(.*?)\s*\n\s*```python\s*([\s\S]*?)\s*```", markdown_content)
        
        if sections:
            logger.info(f"Found {len(sections)} code sections in Markdown template")
            
            # Process sections with headers and code
            for section_name, section_code in sections:
                combined_code.append(f"# {section_name}")
                combined_code.append(section_code)
        else:
            # No section markers, combine all code blocks
            for code in code_blocks:
                combined_code.append(code)
        
        result = "\n\n".join(combined_code)
        
        # Validate the generated code
        try:
            compile(result, "<string>", "exec")  # Validate syntax
            logger.info("Code generated from Markdown passed syntax validation")
        except SyntaxError as e:
            logger.warning(f"Syntax error in code generated from Markdown: {e}")
            # Log the error but continue using the generated code, as LLM might be able to fix these issues
        
        return result
    
    def _load_template_content(self, template_file: str, extract_code: bool = False) -> str:
        """
        Load template file content with unified logic
        
        Args:
            template_file: Template filename or path
            extract_code: Whether to extract code blocks from markdown
            
        Returns:
            str: Template file content
        """
        # Add .md extension if missing
        if not template_file.endswith('.md'):
            template_file = template_file + '.md'
        
        # Define list of possible template paths
        package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        possible_paths = [
            template_file,  # Current directory/absolute path
            os.path.join(package_dir, "templates", template_file),  # templates in package installation directory
            os.path.join(package_dir, "..", "examples", template_file)  # examples in project root directory
        ]
        
        # Iterate through possible paths
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    logger.info(f"Successfully loaded template file: {path}")
                    
                    # If extracting code and it's a markdown file
                    if extract_code and path.endswith('.md'):
                        return self._extract_code_from_markdown(content)
                    
                    return content
                except Exception as e:
                    logger.error(f"Error reading template file {path}: {e}", exc_info=True)
                    # Continue trying the next possible path
        
        # If all paths fail
        logger.warning(f"Template file not found: {template_file}")
        return "" if not extract_code else self._get_default_template()
    
    def _load_template(self, template_file: str) -> str:
        """
        Load template file and extract code (legacy method)
        
        Args:
            template_file: Template filename or path
            
        Returns:
            str: Extracted code from template file
        """
        return self._load_template_content(template_file, extract_code=True)
    
    def _load_markdown_template(self, template_file: str) -> str:
        """
        Load markdown template file content without extracting code (legacy method)
        
        Args:
            template_file: Template filename or path
            
        Returns:
            str: Raw template file content
        """
        return self._load_template_content(template_file, extract_code=False)
    
    def _get_default_template(self) -> str:
        """
        Get default MCP service template
        
        Returns:
            str: Default template content
        """
        return '''
import argparse
import logging
import uvicorn
import time
from fastapi.responses import JSONResponse
from mcp.server import FastMCP, Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount

mcp = FastMCP("example.py")

logger = logging.getLogger(__name__)

@mcp.tool()
async def example_function(param1: str, param2: int):
    """
    Example MCP tool
    :param param1: Input parameter 1
    :param param2: Input parameter 2
    :return: Output result
    """
    # Implement code logic
    result = f"Process {param1} and {param2}"
    return result

async def health_check(request):
    """Health check endpoint"""
    return JSONResponse({"status": "healthy", "timestamp": int(time.time())}) 

def create_starlette_app(mcp_server: Server, *, debug: bool = False):
    """Create a Starlette application that provides MCP service"""
    sse = SseServerTransport("/messages/")
    
    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )
    
    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
            Route("/sse/health", endpoint=health_check, methods=["GET"])
        ],
    )    

if __name__ == "__main__":
    mcp_server = mcp._mcp_server

    parser = argparse.ArgumentParser(description='Run MCP SSE server')
    parser.add_argument("--host", default="0.0.0.0", help="Server host")
    parser.add_argument("--port", default=12345, type=int, help="Server port")
    args = parser.parse_args()
 
    starlette_app = create_starlette_app(mcp_server, debug=True)
    uvicorn.run(starlette_app, host=args.host, port=args.port)
'''
    
    def _get_default_prompt_template(self) -> str:
        """
        Get default prompt template for LLM
        
        Returns:
            str: Default prompt template content
        """
        return '''
You are a professional MCP service development expert. Your task is to generate MCP service code based on the following description:

{{description}}

REQUIREMENTS:
1. Create a complete, high-quality Python code that implements an MCP service
2. Follow the MCP framework structure exactly as shown in the template
3. Include proper error handling and logging
4. Provide appropriate comments and documentation
5. Implement all required functionality
6. Make sure the code is optimized and follows best practices
7. Create a robust, production-ready implementation

{{additional_info}}

OUTPUT ONLY THE COMPLETE PYTHON CODE. DO NOT INCLUDE ANY ADDITIONAL EXPLANATIONS OR MARKDOWN FORMATTING.
'''
    
    def generate(self, description: str, template_file: str = "code_template.md") -> Optional[str]:
        """
        Generate MCP service code based on natural language description (legacy mode)
        
        This is the traditional generation method. It is now a wrapper around the
        modular template approach for backward compatibility.
        
        Args:
            description: Text describing the required code functionality
            template_file: Optional template file name
            
        Returns:
            Optional[str]: Generated code, or None if generation fails
        """
        logger.info("Using legacy generation method (wrapper for modular templates)")
        return self.generate_with_modular_templates(
            description=description,
            code_template=template_file
        )
    
    def generate_with_modular_templates(self, 
                                        description: str, 
                                        prompt_template: Optional[Union[str, Dict[str, str]]] = None,
                                        code_template: Optional[Union[str, Dict[str, str]]] = None, 
                                        additional_template: Optional[Union[str, Dict[str, str]]] = None,
                                        slot_values: Optional[Dict[str, str]] = None) -> Optional[str]:
        """
        Generate MCP service code based on natural language description using modular templates
        
        Args:
            description: Text describing the required code functionality
            prompt_template: Optional prompt template file path or content string
            code_template: Optional code template file path or content string
            additional_template: Optional additional information template file path or content string
            slot_values: Optional dictionary of additional slot values to fill in templates
            
        Returns:
            Optional[str]: Generated code, or None if generation fails
        """
        if not self.llm_client:
            logger.error("Cannot generate code: LLM client not initialized")
            return None
        
        # Load prompt template
        prompt_content = ""
        if prompt_template is None:
            # Use default prompt template
            prompt_content = self._get_default_prompt_template()
            logger.info("Using default prompt template")
        elif isinstance(prompt_template, str):
            if os.path.exists(prompt_template) or len(prompt_template) < 100:
                # Treat as file path
                prompt_content = self._load_template_content(prompt_template, extract_code=False)
                if not prompt_content:
                    logger.warning(f"Failed to load prompt template file: {prompt_template}. Using default template.")
                    prompt_content = self._get_default_prompt_template()
            else:
                # Treat as content string
                prompt_content = prompt_template
                logger.info("Using provided prompt template string")
        elif isinstance(prompt_template, dict) and "content" in prompt_template:
            prompt_content = prompt_template["content"]
            logger.info("Using prompt template from dictionary")
        else:
            logger.warning("Invalid prompt template format. Using default template.")
            prompt_content = self._get_default_prompt_template()
        
        # Load code template
        code_content = ""
        if code_template is None:
            # Use default code template
            code_content = self._load_template_content("code_template.md", extract_code=True)
            logger.info("Using default code template")
        elif isinstance(code_template, str):
            if os.path.exists(code_template) or len(code_template) < 100:
                # Treat as file path
                code_content = self._load_template_content(code_template, extract_code=True)
                if not code_content or code_content == self._get_default_template():
                    logger.warning(f"Failed to load code template file: {code_template}. Using default template.")
                    code_content = self._load_template_content("code_template.md", extract_code=True)
            else:
                # Treat as content string
                code_content = code_template
                logger.info("Using provided code template string")
        elif isinstance(code_template, dict) and "content" in code_template:
            code_content = code_template["content"]
            logger.info("Using code template from dictionary")
        else:
            logger.warning("Invalid code template format. Using default template.")
            code_content = self._load_template_content("code_template.md", extract_code=True)
        
        # Load additional template
        additional_content = ""
        if additional_template is not None:
            if isinstance(additional_template, str):
                if os.path.exists(additional_template) or len(additional_template) < 100:
                    # Treat as file path
                    additional_content = self._load_template_content(additional_template, extract_code=False)
                    if not additional_content:
                        logger.warning(f"Failed to load additional template file: {additional_template}. Using empty string.")
                else:
                    # Treat as content string
                    additional_content = additional_template
                    logger.info("Using provided additional template string")
            elif isinstance(additional_template, dict) and "content" in additional_template:
                additional_content = additional_template["content"]
                logger.info("Using additional template from dictionary")
        
        # Prepare replacements dictionary with required values
        replacements = {
            "description": description,
            "additional_info": additional_content,
            "code_template": code_content
        }
        
        # Add user-provided slot values if any
        if slot_values:
            replacements.update(slot_values)
            
        # Default values for common slots
        default_values = {
            "service_name": "mcp_service",
            "tool_name": "process_data",
            "tool_description": "Process input data and return results",
            "param1_description": "First input parameter",
            "param2_description": "Second input parameter",
            "return_description": "Processing result"
        }
        
        # Fill slots in prompt template
        prompt = self._fill_template_slots(prompt_content, replacements, default_values)
        
        # Add code template to prompt if not already included in the template
        if "{{code_template}}" not in prompt_content:
            prompt += f"\n\nPlease strictly implement the MCP service according to the following template example:\n\n{code_content}\n\nDo not output any explanatory content, only the code"
        
        logger.info("Requesting code generation with modular templates...")
        raw_response = self._call_llm(prompt)
        
        if raw_response and not raw_response.startswith("# Error"):
            extracted_code = self._extract_code(raw_response)
            return extracted_code
        else:
            logger.error(f"Failed to get valid response from LLM. Raw response: {raw_response}")
            return None
    
    def save_to_file(self, code: str, filename: str, directory: str = "./") -> Optional[str]:
        """
        Save generated code to file
        
        Args:
            code: Code to save
            filename: Target filename
            directory: Target directory path
            
        Returns:
            Optional[str]: Full path of the saved file, or None if saving fails
        """
        if not code:
            logger.error("Cannot save empty code")
            return None
            
        if not filename.endswith(".py"):
            filename += ".py"
            logger.info(f"Added '.py' extension. Filename is now: {filename}")
        
        absolute_directory = os.path.abspath(directory)
        full_path = os.path.join(absolute_directory, filename).replace("\\", "/")

        try:
            # Create directory if it doesn't exist
            os.makedirs(directory, exist_ok=True) 
            
            # Write code to file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(code)
            logger.info(f"Code successfully saved to: {full_path}")
            return full_path
        except OSError as e:
            logger.error(f"Error creating directory '{directory}': {e}")
            return None
        except IOError as e:
            logger.error(f"Error writing code to file '{full_path}': {e}")
            return None
        except Exception as e:
             logger.error(f"Unexpected error when saving file: {e}", exc_info=True)
             return None 
