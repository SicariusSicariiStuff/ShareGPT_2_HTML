import json
import sys
import os
import base64
import re
from typing import Union

def find_png_file(json_file_path: str) -> str:
    try:
        directory = os.path.dirname(json_file_path)
        png_file = next((file for file in os.listdir(directory) if file.endswith('.png')), None)

        if png_file:
            return os.path.join(directory, png_file)

    except Exception as e:
        print(f"PNG embedded...")

    try:
        current_directory = os.getcwd()
        png_file = next((file for file in os.listdir(current_directory) if file.endswith('.png')), None)

        if png_file:
            return os.path.join(current_directory, png_file)

    except Exception as e:
        print(f"PNG embedded...")

    return None

def process_json_file(json_file_path: str, output_dir: str) -> None:
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    png_file_path = find_png_file(json_file_path)

    if png_file_path:
        with open(png_file_path, "rb") as image_file:
            img_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        img_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }
            .bold-green { font-weight: bold; color: darkgreen; }
            .character-image { width: 3%; float: left; margin-right: 10px; min-width: 20px; }
            .conversation-entry { margin-bottom: 20px; overflow: hidden; }
            .gpt-entry, .human-entry, .system-entry { padding: 10px; border-radius: 5px; }
            .gpt-entry { background-color: #f0f0f0; }
            .human-entry { background-color: #e6f3ff; }
            .system-entry { background-color: #d4f799; color: black; }  <!-- system background -->
            h1 { border-bottom: 1px solid #ddd; padding-bottom: 10px; }
            h2 { margin-top: 0; }
            .entry-number { background-color: #90EE90; padding: 5px 10px; border-radius: 5px; }
            pre { background-color: #d3d3d3; padding: 10px; border: 1px solid #aaa; border-radius: 5px; white-space: pre-wrap; }
            p { margin-bottom: 15px; }
            strong { font-weight: bold; }
        </style>
    </head>
    <body>
    """

    for entry_number, entry in enumerate(data, 1):
        character_name = entry.get('Character', 'GPT_Assistant')
        html_content += f'<h1><span class="entry-number">Entry {entry_number}</span> Character: {character_name}</h1>\n'
        conversations = entry.get('conversations', [])
        for conversation in conversations:
            source = conversation.get('from')
            conversation_value = conversation.get('value', '')

            # Replace **text** with bold text
            conversation_value = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', conversation_value)

            # Replace *text* with bold dark green text
            conversation_value = re.sub(r'\*(.*?)\*', r'<span class="bold-green">\1</span>', conversation_value)

            # Replace \n with visible paragraph separation
            conversation_value = conversation_value.replace('\n', '</p><p>')

            # Replace ```code``` with <pre>code</pre>
            conversation_value = re.sub(r'```(.*?)```', r'<pre>\1</pre>', conversation_value, flags=re.DOTALL)

            # Replace [link](http://link_address) with <a href="http://link_address">link</a>
            conversation_value = re.sub(r'\[([^\]]+)\]\((http[^\)]+)\)', r'<a href="\2">\1</a>', conversation_value)

            if source == 'gpt':
                html_content += f"""
                <div class="conversation-entry gpt-entry">
                    <h2>{character_name}:</h2>
                    <img src="data:image/png;base64,{img_base64}" alt="Character Image" class="character-image" />
                    <p>{conversation_value}</p>
                </div>
                """
            elif source == 'human':
                html_content += f"""
                <div class="conversation-entry human-entry">
                    <h2>You:</h2>
                    <p>{conversation_value}</p>
                </div>
                """
            elif source == 'system':
                html_content += f"""
                <div class="conversation-entry system-entry">
                    <h2>System:</h2>
                    <p>{conversation_value}</p>
                </div>
                """

    html_content += "</body></html>"

    base_name = os.path.splitext(os.path.basename(json_file_path))[0]
    html_file_path = os.path.join(output_dir, f"{base_name}.html")
    with open(html_file_path, 'w') as html_file:
        html_file.write(html_content)
    print(f"HTML file created: {html_file_path}")

def process_input(input_path: str) -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if os.path.isfile(input_path):
        output_dir = script_dir
        process_json_file(input_path, output_dir)
    elif os.path.isdir(input_path):
        dir_name = os.path.basename(os.path.normpath(input_path))
        output_dir = os.path.join(script_dir, f"{dir_name}_HTML_EXPORT")
        os.makedirs(output_dir, exist_ok=True)
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.endswith('.json'):
                    json_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(root, input_path)
                    file_output_dir = os.path.join(output_dir, relative_path)
                    os.makedirs(file_output_dir, exist_ok=True)
                    process_json_file(json_file_path, file_output_dir)
    else:
        print(f"Error: {input_path} is not a valid file or directory")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <json_file_or_directory_path>")
        sys.exit(1)
    input_path = sys.argv[1]
    process_input(input_path)
