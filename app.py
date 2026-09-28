import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import os


# -----------------------------
# Generate Safe Output Filename
# -----------------------------
def get_safe_filename(file_path):
    base, extension = os.path.splitext(file_path)

    new_path = base + "_decrypted" + extension
    counter = 1

    while os.path.exists(new_path):
        new_path = base + f"_decrypted_{counter}" + extension
        counter += 1

    return new_path


# -----------------------------
# Generate AES-256 Key
# -----------------------------
def generate_key(password, salt):
    return PBKDF2(
        password,
        salt,
        dkLen=32,
        count=100000,
        hmac_hash_module=SHA256
    )


# -----------------------------
# Select File
# -----------------------------
def browse_file():
    file_path = filedialog.askopenfilename(
        title="Select File"
    )

    if file_path:
        selected_file.set(file_path)
        status_text.set("File selected. Ready to encrypt or decrypt.")
        output_text.set("")


# -----------------------------
# Encrypt File
# -----------------------------
def encrypt_file():

    file_path = selected_file.get()
    password = password_entry.get()

    if not file_path:
        messagebox.showwarning(
            "No File",
            "Please select a file first."
        )
        return

    if not password:
        messagebox.showwarning(
            "No Password",
            "Please enter a password."
        )
        return

    if len(password) < 8:
        messagebox.showwarning(
            "Weak Password",
            "Password must contain at least 8 characters."
        )
        return

    try:
        status_text.set("🔄 Encrypting file...")
        window.update()

        # Read file
        with open(file_path, "rb") as file:
            data = file.read()

        # Generate random salt
        salt = get_random_bytes(16)

        # Generate AES-256 key
        key = generate_key(password, salt)

        # AES encryption using EAX mode
        cipher = AES.new(key, AES.MODE_EAX)

        ciphertext, tag = cipher.encrypt_and_digest(data)

        # Output encrypted file
        output_file = file_path + ".enc"

        # Save encrypted file
        with open(output_file, "wb") as file:
            file.write(salt)
            file.write(cipher.nonce)
            file.write(tag)
            file.write(ciphertext)

        status_text.set("✅ File encrypted successfully!")
        output_text.set("Output: " + output_file)

        messagebox.showinfo(
            "Encryption Successful",
            "Your file has been encrypted successfully!"
        )

    except Exception as error:

        status_text.set("❌ Encryption failed!")
        output_text.set("")

        messagebox.showerror(
            "Encryption Error",
            str(error)
        )


# -----------------------------
# Decrypt File
# -----------------------------
def decrypt_file():

    file_path = selected_file.get()
    password = password_entry.get()

    if not file_path:
        messagebox.showwarning(
            "No File",
            "Please select an encrypted file."
        )
        return

    if not password:
        messagebox.showwarning(
            "No Password",
            "Please enter the password."
        )
        return

    if len(password) < 8:
        messagebox.showwarning(
            "Weak Password",
            "Password must contain at least 8 characters."
        )
        return

    try:

        status_text.set("🔄 Decrypting file...")
        window.update()

        # Read encrypted file
        with open(file_path, "rb") as file:
            salt = file.read(16)
            nonce = file.read(16)
            tag = file.read(16)
            ciphertext = file.read()

        # Generate AES key
        key = generate_key(password, salt)

        # AES decryption
        cipher = AES.new(
            key,
            AES.MODE_EAX,
            nonce=nonce
        )

        # Decrypt and verify
        data = cipher.decrypt_and_verify(
            ciphertext,
            tag
        )

        # Generate safe output filename
        if file_path.endswith(".enc"):
            original_file = file_path[:-4]
            output_file = get_safe_filename(original_file)
        else:
            output_file = get_safe_filename(file_path)

        # Save decrypted file
        with open(output_file, "wb") as file:
            file.write(data)

        status_text.set("✅ File decrypted successfully!")
        output_text.set("Output: " + output_file)

        messagebox.showinfo(
            "Decryption Successful",
            "Your file has been decrypted successfully!"
        )

    except ValueError:

        status_text.set("❌ Wrong password or corrupted file!")
        output_text.set("")

        messagebox.showerror(
            "Decryption Failed",
            "Wrong password or corrupted file!"
        )

    except Exception as error:

        status_text.set("❌ Decryption failed!")
        output_text.set("")

        messagebox.showerror(
            "Decryption Error",
            str(error)
        )


