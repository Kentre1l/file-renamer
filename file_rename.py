import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Dark Mode Colors
BG_COLOR = "#1E1E1E"
FG_COLOR = "#FFFFFF"
BTN_COLOR = "#3E8E41"
ENTRY_BG = "#2D2D2D"
ENTRY_FG = "#FFFFFF"
HIGHLIGHT = "#00BFFF"

def find_files(folder, search_term):
    return [os.path.join(folder, f) for f in os.listdir(folder) if search_term.lower() in f.lower()]

def rename_files():
    folder = folder_entry.get()
    search_term = search_entry.get()
    new_name = new_name_entry.get()

    if not os.path.exists(folder):
        messagebox.showerror("Error", "Folder does not exist.")
        return

    if not search_term:
        messagebox.showerror("Error", "Please enter a file name or part of it to search.")
        return

    if not new_name:
        messagebox.showerror("Error", "Please enter a new name for the file(s).")
        return

    files = find_files(folder, search_term)

    if not files:
        messagebox.showerror("Error", f"No files found matching '{search_term}' in '{folder}'.")
        return

    preview_area.config(state=tk.NORMAL)
    preview_area.delete(1.0, tk.END)

    if len(files) == 1:
        old_path = files[0]
        _, ext = os.path.splitext(old_path)
        new_path = os.path.join(folder, f"{new_name}{ext}")
        preview_area.insert(tk.END, f"{os.path.basename(old_path)} → {os.path.basename(new_path)}\n")
        files = [(old_path, new_path)]
    else:
        # Multiple files: append _1, _2, etc.
        files = [(f, os.path.join(folder, f"{new_name}_{i+1}{os.path.splitext(f)[1]}")) for i, f in enumerate(files)]
        preview_area.insert(tk.END, "\n".join([f"{os.path.basename(old)} → {os.path.basename(new)}" for old, new in files]) + "\n")

    preview_area.config(state=tk.DISABLED)

    confirm = messagebox.askyesno("Confirm Rename", f"Rename {len(files)} file(s)?")

    if confirm:
        for old_path, new_path in files:
            try:
                os.rename(old_path, new_path)
            except Exception as e:
                messagebox.showerror("Error", f"Error renaming '{old_path}': {e}")
                return

        messagebox.showinfo("Success", f"Successfully renamed {len(files)} file(s).")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

# GUI Setup
root = tk.Tk()
root.title("File Renamer - Dark Mode")
root.geometry("600x400")
root.configure(bg=BG_COLOR)

# Styling
font_main = ("Arial", 12)
font_label = ("Arial", 10, "bold")

# Folder Selection
tk.Label(root, text="📂 Folder:", fg=FG_COLOR, bg=BG_COLOR, font=font_label).grid(row=0, column=0, padx=10, pady=5, sticky="w")
folder_entry = tk.Entry(root, width=40, bg=ENTRY_BG, fg=ENTRY_FG, font=font_main, insertbackground=FG_COLOR)
folder_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_folder, bg=BTN_COLOR, fg=FG_COLOR, font=font_main).grid(row=0, column=2, padx=10, pady=5)

# Search Term
tk.Label(root, text="🔎 Search for:", fg=FG_COLOR, bg=BG_COLOR, font=font_label).grid(row=1, column=0, padx=10, pady=5, sticky="w")
search_entry = tk.Entry(root, width=40, bg=ENTRY_BG, fg=ENTRY_FG, font=font_main, insertbackground=FG_COLOR)
search_entry.grid(row=1, column=1, padx=10, pady=5)

# New Name
tk.Label(root, text="📝 New Name:", fg=FG_COLOR, bg=BG_COLOR, font=font_label).grid(row=2, column=0, padx=10, pady=5, sticky="w")
new_name_entry = tk.Entry(root, width=40, bg=ENTRY_BG, fg=ENTRY_FG, font=font_main, insertbackground=FG_COLOR)
new_name_entry.grid(row=2, column=1, padx=10, pady=5)

# Preview Area
tk.Label(root, text="📜 Preview:", fg=HIGHLIGHT, bg=BG_COLOR, font=font_label).grid(row=3, column=0, padx=10, pady=5, sticky="w")
preview_area = scrolledtext.ScrolledText(root, width=50, height=5, bg=ENTRY_BG, fg=ENTRY_FG, font=font_main, wrap=tk.WORD)
preview_area.grid(row=3, column=1, padx=10, pady=5, columnspan=2)
preview_area.config(state=tk.DISABLED)

# Rename Button
tk.Button(root, text="🔄 Rename Files", command=rename_files, bg=BTN_COLOR, fg=FG_COLOR, font=font_main).grid(row=4, column=1, pady=15)

root.mainloop()
