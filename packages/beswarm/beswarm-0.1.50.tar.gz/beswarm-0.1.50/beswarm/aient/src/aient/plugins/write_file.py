from .registry import register_tool

import os

@register_tool()
def write_to_file(path, content, mode='w'):
    """
## write_to_file
Description: Request to write full content to a file at the specified path. If the file exists, it will be overwritten with the provided content. If the file doesn't exist, it will be created. This tool will automatically create any directories needed to write the file.
Parameters:
- path: (required) The path of the file to write to (relative to the current working directory ${args.cwd})
- content: (required) The content to write to the file. ALWAYS provide the COMPLETE intended content of the file, without any truncation or omissions. You MUST include ALL parts of the file, even if they haven't been modified. Do NOT include the line numbers in the content though, just the actual content of the file.
- mode: (optional) The mode to write to the file. Default is 'w'. 'w' for write, 'a' for append.
Usage:
<write_to_file>
<path>File path here</path>
<content>
Your file content here
</content>
<mode>w</mode>
</write_to_file>

Example: Requesting to write to frontend-config.json
<write_to_file>
<path>frontend-config.json</path>
<content>
{
  "apiEndpoint": "https://api.example.com",
  "theme": {
    "primaryColor": "#007bff",
    "secondaryColor": "#6c757d",
    "fontFamily": "Arial, sans-serif"
  },
  "features": {
    "darkMode": true,
    "notifications": true,
    "analytics": false
  },
  "version": "1.0.0"
}
</content>
</write_to_file>
    """
    # 确保目录存在
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)

    if content.startswith("##") and (path.endswith(".md") or path.endswith(".txt")):
        content = "\n\n" + content

    # 写入文件
    with open(path, mode, encoding='utf-8') as file:
        file.write(content)

    return f"已成功写入文件：{path}"