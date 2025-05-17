import json
import requests

tools = [
      {
        "type": "function",
        "function": {
          "name": "get_weather",
          "description": "Get the current weather for a city and temperature in Celsius",
          "parameters": {
            "type": "object",
            "properties": {
              "city": {
                "type": "string",
                "description": "The location to get the weather for, e.g. Addis Ababa"
              }
            },
            "required": ["city"]
          }
        }
      },
      {
        "type": "function",
        "function": {
          "name": "convert_temperature",
          "description": "Convert temperature between Celsius and Fahrenheit",
          "parameters": {
            "type": "object",
            "properties": {
              "temperature": {
                "type": "number",
                "description": "The temperature to convert"
              },
              "unit": {
                "type": "string",
                "enum": ["C", "F"],
                "description": "The unit of the temperature to convert from"
              },
              "target_unit": {
                "type": "string",
                "enum": ["C", "F"],
                "description": "The unit to convert the temperature to"
              }
            },
            "required": ["temperature", "unit", "target_unit"]
          }
        }
      }
    ]

def generate_response(user_prompt: str, history: list):
  response = requests.post("http://localhost:11434/api/chat", json={
    "model": "qwen3:1.7b",
    "messages": history,
    "stream": False,
    "tools": tools,
  })
  output = response.json()
  if "tool_calls" in output["message"] and len(output["message"]["tool_calls"]) > 0:
    tool_call = output["message"]["tool_calls"][0]
    tool_name = tool_call["function"]["name"]
    tool_args = tool_call["function"]["arguments"]

    tool_result = "No result, invalid tool call."

    if tool_name == "get_weather":
      city = tool_args["city"]
      tool_result = json.dumps(get_weather(city))
    elif tool_name == "convert_temperature":
      temperature = tool_args["temperature"]
      unit = tool_args["unit"]
      target_unit = tool_args["target_unit"]
      tool_result = convert_temperature(temperature, unit, target_unit)
    
    history.append({
      "role": "tool",
      "content": f"Calling the {tool_name} function with the argument {tool_args}.\nThe result is: {tool_result}"
    })
    # history.append({"role": "assistant", "content": f"I wanted to call the {tool_name} function with the argument {tool_args}."})
    # history.append({"role": "user", "content": f"""
    #                 My original prompt was: {user_prompt}. 
    #                 You wanted to call the {tool_name} function with the argument {tool_args}.
    #                 The result of the tool call is: {tool_result}"""})
    return generate_response(user_prompt, history)

  return output["message"]["content"]

def get_weather(city: str):
  cities = {
    "Addis Ababa": {
      "temperature": 20,
      "description": "Sunny",
      "humidity": 50,
      "wind_speed": 5
    },
    "New York": {
      "temperature": 15,
      "description": "Cloudy",
      "humidity": 60,
      "wind_speed": 10
    },
    "Los Angeles": {
      "temperature": 25,
      "description": "Sunny",
      "humidity": 40,
      "wind_speed": 3
    },
    "Tokyo": {
      "temperature": 18,
      "description": "Rainy",
      "humidity": 70,
      "wind_speed": 8
    },
    "London": {
      "temperature": 12,
      "description": "Windy",
      "humidity": 65,
      "wind_speed": 12
    },
    "Paris": {
      "temperature": 16,
      "description": "Partly Cloudy",
      "humidity": 55,
      "wind_speed": 7
    },
    "Berlin": {
      "temperature": 14,
      "description": "Overcast",
      "humidity": 75,
      "wind_speed": 6
    },
  }

  if city not in cities:
    return f"Sorry, I don't have weather information for {city}."
  return cities[city]

def convert_temperature(temperature: float, unit: str, target_unit: str):
  print(f"Converting {temperature}°{unit} to {target_unit}")
  if unit == "C" and target_unit == "F":
    return (temperature * 9/5) + 32
  elif unit == "F" and target_unit == "C":
    return (temperature - 32) * 5/9
  else:
    return temperature

def main():
  history = []

  while True:
    user_input = input("Your prompt: ")
    if user_input.lower() == "exit":
      break
    history.append({"role": "user", "content": user_input})
    output = generate_response(user_input, history)

    print(output)

if __name__ == "__main__":
  main()