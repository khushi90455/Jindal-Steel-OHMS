import re

with open('generate_all_figures.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace short hex color strings like '#888' with '#888888', '#ccc' with '#cccccc', '#555' with '#555555', etc.
def expand_hex(match):
    h = match.group(1)
    expanded = '#' + h[0]*2 + h[1]*2 + h[2]*2
    return f"'{expanded}'"

# Pattern matches '#123' (single quotes)
new_content = re.sub(r"'#([a-fA-F0-9]{3})'", expand_hex, content)

with open('generate_all_figures.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Expanded all short hex colors in generate_all_figures.py!")
