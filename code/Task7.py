import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from Task6 import create_graph  # Reuse the graph generation function from Task6


def launch_gui():
    """
    Launch the GUI for visualizing and interacting with the 'Also Likes' graph.
    """
    def open_dot_file():
        """
        Open a .dot file and display its contents in the text box.
        """
        dot_file = askopenfilename(filetypes=[("DOT files", "*.dot"), ("All files", "*.*")])
        if dot_file:
            try:
                with open(dot_file, "r") as file:
                    content = file.read()
                    text_box.delete("1.0", tk.END)
                    text_box.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")

    def generate_graph():
        """
        Generate a graph from the current .dot file contents.
        """
        dot_file = asksaveasfilename(defaultextension=".dot", filetypes=[("DOT files", "*.dot")])
        if not dot_file:
            return

        try:
            with open(dot_file, "w") as file:
                file.write(text_box.get("1.0", tk.END))

            output_file = asksaveasfilename(defaultextension=".ps", filetypes=[("PostScript files", "*.ps")])
            if output_file:
                create_graph(dot_file, output_file)
                messagebox.showinfo("Success", f"Graph created: {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate graph: {e}")

    # Create the main window
    root = tk.Tk()
    root.title("Task 7 - Also Likes Graph GUI")

    # Create a text box for editing/viewing DOT file content
    text_box = tk.Text(root, wrap="word", width=80, height=25)
    text_box.pack(padx=10, pady=10, fill="both", expand=True)

    # Create buttons for file operations
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    open_button = tk.Button(button_frame, text="Open .dot File", command=open_dot_file)
    open_button.pack(side="left", padx=5)

    save_button = tk.Button(button_frame, text="Generate Graph", command=generate_graph)
    save_button.pack(side="left", padx=5)

    close_button = tk.Button(button_frame, text="Close", command=root.destroy)
    close_button.pack(side="left", padx=5)

    # Start the GUI event loop
    root.mainloop()
