import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re

def parse_custom_markup(text, output_format):
    lines = text.splitlines()
    result = []
    in_code = False

    def convert_line(line):
        if line.startswith("# "): return f"<h1>{line[2:]}</h1>" if output_format == "html" else f"# {line[2:]}"
        if line.startswith("## "): return f"<h2>{line[3:]}</h2>" if output_format == "html" else f"## {line[3:]}"
        if line.startswith("### "): return f"<h3>{line[4:]}</h3>" if output_format == "html" else f"### {line[4:]}"
        if line.startswith("* "): return f"<li>{line[2:]}</li>" if output_format == "html" else f"- {line[2:]}"
        if line.strip().startswith("```"): return "<pre><code>" if output_format == "html" else "```"
        if "|" in line and not in_code:
            cells = [cell.strip() for cell in line.split("|")]
            if output_format == "html":
                return "<tr>" + "".join(f"<td>{c}</td>" for c in cells if c) + "</tr>"
            else:
                return "| " + " | ".join(cells) + " |"
        line = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>" if output_format == "html" else r"**\1**", line)
        line = re.sub(r"\*(.*?)\*", r"<em>\1</em>" if output_format == "html" else r"*\1*", line)
        return line

    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            if in_code:
                result.append("</code></pre>" if output_format == "html" else "```")
                in_code = False
            else:
                result.append("<pre><code>" if output_format == "html" else "```")
                in_code = True
            continue

        if output_format == "html" and "|" in line and not in_code:
            if not result or not result[-1].startswith("<table>"):
                result.append("<table>")
            result.append(convert_line(line))
            if i + 1 >= len(lines) or "|" not in lines[i + 1]:
                result.append("</table>")
        else:
            result.append(convert_line(line))

    return "\n".join(result)

class MarkupPreviewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Markup Previewer")

        self.format_var = tk.StringVar(value="markdown")

        # Buttons and options
        tk.Button(root, text="Load File", command=self.load_file).pack(pady=5)
        tk.OptionMenu(root, self.format_var, "markdown", "html").pack()
        tk.Button(root, text="Preview", command=self.preview).pack(pady=5)
        tk.Button(root, text="Save Output", command=self.save_output).pack(pady=5)

        # Text area
        self.output_text = scrolledtext.ScrolledText(root, width=100, height=30)
        self.output_text.pack()

        self.loaded_text = ""

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Markup files", "*.txt *.md *.markup"), ("All files", "*.*")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.loaded_text = f.read()
            messagebox.showinfo("File Loaded", f"Loaded: {path}")

    def preview(self):
        if not self.loaded_text:
            messagebox.showwarning("No file", "Load a file first!")
            return
        fmt = self.format_var.get()
        parsed = parse_custom_markup(self.loaded_text, fmt)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, parsed)

    def save_output(self):
        if not self.loaded_text:
            messagebox.showwarning("No content", "Nothing to save.")
            return
        output = self.output_text.get("1.0", tk.END).strip()
        if not output:
            messagebox.showwarning("No output", "Preview first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All files", "*.*")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(output)
            messagebox.showinfo("Saved", f"Output saved to {path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkupPreviewer(root)
    root.mainloop()
