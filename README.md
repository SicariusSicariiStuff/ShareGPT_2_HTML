
# ShareGPT to HTML Converter

This is a simple script designed to convert JSON files in the ShareGPT format into easily readable HTML. The goal is to provide an easy, lightweight option for the open-source community to view datasets in a human-friendly way.

## Usage

```
shareGPT_2_HTML.py <json file or a directory with JSON files>
```

## Notes

- If there is a PNG file in the same directory as the JSON file(s), it will be embedded into the HTML output.

## Features

- **Clear Visual Separation:** The script provides a strong visual distinction between GPT and human turns.
- **Custom Character Names:** If the JSON contains a character name, it will replace the default 'GPT_Assistant' naming scheme.
- **Markdown Highlighting:** Markdown text formatted with `**bold**` will be highlighted in the HTML output.
- **Code Box Highlighting:** Code blocks within the JSON are highlighted for better readability.
- **Entry-Based Highlighting:** Each entry is highlighted based on the JSON ID tag.

## Purpose

This script is intentionally kept simple and bare-bones, allowing users to fork and modify it as needed. The hope is to inspire the development of more easy yet useful tools for processing datasets in the future.
````

* Check the example folder for... examples.

python shareGPT_2_HTML.py Example/
