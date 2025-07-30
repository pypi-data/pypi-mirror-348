# vlm_inference/inference.py
"""
The model can be loaded by a local opensource model or  call the api
Clase VLMInference: recibe imágenes: 
INPUT:

    # Single image or a list of images, because in the future maybe we want to do stitching, but for now I want just to process one 
    # Status (Optional)
devuelve JSON con:
OUTPUT:
    • actions: {type: Navigation | Interaction, parameters}  
    • description: texto descriptivo  
    • obstacles: lista de obstáculos detectados  
    • status: enum {OK, BLOCKED, ERROR, NEED_HELP} 

For now we are going just to call the api of OPENAI, But future developments it will try to call a opensource model

"""
import os
import json
import base64
import io
from enum import Enum
from typing import Dict, List, Union, TypedDict
from pathlib import Path

import yaml
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import numpy as np
import importlib.resources

import time

# Type definitions
class Status(str, Enum):
    OK = "OK"
    BLOCKED = "BLOCKED"
    ERROR = "ERROR"
    NEED_HELP = "NEED_HELP"

class ActionParameters(TypedDict):
    direction: str
    angle: int
    distance: float

class Action(TypedDict):
    type: str
    parameters: ActionParameters

class InferenceResult(TypedDict):
    actions: List[Action]
    description: str
    obstacles: List[str]
    status: Status

# Configuration management
class VLMSettings:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.prompt_path = os.getenv(
            "VLM_NAV_PROMPT_PATH",
            "vlm_navigation/prompt_manager/navigation_prompt.txt"
        )

class VLMInferenceError(Exception):
    """Base exception for inference errors"""
    pass

