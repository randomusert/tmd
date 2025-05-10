import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from main import parse_custom_markup_to_html, parse_custom_markup_to_md  # Import your parser here

class TmdEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("TMD Editor & Previewer")

        self.filename = None
        self.format_var = tk.StringVar(value="markdown")

        # Editor area (left)
        self.editor = scrolledtext.ScrolledText(root, width=60, height=30)
        self.editor.grid(row=0, column=0, padx=5, pady=5)

        # Preview area (right)
        self.preview = scrolledtext.ScrolledText(root, width=60, height=30, state='disabled')
        self.preview.grid(row=0, column=1, padx=5, pady=5)

        # Buttons
        control_frame = tk.Frame(root)
        control_frame.grid(row=1, column=0, columnspan=2, pady=5)

        tk.Button(control_frame, text="Open .tmd", command=self.load_file).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Save .tmd", command=self.save_file).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Preview", command=self.render_preview).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Export Output", command=self.export_output).pack(side=tk.LEFT, padx=5)
        tk.OptionMenu(control_frame, self.format_var, "markdown", "html").pack(side=tk.LEFT)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("TMD files", "*.tmd"), ("All files", "*.*")])
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, f.read())
                self.filename = path
                messagebox.showinfo("Opened", f"Loaded {os.path.basename(path)}")

    def save_file(self):
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(defaultextension=".tmd", filetypes=[("TMD files", "*.tmd")])
        if self.filename:
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(self.editor.get("1.0", tk.END).strip())
            messagebox.showinfo("Saved", f"Saved to {os.path.basename(self.filename)}")

    def render_preview(self):
        content = self.editor.get("1.0", tk.END).strip()
        if not content:
            return
        fmt = self.format_var.get()
        rendered = parse_custom_markup_to_html(content)
        self.preview.config(state='normal')
        self.preview.delete("1.0", tk.END)
        self.preview.insert(tk.END, rendered)
        self.preview.config(state='disabled')

    def export_output(self):
        content = self.editor.get("1.0", tk.END).strip()
        if not content:
            return
        fmt = "html"
        output = parse_custom_markup_to_html(content)
        ext = ".html" if fmt == "html" else ".md"
        path = filedialog.asksaveasfilename(defaultextension=ext,
                                            filetypes=[("HTML", "*.html")] if fmt == "html" else [("Markdown", "*.md")])
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(output)
            messagebox.showinfo("Exported", f"Saved to {os.path.basename(path)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TmdEditor(root)
    root.mainloop()
