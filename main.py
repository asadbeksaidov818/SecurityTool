import re
import math
import hashlib
import string
import secrets
import pyperclip
import requests
import customtkinter as ctk
from tkinter import messagebox


# ------------------------------
# 1. Password Entropy Calculation
# ------------------------------
def calculate_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[^A-Za-z0-9]", password): charset += 33

    if charset == 0:
        return 0
    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)


# ------------------------------
# 2. Check Breach Database
# ------------------------------
def check_pwned_api(password):
    sha1pwd = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1pwd[:5], sha1pwd[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    res = requests.get(url)

    if res.status_code != 200:
        return "❌ Error checking HIBP API."

    hashes = (line.split(":") for line in res.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return f"⚠️ Found in {count} breaches!"
    return "✅ Not found in known breaches."


# ------------------------------
# 3. Strength Evaluation
# ------------------------------
def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Too short (min 8 characters).")

    if re.search(r"[a-z]", password): score += 1
    else: feedback.append("Add lowercase letters.")
    if re.search(r"[A-Z]", password): score += 1
    else: feedback.append("Add uppercase letters.")
    if re.search(r"[0-9]", password): score += 1
    else: feedback.append("Add numbers.")
    if re.search(r"[^A-Za-z0-9]", password): score += 1
    else: feedback.append("Add symbols (@, #, $, etc.).")

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, feedback, score


# ------------------------------
# 4. GUI Functionality
# ------------------------------
def analyze_password():
    pwd = entry.get()
    if not pwd:
        messagebox.showwarning("Input Error", "Please enter a password!")
        return

    # Strength check
    strength, feedback, score = check_password_strength(pwd)

    # Entropy
    entropy = calculate_entropy(pwd)

    # Breach check
    breach_result = check_pwned_api(pwd)

    # Update GUI labels
    result_strength.configure(text=f"Your password is {strength}")
    result_entropy.configure(text=f"Entropy: {entropy} bits")
    # Update breach message inside styled frame
    if "Found in" in breach_result:
        breach_frame.configure(fg_color="#3B0000")  # dark red
        breach_message.configure(
            text=f"⚠️ Oh no — pwned!\n\nThis password has been seen {breach_result.split(' ')[2]} times before in data breaches!\n\nThis password has previously appeared in a breach and should never be used. If you’ve ever used it anywhere, change it immediately!",
            text_color="red"
        )
    else:
        breach_frame.configure(fg_color="#002B00")  # dark green
        breach_message.configure(
            text="✅ Good news — not found in known breaches.\n\nThis password has not appeared in any public breaches. Still, use unique, strong passwords for every account!",
            text_color="lightgreen"
        )

    # Update progress bar (0–1 scale)
    progress_bar.set(score / 6)

    # Change progress bar color based on strength
    if strength == "Weak":
        progress_bar.configure(progress_color="red")
    elif strength == "Medium":
        progress_bar.configure(progress_color="yellow")
    else:  # Strong
        progress_bar.configure(progress_color="blue")

    # Suggestions
    if feedback:
        result_feedback.configure(text="Suggestions:\n" + "\n".join(feedback))
    else:
        result_feedback.configure(text="Your password is strong")

# ------------------------------
# Strong Password Generator
# ------------------------------
def generate_password(length=16):
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.<>?"
    return ''.join(secrets.choice(all_chars) for _ in range(length))


def on_generate():
    # Get selected length
    length = int(length_var.get())
    pwd = generate_password(length)

    # Show in entry
    password_output.configure(state="normal")
    password_output.delete(0, "end")
    password_output.insert(0, pwd)
    password_output.configure(state="readonly")

    # Analyze generated password with your existing functions
    strength, feedback, score = check_password_strength(pwd)
    entropy = calculate_entropy(pwd)

    gen_strength.configure(text=f"Strength: {strength}")
    gen_entropy.configure(text=f"Entropy: {entropy} bits")

    # Progress bar strength
    gen_progress.set(score / 6)
    if strength == "Weak":
        gen_progress.configure(progress_color="red")
    elif strength == "Medium":
        gen_progress.configure(progress_color="yellow")
    else:
        gen_progress.configure(progress_color="blue")


def copy_to_clipboard():
    pwd = password_output.get()
    if pwd:
        pyperclip.copy(pwd)
        copy_status.configure(text="📋 Password copied!", text_color="lightgreen")
    else:
        copy_status.configure(text="⚠️ No password to copy.", text_color="red")


# ------------------------------
# 5. Build CustomTkinter GUI with Scroll
# ------------------------------
ctk.set_appearance_mode("dark")  # dark mode
ctk.set_default_color_theme("blue")  # accent color

root = ctk.CTk()
root.title("🔐 Password Security Analyzer")
root.geometry("650x600")

# Create scrollable frame
main_frame = ctk.CTkScrollableFrame(root, width=600, height=550)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Title
title = ctk.CTkLabel(main_frame, text="🔐 Password Security Analyzer", font=("Arial", 20, "bold"))
title.pack(pady=20)

# Input
entry = ctk.CTkEntry(main_frame, placeholder_text="Enter your password", show="*", width=300, font=("Arial", 14))
entry.pack(pady=10)

# Analyze Button
btn = ctk.CTkButton(main_frame, text="Analyze", command=analyze_password, width=200, height=40, font=("Arial", 14))
btn.pack(pady=15)

# Progress Bar
progress_label = ctk.CTkLabel(main_frame, text="Password Strength Meter:", font=("Arial", 14))
progress_label.pack(pady=5)

progress_bar = ctk.CTkProgressBar(main_frame, width=400)
progress_bar.set(0)
progress_bar.pack(pady=5)

# Results
result_strength = ctk.CTkLabel(main_frame, text="", font=("Arial", 14))
result_strength.pack(pady=5)
result_entropy = ctk.CTkLabel(main_frame, text="", font=("Arial", 14))
result_entropy.pack(pady=5)

# Breach Check Box (goes inside scrollable frame now!)
breach_frame = ctk.CTkFrame(main_frame, fg_color="#2B0000", corner_radius=10, width=500, height=120)
breach_frame.pack(pady=10, padx=20, fill="x")

breach_title = ctk.CTkLabel(breach_frame, text="Breach Check Result", font=("Arial", 14, "bold"), text_color="white")
breach_title.pack(pady=5)

breach_message = ctk.CTkLabel(breach_frame, text="", font=("Arial", 13), text_color="white", wraplength=480, justify="center")
breach_message.pack(pady=5)

# Feedback
result_feedback = ctk.CTkLabel(main_frame, text="", font=("Arial", 14), justify="left")
result_feedback.pack(pady=15)

# ------------------------------
# Password Generator Section
# ------------------------------
gen_title = ctk.CTkLabel(main_frame, text="🔑 Password Generator", font=("Arial", 18, "bold"))
gen_title.pack(pady=15)

# Dropdown for length
length_var = ctk.StringVar(value="12")
length_label = ctk.CTkLabel(main_frame, text="Select length:")
length_label.pack()
length_dropdown = ctk.CTkOptionMenu(main_frame, values=["12", "16", "20"], variable=length_var)
length_dropdown.pack(pady=5)

# Generate button
gen_button = ctk.CTkButton(main_frame, text="Generate Strong Password", command=on_generate, width=250, height=40)
gen_button.pack(pady=10)

# Output field
password_output = ctk.CTkEntry(main_frame, width=400, font=("Arial", 14), state="readonly")
password_output.pack(pady=5)

# Copy button
copy_button = ctk.CTkButton(main_frame, text="Copy to Clipboard", command=copy_to_clipboard, width=200)
copy_button.pack(pady=5)

copy_status = ctk.CTkLabel(main_frame, text="", font=("Arial", 12))
copy_status.pack(pady=5)

# Entropy + Strength for generated password
gen_strength = ctk.CTkLabel(main_frame, text="", font=("Arial", 14))
gen_strength.pack(pady=5)

gen_entropy = ctk.CTkLabel(main_frame, text="", font=("Arial", 14))
gen_entropy.pack(pady=5)

gen_progress = ctk.CTkProgressBar(main_frame, width=400)
gen_progress.set(0)
gen_progress.pack(pady=10)

root.mainloop()
