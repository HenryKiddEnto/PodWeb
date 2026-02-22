import pandas as pd
import json
import ast

# Read the CSV
newdf = pd.read_csv("C:/Users/henry/Documents/Website/pokedata.csv", encoding="ISO-8859-1")

# Enhanced function to parse string representations of dicts AND lists
def parse_string_representation(value):
    if isinstance(value, str):
        value = value.strip()  # Remove any whitespace

        # Check if it's a dictionary: starts with { and ends with }
        if value.startswith('{') and value.endswith('}'):
            try:
                # Try ast.literal_eval for Python-style dicts
                return ast.literal_eval(value)
            except (ValueError, SyntaxError):
                try:
                    # Try json.loads for JSON-style dicts (convert single quotes to double)
                    return json.loads(value.replace("'", '"'))
                except json.JSONDecodeError:
                    return value

        # Check if it's a list: starts with [ and ends with ]
        elif value.startswith('[') and value.endswith(']'):
            try:
                # Try ast.literal_eval for Python-style lists
                return ast.literal_eval(value)
            except (ValueError, SyntaxError):
                try:
                    # Try json.loads for JSON-style lists (convert single quotes to double)
                    return json.loads(value.replace("'", '"'))
                except json.JSONDecodeError:
                    return value

    return value

# Apply the parsing to all string columns
for col in newdf.select_dtypes(include=['object']).columns:
    newdf[col] = newdf[col].apply(parse_string_representation)

# Convert to JSON
datastring = newdf.to_json(orient='index', indent=4)
data = json.loads(datastring)
data = {value["ID"]: value for key, value in data.items()}

# Save to file
with open('C:/Users/henry/Documents/Website/static/json/pokedata.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
