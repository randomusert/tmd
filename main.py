import argparse
import re
import sys

def parse_custom_markup_to_html(text):
    lines = text.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False

    for line in lines:
        stripped = line.strip()

        if stripped == "```":
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            in_code_block = not in_code_block
            html_lines.append("<pre><code>" if in_code_block else "</code></pre>")
            continue

        if in_code_block:
            html_lines.append(line)
            continue

        # Unordered list
        if stripped.startswith("* "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{stripped[2:]}</li>")
            continue
        elif in_list:
            html_lines.append("</ul>")
            in_list = False

        # Headings
        if line.startswith("## "):
            html_lines.append(f"<h2>{line[3:].strip()}</h2>")
        elif line.startswith("# "):
            html_lines.append(f"<h1>{line[2:].strip()}</h1>")
        else:
            # Inline formatting
            line = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line)
            line = re.sub(r"//(.*?)//", r"<em>\1</em>", line)
            line = re.sub(r"\[\[(.*?)\|(.*?)\]\]", r'<a href="\2">\1</a>', line)
            line = re.sub(r"!\[(.*?)\|(.*?)\]", r'<img src="\2" alt="\1"/>', line)
            html_lines.append(f"<p>{line}</p>")

    if in_list:
        html_lines.append("</ul>")

    return '\n'.join(html_lines)

def parse_custom_markup_to_md(text):
    lines = text.split('\n')
    md_lines = []
    in_code_block = False

    for line in lines:
        stripped = line.strip()

        if stripped == "```":
            in_code_block = not in_code_block
            md_lines.append("```")
            continue

        if in_code_block:
            md_lines.append(line)
            continue

        # Headings
        if line.startswith("## "):
            md_lines.append(f"## {line[3:].strip()}")
        elif line.startswith("# "):
            md_lines.append(f"# {line[2:].strip()}")
        # List
        elif stripped.startswith("* "):
            md_lines.append(f"- {stripped[2:]}")
        else:
            line = re.sub(r"\*\*(.*?)\*\*", r"**\1**", line)
            line = re.sub(r"//(.*?)//", r"*\1*", line)
            line = re.sub(r"\[\[(.*?)\|(.*?)\]\]", r'[\1](\2)', line)
            line = re.sub(r"!\[(.*?)\|(.*?)\]", r'![\1](\2)', line)
            md_lines.append(line)

    return '\n'.join(md_lines)

def main():
    parser = argparse.ArgumentParser(description="Custom markup converter")
    parser.add_argument("input", help="Path to input file")
    parser.add_argument("--format", choices=["html", "markdown"], default="html", help="Output format")
    parser.add_argument("--output", help="Path to output file (optional)")

    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if args.format == "html":
        result = parse_custom_markup_to_html(content)
    else:
        result = parse_custom_markup_to_md(content)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Written to {args.output}")
    else:
        print(result)

if __name__ == "__main__":
    main()
