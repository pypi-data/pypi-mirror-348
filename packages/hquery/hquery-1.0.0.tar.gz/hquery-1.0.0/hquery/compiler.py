import re
import base64

def parse_block(lines, index=0):
    html_output = ""
    indent = "  "

    while index < len(lines):
        line = lines[index].strip()

        if line.lower() == "end":
            return html_output, index

        if line.startswith("--"):
            comment_text = line[2:].strip()
            html_output += f"{indent}<!-- {comment_text} -->\n"

        elif re.match(r'CREATE \w+ CONTAINS', line):
            contains_match = re.match(r'CREATE (\w+) CONTAINS(?: "([^"]+)")?(?: WITH \(([^)]+)\))?(?:$|\s*\()?', line)
            if contains_match:
                tag, text, attrs = contains_match.groups()
                attrs_str = ""

                if attrs:
                    attr_pairs = re.findall(r'(\w+)\s*=\s*"([^"]+)"', attrs)
                    for attr_name, attr_value in attr_pairs:
                        attrs_str += f' {attr_name.lower()}="{attr_value}"'

                if line.endswith("("):
                    nested_content, new_index = parse_block(lines, index + 1)
                    html_output += f'{indent}<{tag.lower()}{attrs_str}>\n{nested_content}{indent}</{tag.lower()}>\n'
                    index = new_index
                else:
                    html_output += f'{indent}<{tag.lower()}{attrs_str}>{text or ""}</{tag.lower()}>\n'

        elif re.match(r'CREATE \w+ WITH \(', line):
            with_only_match = re.match(r'CREATE (\w+) WITH \(([^)]+)\)', line)
            if with_only_match:
                tag, attrs = with_only_match.groups()
                attrs_str = ""
                attr_pairs = re.findall(r'(\w+)\s*=\s*"([^"]+)"', attrs)
                for attr_name, attr_value in attr_pairs:
                    attrs_str += f' {attr_name.lower()}="{attr_value}"'
                html_output += f'{indent}<{tag.lower()}{attrs_str}></{tag.lower()}>\n'

        elif line.lower() == "head:":
            nested_content, new_index = parse_block(lines, index + 1)
            html_output += f"<head>\n{nested_content}</head>\n"
            index = new_index

        elif line.lower() == "body:":
            nested_content, new_index = parse_block(lines, index + 1)
            html_output += f"<body>\n{nested_content}</body>\n"
            index = new_index

        index += 1

    return html_output, index

def obfuscate_minify(html):
    return ''.join(html.split())

def obfuscate_hex_entities(html):
    return ''.join(f'&#x{ord(c):x};' for c in html)

def obfuscate_base64(html):
    b64_encoded = base64.b64encode(html.encode('utf-8')).decode('utf-8')
    return f'<script>document.write(atob("{b64_encoded}"));</script>'

def obfuscate_charcode(html):
    charcodes = ','.join(str(ord(c)) for c in html)
    return f'<script>document.write(String.fromCharCode({charcodes}));</script>'

def compiler(content, obfuscate=None):
    lines = [line.rstrip() for line in content.strip().splitlines() if line.strip()]
    html_content, _ = parse_block(lines)
    final_html = f"<html>\n{html_content}</html>"

    if obfuscate == 'minify':
        return obfuscate_minify(final_html)
    elif obfuscate == 'hex':
        return obfuscate_hex_entities(final_html)
    elif obfuscate == 'base64':
        return obfuscate_base64(final_html)
    elif obfuscate == 'charcode':
        return obfuscate_charcode(final_html)
    else:
        return final_html