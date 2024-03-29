import itertools
import tkinter as tk
from tkinter import filedialog, messagebox

def generate_wordlist(characters, min_length, max_length):
    wordlist = set()
    for length in range(min_length, max_length + 1):
        for combination in itertools.product(characters, repeat=length):
            wordlist.add(''.join(combination))
    return wordlist

def save_wordlist(wordlist, filename, file_format):
    if file_format == "txt":
        with open(filename + ".txt", 'w') as file:
            for word in wordlist:
                file.write(word + '\n')
    else:
        messagebox.showinfo("Wordlist Generator", "Selected format is not supported.")

def generate_wordlist_from_gui():
    custom_words = custom_words_entry.get().split()
    custom_special_characters = custom_special_chars_entry.get()
    characters = "abcdefghijklmnopqrstuvwxyz"

    if cap_check_var.get():
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if special_check_var.get():
        characters += "!@#$%^&*()_+-/.,<`~>:""|}{"
        characters += custom_special_characters
    if digits_check_var.get():
        characters += "0123456789"

    min_length_str = min_length_entry.get()
    max_length_str = max_length_entry.get()
    filename = filename_entry.get()
    file_format = format_choice_var.get()

    try:
        min_length = int(min_length_str)
        max_length = int(max_length_str)
    except ValueError:
        messagebox.showerror("Error", "Minimum and maximum lengths must be integers.")
        return

    if min_length <= 0 or max_length <= 0:
        messagebox.showerror("Error", "Minimum and maximum lengths must be positive integers.")
        return

    if min_length > max_length:
        messagebox.showerror("Error", "Minimum length cannot be greater than maximum length.")
        return

    if max_length > 14:
        messagebox.showerror("Error", "Maximum length cannot exceed 14 characters.")
        return

    if not filename:
        messagebox.showerror("Error", "Filename cannot be empty.")
        return

    with open(filename + ".txt", 'w') as file:
        for length in range(min_length, max_length + 1):
            for combination in itertools.product(characters, repeat=length):
                word = ''.join(combination)
                file.write(word + '\n')

    for word in custom_words:
        with open(filename + ".txt", 'a') as file:
            file.write(word + '\n')
            file.write(word.lower() + '\n')
            file.write(word.upper() + '\n')

    messagebox.showinfo("Wordlist Generator", f"Wordlist generated and saved to {filename}.{file_format}")

def browse_file():
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    filename_entry.delete(0, tk.END)
    filename_entry.insert(0, filename)

# Create GUI
root = tk.Tk()
root.title("Wordlist Generator")

# Custom Words
custom_words_label = tk.Label(root, text="Custom Words (separate by spaces):")
custom_words_label.grid(row=0, column=0, sticky="w")
custom_words_entry = tk.Entry(root)
custom_words_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

# Custom Special Characters
custom_special_chars_label = tk.Label(root, text="Custom Special Characters:")
custom_special_chars_label.grid(row=1, column=0, sticky="w")
custom_special_chars_entry = tk.Entry(root)
custom_special_chars_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

# Character Set
char_set_label = tk.Label(root, text="Character Set:")
char_set_label.grid(row=2, column=0, sticky="w")

# Minimum Length
min_length_label = tk.Label(root, text="Min Length:")
min_length_label.grid(row=3, column=0, sticky="w")
min_length_entry = tk.Entry(root)
min_length_entry.grid(row=3, column=1, padx=5, pady=5)
min_length_entry.insert(0, "6")

# Maximum Length
max_length_label = tk.Label(root, text="Max Length:")
max_length_label.grid(row=4, column=0, sticky="w")
max_length_entry = tk.Entry(root)
max_length_entry.grid(row=4, column=1, padx=5, pady=5)
max_length_entry.insert(0, "8")

# Capital Letters Checkbox
cap_check_var = tk.BooleanVar()
cap_check = tk.Checkbutton(root, text="Include Capital Letters", variable=cap_check_var)
cap_check.grid(row=5, column=0, columnspan=2, sticky="w")

# Special Characters Checkbox
special_check_var = tk.BooleanVar()
special_check = tk.Checkbutton(root, text="Include Special Characters", variable=special_check_var)
special_check.grid(row=6, column=0, columnspan=2, sticky="w")

# Digits Checkbox
digits_check_var = tk.BooleanVar()
digits_check = tk.Checkbutton(root, text="Include Digits", variable=digits_check_var)
digits_check.grid(row=7, column=0, columnspan=2, sticky="w")

# Format choice
format_choice_label = tk.Label(root, text="Choose format:")
format_choice_label.grid(row=8, column=0, sticky="w")
format_choice_var = tk.StringVar(root)
format_choice_var.set(".txt")  # default value
format_choice_menu = tk.OptionMenu(root, format_choice_var, ".txt", ".docx", ".csv", ".xlsx", ".zip")
format_choice_menu.grid(row=8, column=1, sticky="w")

# Filename
filename_label = tk.Label(root, text="Filename:")
filename_label.grid(row=9, column=0, sticky="w")
filename_entry = tk.Entry(root)
filename_entry.grid(row=9, column=1, padx=5, pady=5)
filename_entry.insert(0, "wordlist")

# Browse Button
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=9, column=2, padx=5, pady=5)

# Generate Button
generate_button = tk.Button(root, text="Generate", command=generate_wordlist_from_gui)
generate_button.grid(row=10, column=1, pady=10)

root.mainloop()
