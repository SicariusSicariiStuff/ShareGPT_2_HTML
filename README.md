
# ShareGPT to HTML Converter

This is a simple script designed to convert JSON files in the ShareGPT format into easily readable HTML. The goal is to provide an easy, lightweight option for the open-source community to view datasets in a human-friendly way.

## Usage

```
shareGPT_2_HTML.py <json file or a directory with JSON files>
```

## Notes

- If there is a PNG file in the same directory as the JSON file(s), it will be embedded into the HTML output.

## Features

- Displays character names within each conversation.
- Includes conversation ID numbers for easy navigation in large datasets.
- Supports embedding character images directly into the HTML.
- Formats bold text using a markdown-like style (**two asterisks**).
- Translates markdown-like links into clickable HTML links.
- Highlights code blocks using a markdown-like syntax (```like so```).
- Provides clear visual separation between conversations and individual conversation turns.

## Purpose

This script is intentionally kept simple and bare-bones, allowing users to fork and modify it as needed. The hope is to inspire the development of more easy yet useful tools for processing datasets in the future.

## Example:
````
python shareGPT_2_HTML.py Example/
````
