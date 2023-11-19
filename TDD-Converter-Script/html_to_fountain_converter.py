
import re
from bs4 import BeautifulSoup

def load_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def convert_to_fountain(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    fountain_script = []

    for tag in soup.find_all(True):
        if tag.name == 'h3':  # Scene Headers
            fountain_script.append('. ' + tag.get_text().strip())
        elif tag.name == 'i':  # Stage Directions
            stage_direction = tag.get_text().strip()
            if stage_direction:
                fountain_script.append('[' + stage_direction + ']')
        elif tag.name == 'b':  # Character Names and Dialogue
            character_name = tag.get_text().strip().upper()
            if character_name:
                fountain_script.append(character_name)
                blockquote = tag.find_next('blockquote')
                if blockquote:
                    dialogue = blockquote.get_text().strip()
                    if dialogue:
                        fountain_script.append(dialogue)
    return '\n'.join(fountain_script)

def apply_user_edits(fountain_script):
    # User-specific edits (adding empty lines, hashing, etc.)
    refined_script = []
    for line in fountain_script.split('\n'):
        if line.startswith('. ACT') or line.startswith('. SCENE'):
            refined_script.append('#' + line[2:])
        elif line.startswith('[') and line.endswith(']'):
            refined_script.append('(' + line[1:-1] + ')')
        elif line.isupper():
            refined_script.append('\n' + line)
        else:
            refined_script.append(line)
    return '\n'.join(refined_script)

def remove_duplicates(script):
    script_lines = script.split('\n')
    cleaned_script_lines = []
    skip_next = False
    for i in range(len(script_lines) - 1):
        current_line = script_lines[i]
        next_line = script_lines[i + 1]
        if not skip_next and next_line.startswith('(') and next_line.endswith(')') and current_line == next_line[1:-1]:
            skip_next = True
        else:
            cleaned_script_lines.append(current_line)
            skip_next = False
    if not skip_next:
        cleaned_script_lines.append(script_lines[-1])
    return '\n'.join(cleaned_script_lines)

def add_empty_lines_before_elements(script, elements):
    script_lines = script.split('\n')
    updated_script_lines = []
    for line in script_lines:
        if any(line.startswith(e) for e in elements):
            updated_script_lines.append('')
            updated_script_lines.append(line)
        else:
            updated_script_lines.append(line)
    return '\n'.join(updated_script_lines)

def save_to_fountain_file(script, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(script)

# Usage
# html_file_path = 'path_to_html_file.html'
# fountain_file_path = 'path_to_save_fountain_file.fountain'
# html_content = load_html(html_file_path)
# fountain_script = convert_to_fountain(html_content)
# fountain_script = apply_user_edits(fountain_script)
# fountain_script = remove_duplicates(fountain_script)
# fountain_script = add_empty_lines_before_elements(fountain_script, ['#ACT', '##SCENE', '('])
# save_to_fountain_file(fountain_script, fountain_file_path)