class VLMInference:
    """
    Handles visual-language model inference for navigation tasks.
    
    Args:
        provider: Inference provider (API or local model)
        settings: Configuration settings
    """
    
    def __init__(self, provider: str = "openai", settings: VLMSettings = None):
        self.settings = settings or VLMSettings()
        self.provider = provider 
        self._validate_settings()
        
        self.provider = provider
        self.prompt_template = self._load_prompt()
        self.client = self._initialize_client()

    def _validate_settings(self) -> None:
        """Ensure required settings are present"""
        if not self.settings.api_key and self.provider == "openai":
            raise VLMInferenceError("OPENAI_API_KEY required for API provider")

    def _load_prompt(self) -> str:
        """
        Load navigation prompt template.
        Prioritizes VLM_NAV_PROMPT_PATH environment variable.
        If not set, attempts to load 'navigation_prompt.txt' from the package resources.
        """
        prompt_content = None
        # La variable de entorno VLM_NAV_PROMPT_PATH tiene la máxima prioridad.
        # Asumimos que self.settings.prompt_path_from_env contiene el valor de os.getenv("VLM_NAV_PROMPT_PATH")
        # o None si no está definida. (Esto debería inicializarse en VLMSettings).

        # Para que esto funcione, VLMSettings debería tener algo como:
        # self.explicit_prompt_path = os.getenv("VLM_NAV_PROMPT_PATH")

        # Vamos a simplificar y leer la variable de entorno directamente aquí
        # o depender de cómo self.settings.prompt_path fue configurado.
        # El código original para VLMSettings era:
        # self.prompt_path = os.getenv(
        #     "VLM_NAV_PROMPT_PATH",
        #     "vlm_navigation/prompt_manager/navigation_prompt.txt"  <-- este es el default_path_string
        # )
        # Necesitamos saber si el valor en self.settings.prompt_path vino de la variable de entorno
        # o si es el valor por defecto.

        # Una forma más clara es que VLMSettings guarde esta información:
        # class VLMSettings:
        # def __init__(self):
        #     # ...
        #     self.vlm_nav_prompt_path_env = os.getenv("VLM_NAV_PROMPT_PATH")
        #     self.default_prompt_resource_module = "vlm_inference.vlm_navigation.prompt_manager"
        #     self.default_prompt_resource_name = "navigation_prompt.txt"


        # Asumiendo que en VLMSettings tienes:
        # self.vlm_nav_prompt_path_env = os.getenv("VLM_NAV_PROMPT_PATH")
        # Y que el path por defecto NO es lo que queremos usar directamente cuando está instalado.

        # Enfoque actualizado basado en la lógica de tu VLMSettings original:
        # `self.settings.prompt_path` contendrá el valor de la variable de entorno si está seteada,
        # o la ruta por defecto "vlm_navigation/prompt_manager/navigation_prompt.txt" si no lo está.

        # Verificamos si VLM_NAV_PROMPT_PATH fue explícitamente seteada.
        # Es más limpio si VLMSettings expone esto, por ejemplo, con un atributo booleano
        # o si `prompt_path` es None cuando la variable no está seteada y no hay default.
        # Por ahora, haremos una suposición: si `self.settings.prompt_path` NO es la ruta por defecto
        # que pusiste en `os.getenv`, entonces fue seteada por la variable de entorno.

        default_path_string_from_settings = "vlm_navigation/prompt_manager/navigation_prompt.txt" # El valor por defecto de tu os.getenv
        path_from_env_variable = os.getenv("VLM_NAV_PROMPT_PATH")

        if path_from_env_variable:
            # Si la variable de entorno está configurada, usar esa ruta.
            prompt_file_path = Path(path_from_env_variable)
            try:
                prompt_content = prompt_file_path.read_text(encoding='utf-8')
                # print(f"Prompt loaded from environment variable VLM_NAV_PROMPT_PATH: {prompt_file_path}") # Para depuración
            except FileNotFoundError:
                raise VLMInferenceError(
                    f"Error loading prompt: File not found at VLM_NAV_PROMPT_PATH: '{prompt_file_path}'"
                )
            except Exception as e:
                raise VLMInferenceError(
                    f"Error loading prompt from VLM_NAV_PROMPT_PATH '{prompt_file_path}': {str(e)}"
                )
        else:
            # Si la variable de entorno NO está configurada, cargar desde los recursos del paquete.
            # Asumiendo la estructura:
            # tu_paquete_principal (ej: 'vlm_inference')
            #  └── vlm_navigation
            #      └── prompt_manager
            #          └── navigation_prompt.txt
            # El módulo sería 'nombre_paquete_principal.vlm_navigation.prompt_manager'
            # Reemplaza 'vlm_inference' con el nombre real de tu paquete si es diferente.
            package_name_containing_resources = "vlm_inference.vlm_navigation.prompt_manager"
            resource_name = "navigation_prompt.txt"
            try:
                # Para Python 3.9+ puedes usar .files() y .joinpath().read_text()
                # if hasattr(importlib.resources, 'files'):
                #    prompt_content = importlib.resources.files(package_name_containing_resources).joinpath(resource_name).read_text(encoding='utf-8')
                # Para Python 3.7+ (más compatible si no estás seguro de la versión de Python)
                prompt_content = importlib.resources.read_text(
                    package_name_containing_resources,
                    resource_name,
                    encoding='utf-8'
                )
                # print(f"Prompt loaded from package resource: {package_name_containing_resources}/{resource_name}") # Para depuración
            except ModuleNotFoundError:
                # Esto sucedería si la ruta del paquete 'vlm_inference.vlm_navigation.prompt_manager' es incorrecta
                # o los __init__.py no están presentes.
                raise VLMInferenceError(
                    f"Error loading prompt: Could not find the prompt module '{package_name_containing_resources}'. "
                    "Ensure your package structure and __init__.py files are correct. "
                    "Alternatively, set the VLM_NAV_PROMPT_PATH environment variable."
                )
            except FileNotFoundError: # importlib.resources.read_text también puede lanzar esto
                raise VLMInferenceError(
                    f"Error loading prompt: Resource file '{resource_name}' not found within package module '{package_name_containing_resources}'. "
                    "Ensure the file is included in your package (e.g., via setup.py's include_package_data or MANIFEST.in). "
                    "Alternatively, set the VLM_NAV_PROMPT_PATH environment variable."
                )
            except Exception as e:
                raise VLMInferenceError(
                    f"Error loading prompt from package resource '{package_name_containing_resources}/{resource_name}': {str(e)}"
                )
        
        if prompt_content is None:
            # Esto no debería ocurrir si la lógica anterior es correcta, pero como salvaguarda.
            raise VLMInferenceError("Failed to load prompt for an unknown reason.")
            
        return prompt_content

    def _initialize_client(self):
        """Initialize model client based on provider"""
        if self.provider == "openai":
            return OpenAI(api_key=self.settings.api_key)
        # Add other providers here
        raise NotImplementedError(f"Provider {self.provider} not implemented")

    def infer(self, image_input: Union[str, np.ndarray, Image.Image]) -> InferenceResult:
        """
        Perform inference on visual input.
        
        Args:
            image_input: Path to image, PIL Image, or numpy array
            
        Returns:
            Structured navigation instructions
        """
        try:
            data_url = self._process_image_input(image_input)
            response = self._call_model(data_url)
            return self._parse_response(response)
        except Exception as e:
            return self._error_result(str(e))

    def _process_image_input(self, image_input) -> str:
        """Convert various image formats to data URL"""
        if isinstance(image_input, str):
            return encode_image_to_data_url(image_input)
        elif isinstance(image_input, Image.Image):
            return pil_to_data_url(image_input)
        elif isinstance(image_input, np.ndarray):
            return array_to_data_url(image_input)
        raise ValueError("Unsupported image input type")

    def _call_model(self, data_url: str) -> str:
        """Execute model inference call"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self.prompt_template},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ]
                }],
                max_tokens=2048
            )
            #print("-------------raw response-----------------------")
            #print(response.choices[0].message.content)
            #print("------------------------------------")
            return response.choices[0].message.content
        except Exception as e:
            raise VLMInferenceError(f"Model call failed: {str(e)}")

    def _parse_response(self, raw_response: str) -> InferenceResult:
            """Validate and parse model response"""
            cleaned_response = raw_response.strip() # Remove leading/trailing whitespace

            # Check if the response is wrapped in markdown json code block
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[len("```json"):].strip() # Remove ```json prefix
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-len("```")].strip() # Remove ``` suffix
            elif cleaned_response.startswith("```"): # In case it's just ``` (without json)
                cleaned_response = cleaned_response[len("```"):].strip()
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-len("```")].strip()

            try:
                # Ensure the string isn't empty after stripping
                if not cleaned_response:
                    # Handle case where the response might have been only the markdown fences
                    raise VLMInferenceError("Empty response after stripping markdown")

                response_data = json.loads(cleaned_response)
                return {
                    "actions": response_data.get("actions", []),
                    "description": response_data.get("description", ""),
                    "obstacles": response_data.get("obstacles", []),
                    "status": Status(response_data.get("status", Status.ERROR.value))
                }
            except json.JSONDecodeError as e:
                # It can be helpful to log what you tried to parse
                error_message = f"Invalid JSON response after cleaning. Original error: {str(e)}. Attempted to parse: '{cleaned_response[:200]}...'"
                raise VLMInferenceError(error_message)
            except ValueError as e: # For Status enum conversion
                raise VLMInferenceError(f"Invalid status value: {str(e)}. Value was: '{response_data.get('status')}'")
            except Exception as e: # Catch any other unexpected errors during parsing
                raise VLMInferenceError(f"An unexpected error occurred during response parsing: {str(e)}")

    def _error_result(self, error_msg: str) -> InferenceResult:
        """Generate error result payload"""
        return {
            "actions": [],
            "description": "",
            "obstacles": [],
            "status": Status.ERROR,
            "error": error_msg
        }

# Image processing utilities
def encode_image_to_data_url(img_path: str) -> str:
    """Encode image file to base64 data URL"""
    with Image.open(img_path) as img:
        return pil_to_data_url(img)

def pil_to_data_url(img: Image.Image, format: str = "JPEG") -> str:
    """Convert PIL Image to data URL"""
    buffered = io.BytesIO()
    img.save(buffered, format=format)
    b64 = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/{format.lower()};base64,{b64}"

def array_to_data_url(arr: np.ndarray) -> str:
    """Convert numpy array to data URL"""
    img = Image.fromarray(arr)
    return pil_to_data_url(img)

if __name__ == "__main__":
    # Example usage
    inference = VLMInference()
    for i in range(3):
        click = time.time()
        print(f"Try No:{i}")
        result = inference.infer("./batroom_images_path_multiview/1_left.jpg")
        clock = time.time()
        #print(result)
        print(json.dumps(result, indent=2))
        print(f"Total time with the API: {clock-click}")

        print("---------------------------------")
        navigation_action = result["actions"][0]
        action_type = navigation_action.get("type")
        parameters = navigation_action.get("parameters", {})
        direction = parameters.get("direction")
        angle = parameters.get("angle")
        distance = parameters.get("distance")
        obstacle_avoidance_strategy = navigation_action.get("obstacle_avoidance_strategy")

        print("\nValores desempaquetados:")
        print(f"Tipo de acción: {action_type}")
        print(f"Dirección: {direction}")
        print(f"Ángulo: {angle}")
        print(f"Distancia: {distance}")
        print(f"obstacle_avoidance_strategy: {obstacle_avoidance_strategy}")
        print("---------------------------------")

