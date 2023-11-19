
import re
from bs4 import BeautifulSoup

def load_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def replace_square_brackets_with_parentheticals(html_content):
    return html_content.replace('[', '(').replace(']', ')')

def convert_to_fountain(html_content):
    html_content = replace_square_brackets_with_parentheticals(html_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    fountain_script = []

    for tag in soup.find_all(True):
        if tag.name == 'h3':  # Scene Headers
            fountain_script.append('. ' + tag.get_text().strip())
        elif tag.name == 'i':  # Stage Directions
            stage_direction = tag.get_text().strip()
            if stage_direction:
                fountain_script.append('[' + stage_direction + ']')
        elif tag.name == 'b':  # Character Names
            character_name = tag.get_text().strip().upper()
            if character_name:
                fountain_script.append(character_name)
        elif tag.name in ['p', 'div']:  # Dialogue and Action
            text = tag.get_text().strip()
            if text:
                fountain_script.append(text)

    return '\n'.join(fountain_script)