# -----------------------------
# Password Strength Checker
# -----------------------------
def check_password_strength(event=None):

    password = password_entry.get()

    score = 0

    if len(password) >= 8:
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(not char.isalnum() for char in password):
        score += 1

    if not password:
        strength_text.set("Password strength: Not entered")

    elif score <= 2:
        strength_text.set("Password strength: 🔴 Weak")

    elif score <= 4:
        strength_text.set("Password strength: 🟡 Medium")

    else:
        strength_text.set("Password strength: 🟢 Strong")


# -----------------------------
# Show / Hide Password
# -----------------------------
def toggle_password():

    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        show_button.config(text="🙈")
    else:
        password_entry.config(show="*")
        show_button.config(text="👁")


# -----------------------------
# Main Window
# -----------------------------
window = tk.Tk()

window.title("Secure File Vault")
window.geometry("700x550")
window.resizable(False, False)


# -----------------------------
# Title
# -----------------------------
title = tk.Label(
    window,
    text="🔐 SECURE FILE VAULT",
    font=("Arial", 24, "bold")
)

title.pack(pady=(25, 5))


subtitle = tk.Label(
    window,
    text="AES-256 File Encryption & Decryption",
    font=("Arial", 12)
)

subtitle.pack(pady=(0, 25))


# -----------------------------
# File Section
# -----------------------------
file_frame = tk.Frame(window)

file_frame.pack(pady=5)

file_label = tk.Label(
    file_frame,
    text="Selected File:",
    font=("Arial", 11, "bold")
)

file_label.pack(anchor="w")


selected_file = tk.StringVar()

file_entry = tk.Entry(
    file_frame,
    textvariable=selected_file,
    width=58,
    font=("Arial", 10)
)

file_entry.pack(side="left", padx=(0, 10))


browse_button = tk.Button(
    file_frame,
    text="📁 Browse",
    command=browse_file,
    width=10
)

browse_button.pack(side="right")


# -----------------------------
# Password Section
# -----------------------------
password_label = tk.Label(
    window,
    text="Password:",
    font=("Arial", 11, "bold")
)

password_label.pack(pady=(25, 5))


password_frame = tk.Frame(window)

password_frame.pack()


password_entry = tk.Entry(
    password_frame,
    width=32,
    show="*",
    font=("Arial", 12)
)

password_entry.pack(side="left")


show_button = tk.Button(
    password_frame,
    text="👁",
    command=toggle_password,
    width=4
)

show_button.pack(side="left", padx=5)


# -----------------------------
# Password Strength
# -----------------------------
strength_text = tk.StringVar()

strength_text.set("Password strength: Not entered")


strength_label = tk.Label(
    window,
    textvariable=strength_text,
    font=("Arial", 10)
)

strength_label.pack(pady=5)


password_entry.bind(
    "<KeyRelease>",
    check_password_strength
)


# -----------------------------
# Action Buttons
# -----------------------------
button_frame = tk.Frame(window)

button_frame.pack(pady=30)


encrypt_button = tk.Button(
    button_frame,
    text="🔒 Encrypt File",
    command=encrypt_file,
    width=20,
    height=2,
    font=("Arial", 11, "bold")
)

encrypt_button.pack(side="left", padx=10)


decrypt_button = tk.Button(
    button_frame,
    text="🔓 Decrypt File",
    command=decrypt_file,
    width=20,
    height=2,
    font=("Arial", 11, "bold")
)

decrypt_button.pack(side="left", padx=10)


# -----------------------------
# Status Section
# -----------------------------
status_title = tk.Label(
    window,
    text="Status",
    font=("Arial", 11, "bold")
)

status_title.pack()


status_text = tk.StringVar()

status_text.set("Ready")


status_label = tk.Label(
    window,
    textvariable=status_text,
    font=("Arial", 11)
)

status_label.pack(pady=5)


# -----------------------------
# Output Section
# -----------------------------
output_text = tk.StringVar()

output_text.set("")


output_label = tk.Label(
    window,
    textvariable=output_text,
    font=("Arial", 9),
    wraplength=650
)

output_label.pack(pady=10)


# -----------------------------
# Start Application
# -----------------------------
window.mainloop()