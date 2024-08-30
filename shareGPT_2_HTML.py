import json
import sys
import os
import base64
import re
import argparse
from typing import Union

def process_json_file(json_file_path: str, output_dir: str, include_image: bool) -> None:
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    img_base64 = ""
    if include_image:
        png_file_path = find_png_file(json_file_path)
        if png_file_path:
            with open(png_file_path, "rb") as image_file:
                img_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        else:
            img_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

    html_content = generate_html_header()

    for entry_number, entry in enumerate(data, 1):
        character_name = entry.get('Character', 'GPT_Assistant')
        html_content += f'<h1><span class="entry-number">Entry {entry_number}</span> Character: {character_name}</h1>\n'
        conversations = entry.get('conversations', [])
        for conversation in conversations:
            source = conversation.get('from')
            conversation_value = process_conversation_text(conversation.get('value', ''))

            if source == 'gpt':
                html_content += generate_gpt_entry(character_name, conversation_value, img_base64, include_image)
            elif source == 'human':
                html_content += generate_human_entry(conversation_value)
            elif source == 'system':
                html_content += generate_system_entry(conversation_value)

    html_content += "</body></html>"

    base_name = os.path.splitext(os.path.basename(json_file_path))[0]
    html_file_path = os.path.join(output_dir, f"{base_name}.html")
    with open(html_file_path, 'w') as html_file:
        html_file.write(html_content)
    print(f"HTML file created: {html_file_path}")

def find_png_file(json_file_path: str) -> Union[str, None]:
    try:
        directory = os.path.dirname(json_file_path)
        png_file = next((file for file in os.listdir(directory) if file.endswith('.png')), None)
        if png_file:
            return os.path.join(directory, png_file)
    except Exception:
        pass

    try:
        current_directory = os.getcwd()
        png_file = next((file for file in os.listdir(current_directory) if file.endswith('.png')), None)
        if png_file:
            return os.path.join(current_directory, png_file)
    except Exception:
        pass

    return None

def generate_html_header() -> str:
    return """
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
            .system-entry { background-color: #d4f799; color: black; }
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

def process_conversation_text(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<span class="bold-green">\1</span>', text)
    text = text.replace('\n', '</p><p>')
    text = re.sub(r'```(.*?)```', r'<pre>\1</pre>', text, flags=re.DOTALL)
    text = re.sub(r'\[([^\]]+)\]\((http[^\)]+)\)', r'<a href="\2">\1</a>', text)
    return text

def generate_gpt_entry(character_name: str, conversation_value: str, img_base64: str, include_image: bool) -> str:
    image_tag = f'<img src="data:image/png;base64,{img_base64}" alt="Character Image" class="character-image" />' if include_image else ''
    return f"""
    <div class="conversation-entry gpt-entry">
        <h2>{character_name}:</h2>
        {image_tag}
        <p>{conversation_value}</p>
    </div>
    """

def generate_human_entry(conversation_value: str) -> str:
    return f"""
    <div class="conversation-entry human-entry">
        <h2>You:</h2>
        <p>{conversation_value}</p>
    </div>
    """

def generate_system_entry(conversation_value: str) -> str:
    return f"""
    <div class="conversation-entry system-entry">
        <h2>System:</h2>
        <p>{conversation_value}</p>
    </div>
    """

def process_input(input_path: str, include_image: bool) -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if os.path.isfile(input_path):
        output_dir = script_dir
        process_json_file(input_path, output_dir, include_image)
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
                    process_json_file(json_file_path, file_output_dir, include_image)
    else:
        print(f"Error: {input_path} is not a valid file or directory")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert JSON files to HTML with optional image embedding.")
    parser.add_argument("input_path", help="Path to JSON file or directory containing JSON files")
    parser.add_argument("-n", "--no-image", action="store_true", help="Do not embed images in the output")
    args = parser.parse_args()

    process_input(args.input_path, not args.no_image)
