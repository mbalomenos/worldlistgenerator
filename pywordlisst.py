import itertools
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar

def compute_statistics():
    try:
        min_length = int(min_length_entry.get())
        max_length = int(max_length_entry.get())
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

    custom_words = custom_words_entry.get().replace(',', ' ').split()
    custom_special_characters = custom_special_chars_entry.get()
    characters = "abcdefghijklmnopqrstuvwxyz"

    if cap_check_var.get():
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if special_check_var.get():
        characters += "!@#$%^&*()_+-/.,<`~>:""|}{"
        characters += custom_special_characters
    if digits_check_var.get():
        characters += "0123456789"

    total_combinations = sum(len(characters) ** i for i in range(min_length, max_length + 1))
    total_words = total_combinations + len(custom_words) * 3  # Consider all possible combinations and custom words

    # Estimate file size (assuming average word length of 8 characters and newline character)
    avg_word_length = 8
    estimated_file_size = total_words * (avg_word_length + 1)

    messagebox.showinfo("Statistics", f"Total Words to be Generated: {total_words}\nEstimated File Size: {estimated_file_size} bytes")

def preview_wordlist():
    try:
        min_length = int(min_length_entry.get())
        max_length = int(max_length_entry.get())
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

    custom_words = custom_words_entry.get().replace(',', ' ').split()
    custom_special_characters = custom_special_chars_entry.get()
    characters = "abcdefghijklmnopqrstuvwxyz"

    if cap_check_var.get():
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if special_check_var.get():
        characters += "!@#$%^&*()_+-/.,<`~>:""|}{"
        characters += custom_special_characters
    if digits_check_var.get():
        characters += "0123456789"

    total_combinations = sum(len(characters) ** i for i in range(min_length, max_length + 1))
    total_words = total_combinations + len(custom_words) * 3  # Consider all possible combinations and custom words

    # Estimate file size (assuming average word length of 8 characters and newline character)
    avg_word_length = 8
    estimated_file_size = total_words * (avg_word_length + 1)

    messagebox.showinfo("Preview", f"Total Words to be Generated: {total_words}\nEstimated File Size: {estimated_file_size} bytes")

