import tkinter as tk
from tkinter import filedialog, ttk
import os
import re

def extract_email_password(text):
    email_pattern = r'(?i)Login:\s*(\S+)'
    password_pattern = r'(?i)Password:\s*(\S+)'
    url_pattern = r'(?i)URL:\s*(https?://\S+)'

    email_match = re.search(email_pattern, text)
    password_match = re.search(password_pattern, text)
    url_match = re.search(url_pattern, text)

    if email_match and password_match and url_match:
        email = email_match.group(1)
        password = password_match.group(1)
        return f"{email}:{password}"
    else:
        return None

def find_email_password_combinations_in_file(file_path, target_url):
    email_password_combinations = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                if target_url in line:
                    login = next(file).strip().split(":")[1].strip() 
                    password = next(file).strip().split(":")[1].strip()
                    email_password_combinations.append(f"{login}:{password}")
    except Exception as e:
        print(f"Hata: {e}")
    return email_password_combinations

def select_folder(event=None):
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_path)

def process_folder():
    folder_path = folder_path_entry.get()
    target_urls = url_entry.get().split(",")
    if folder_path and target_urls:
        all_results = []
        for target_url in target_urls:
            email_password_combinations = []
            for root, dirs, files in os.walk(folder_path):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    if filename.endswith(".txt"):
                        combinations = find_email_password_combinations_in_file(file_path, target_url.strip())
                        email_password_combinations.extend(combinations)

            if email_password_combinations:
                current_dir = os.path.dirname(__file__)
                output_folder = current_dir
                output_file_name = target_url.strip().replace("/", "_").replace(":", "_") + "_Result.txt"
                output_file_path = os.path.join(output_folder, output_file_name)
                with open(output_file_path, 'w', encoding='utf-8') as output:
                    for combo in email_password_combinations:
                        output.write(combo + '\n')
                
                all_results.extend(email_password_combinations)
                result_label.config(text=f"{target_url.strip()} için e-posta:şifre kombinasyonları başarıyla kaydedildi.", foreground="green", font=("Helvetica", 10, "bold"))
            else:
                result_label.config(text=f"{target_url.strip()} için uygun dosya bulunamadı.", foreground="red", font=("Helvetica", 10, "bold"))

        if all_results:
            all_output_file_path = os.path.join(output_folder, "all_results.txt")
            with open(all_output_file_path, 'w', encoding='utf-8') as all_output:
                for combo in all_results:
                    all_output.write(combo + '\n')
            result_label.config(text=f"Tüm kombinasyonlar başarıyla kaydedildi.", foreground="green", font=("Helvetica", 10, "bold"))
    else:
        result_label.config(text="Klasör veya URL seçilmediğinden işlem yapılamadı.", foreground="red", font=("Helvetica", 10, "bold"))

root = tk.Tk()
root.title("")
root.geometry("500x400")
root.resizable(False, False)
root.configure(bg="#2b2b2b")

lunex_label = ttk.Label(root, text="SAHMERAN", foreground="red", background="#2b2b2b", font=("Courier", 24, "bold"))
lunex_label.pack(pady=10)

url_label = ttk.Label(root, text="URL (Birden fazla URL'yi virgülle ayırın):", foreground="yellow", background="#2b2b2b", font=("Helvetica", 10, "bold"))
url_label.pack()

url_entry = ttk.Entry(root, width=50)
url_entry.pack()

folder_label = ttk.Label(root, text="Klasör Seç:", foreground="green", background="#2b2b2b", font=("Helvetica", 10, "bold"))
folder_label.pack()

folder_path_entry = ttk.Entry(root, width=50)
folder_path_entry.pack()

folder_path_entry.bind("<Button-1>", select_folder)

process_button = ttk.Button(root, text="Klasörü İşle", command=process_folder, width=20)
process_button.pack(pady=10)

result_label = ttk.Label(root, text="", foreground="pink", background="#2b2b2b", font=("Helvetica", 10, "bold"), wraplength=480)
result_label.pack()

root.mainloop()
