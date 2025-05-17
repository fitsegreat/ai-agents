from google import genai
from google.genai import types
import os
import dotenv
# Load environment variables from .env file
dotenv.load_dotenv()

# Define the function declaration for the model
weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}

# Define a function that the model can call to control smart lights
set_light_values_declaration = {
    "name": "set_light_values",
    "description": "Sets the brightness and color temperature of a light.",
    "parameters": {
        "type": "object",
        "properties": {
            "brightness": {
                "type": "integer",
                "description": "Light level from 0 to 100. Zero is off and 100 is full brightness",
            },
            "color_temp": {
                "type": "string",
                "enum": ["daylight", "cool", "warm"],
                "description": "Color temperature of the light fixture, which can be `daylight`, `cool` or `warm`.",
            },
        },
        "required": ["brightness", "color_temp"],
    },
}

# This is the actual function that would be called based on the model's suggestion
def set_light_values(brightness: int, color_temp: str) -> dict[str, int | str]:
    """Set the brightness and color temperature of a room light. (mock API).

    Args:
        brightness: Light level from 0 to 100. Zero is off and 100 is full brightness
        color_temp: Color temperature of the light fixture, which can be `daylight`, `cool` or `warm`.

    Returns:
        A dictionary containing the set brightness and color temperature.
    """
    return {"brightness": brightness, "colorTemperature": color_temp}


def main():
	# Configure the client and tools
	client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
	tools = types.Tool(function_declarations=[set_light_values_declaration])
	config = types.GenerateContentConfig(tools=[tools])

	# Define user prompt
	contents = [
		types.Content(
			role="user", parts=[types.Part(text="Turn the lights down to a romantic level")]
		)
	]

	# Send request with function declarations
	response = client.models.generate_content(
		model="gemini-2.0-flash",
		contents=contents,
		config=config,
	)

	# Extract tool call details
	tool_call = response.candidates[0].content.parts[0].function_call

	if tool_call.name == "set_light_values":
			result = set_light_values(**tool_call.args)
			print(f"Function execution result: {result}")

	# Create a function response part
	function_response_part = types.Part.from_function_response(
			name=tool_call.name,
			response={"result": result},
	)

	# Append function call and result of the function execution to contents
	contents.append(types.Content(role="model", parts=[types.Part(function_call=tool_call)])) # Append the model's function call message
	contents.append(types.Content(role="user", parts=[function_response_part])) # Append the function response

	final_response = client.models.generate_content(
			model="gemini-2.0-flash",
			config=config,
			contents=contents,
	)

	print(final_response.text)


if __name__ == "__main__":
	main()