def generate_wordlist_from_gui():
    try:
        min_length = int(min_length_entry.get())
        max_length = int(max_length_entry.get())
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

    filename = filename_entry.get()
    if not filename:
        messagebox.showerror("Error", "Filename cannot be empty.")
        return

    custom_words = custom_words_entry.get().replace(',', ' ').split()
    custom_special_characters = custom_special_chars_entry.get()
    characters = "abcdefghijklmnopqrstuvwxyz"

    if cap_check_var.get():
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if special_check_var.get():
        characters += "!@#$%^&*()_+-/.,<`~>:""|}{"
        characters += custom_special_characters
    if digits_check_var.get():
        characters += "0123456789"

    # Open the file
    try:
        with open(f"{filename}.{format_choice_var.get()}", 'w') as file:
            # Generate and write the wordlist
            total_combinations = sum(len(characters) ** i for i in range(min_length, max_length + 1))
            progress_step = 100 / total_combinations
            progress = 0
            word_count = 0
            for length in range(min_length, max_length + 1):
                for combination in itertools.product(characters, repeat=length):
                    word = ''.join(combination)
                    if word not in custom_words:
                        file.write(word + '\n')
                        word_count += 1
                        progress += progress_step
                        progress_var.set(progress)
                        word_count_label.config(text=f"Words Generated: {word_count}")
                        root.update_idletasks()

            # Append custom words
            for word in custom_words:
                if min_length <= len(word) <= max_length and word not in custom_words:
                    file.write(word + '\n')
                    word_count += 1
                    progress += progress_step
                    progress_var.set(progress)
                    word_count_label.config(text=f"Words Generated: {word_count}")
                    root.update_idletasks()

                    # Merge, randomize, and write custom words
                    for merged_word in merge_and_randomize(word):
                        if min_length <= len(merged_word) <= max_length:
                            file.write(merged_word + '\n')
                            word_count += 1
                            progress += progress_step
                            progress_var.set(progress)
                            word_count_label.config(text=f"Words Generated: {word_count}")
                            root.update_idletasks()

        messagebox.showinfo("Wordlist Generator", f"Wordlist generated and saved to {filename}.{format_choice_var.get()}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def merge_and_randomize(word):
    merged_words = [word]
    merged_words.extend(''.join(comb) for comb in itertools.combinations(word, 2))
    random.shuffle(merged_words)
    return merged_words

def browse_file():
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    filename_entry.delete(0, tk.END)
    filename_entry.insert(0, filename)

# Create GUI
root = tk.Tk()
root.title("Wordlist Generator")

# Custom Words
custom_words_label = tk.Label(root, text="Custom Words (separate by commas or spaces):")
custom_words_label.grid(row=0, column=0, sticky="w")
custom_words_entry = tk.Entry(root)
custom_words_entry.grid(row=0, column=1, columnspan=2, sticky="we", padx=5, pady=5)

# Custom Special Characters
custom_special_chars_label = tk.Label(root, text="Custom Special Characters:")
custom_special_chars_label.grid(row=1, column=0, sticky="w")
custom_special_chars_entry = tk.Entry(root)
custom_special_chars_entry.grid(row=1, column=1, columnspan=2, sticky="we", padx=5, pady=5)

# Character Set
char_set_label = tk.Label(root, text="Character Set:")
char_set_label.grid(row=2, column=0, sticky="w")

# Minimum Length
min_length_label = tk.Label(root, text="Min Length:")
min_length_label.grid(row=3, column=0, sticky="w")
min_length_entry = tk.Entry(root)
min_length_entry.grid(row=3, column=1, sticky="we", padx=5, pady=5)
min_length_entry.insert(0, "6")

# Maximum Length
max_length_label = tk.Label(root, text="Max Length:")
max_length_label.grid(row=4, column=0, sticky="w")
max_length_entry = tk.Entry(root)
max_length_entry.grid(row=4, column=1, sticky="we", padx=5, pady=5)
max_length_entry.insert(0, "8")

# Capital Letters Checkbox
cap_check_var = tk.BooleanVar()
cap_check = tk.Checkbutton(root, text="Include Capital Letters", variable=cap_check_var)
cap_check.grid(row=5, column=0, columnspan=3, sticky="w")

# Special Characters Checkbox
special_check_var = tk.BooleanVar()
special_check = tk.Checkbutton(root, text="Include Special Characters", variable=special_check_var)
special_check.grid(row=6, column=0, columnspan=3, sticky="w")

# Digits Checkbox
digits_check_var = tk.BooleanVar()
digits_check = tk.Checkbutton(root, text="Include Digits", variable=digits_check_var)
digits_check.grid(row=7, column=0, columnspan=3, sticky="w")

# Format choice
format_choice_label = tk.Label(root, text="Choose format:")
format_choice_label.grid(row=8, column=0, sticky="w")
format_choice_var = tk.StringVar(root)
format_choice_var.set(".txt")  # default value
format_choice_menu = tk.OptionMenu(root, format_choice_var, ".txt", ".docx", ".csv", ".xlsx", ".zip")
format_choice_menu.grid(row=8, column=1, columnspan=2, sticky="we", padx=5, pady=5)

# Filename
filename_label = tk.Label(root, text="Filename:")
filename_label.grid(row=9, column=0, sticky="w")
filename_entry = tk.Entry(root)
filename_entry.grid(row=9, column=1, sticky="we", padx=5, pady=5)
filename_entry.insert(0, "wordlist")

# Browse Button
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=9, column=2, sticky="e", padx=5, pady=5)

# Generate Button
generate_button = tk.Button(root, text="Generate", command=generate_wordlist_from_gui)
generate_button.grid(row=10, column=1, columnspan=2, sticky="we", pady=5)

# Preview Button
preview_button = tk.Button(root, text="Preview", command=preview_wordlist)
preview_button.grid(row=10, column=0, sticky="w", pady=5)

# Statistics Button
statistics_button = tk.Button(root, text="Statistics", command=compute_statistics)
statistics_button.grid(row=11, column=0, sticky="w", pady=5)

# Progress Bar
progress_var = tk.DoubleVar()
progress_bar = Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=12, column=0, columnspan=3, sticky="we", padx=5, pady=5)

# Word Count Label
word_count_label = tk.Label(root, text="Words Generated: 0")
word_count_label.grid(row=13, column=0, columnspan=3, sticky="we", padx=5, pady=5)

root.mainloop()
