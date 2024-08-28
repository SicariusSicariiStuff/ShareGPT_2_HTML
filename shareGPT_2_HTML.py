import json
import sys
import os
import base64
import re

def json_to_html(json_file_path):
    # Read the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Find a PNG file in the directory
    png_file = next((file for file in os.listdir('.') if file.endswith('.png')), None)

    # Convert the PNG file to a base64 string if it exists, otherwise use a placeholder
    if png_file:
        with open(png_file, "rb") as image_file:
            img_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        # Base64 encoded 1x1 pixel transparent PNG
        img_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

    # Prepare the HTML content
    html_content = """
    <html>
    <head>
        <style>
            .bold-green { font-weight: bold; color: darkgreen; }
            .character-image { width: 3%; float: left; margin-right: 5px; min-width: 20px; }
        </style>
    </head>
    <body>
    """

    for entry in data:
        character_name = entry.get('Character', 'GPT_Assistant')
        html_content += f"<h1>Character: {character_name}</h1>\n"
        conversations = entry.get('conversations', [])
        for conversation in conversations:
            if conversation.get('from') in ['gpt', 'human'] and conversation.get('value'):
                # Replace *text* with bold dark green text
                conversation_value = re.sub(r'\*(.*?)\*', r'<span class="bold-green">\1</span>', conversation['value'])

                if conversation['from'] == 'gpt':
                    html_content += f"""
                    <h2>{character_name}:</h2>
                    <div>
                        <img src="data:image/png;base64,{img_base64}" alt="Character Image" class="character-image" />
                        <p>{conversation_value}</p>
                    </div>
                    """
                else:
                    html_content += f"<h2>You:</h2>\n<p>{conversation_value}</p>\n"

    # Close the HTML tags
    html_content += "</body></html>"

    # Get the base name of the JSON file without the extension
    base_name = os.path.splitext(json_file_path)[0]
    # Create the HTML file path
    html_file_path = f"{base_name}.html"
    # Write the HTML content to the file
    with open(html_file_path, 'w') as html_file:
        html_file.write(html_content)
    print(f"HTML file created: {html_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <json_file_path>")
        sys.exit(1)
    json_file_path = sys.argv[1]
    json_to_html(json_file_path)
