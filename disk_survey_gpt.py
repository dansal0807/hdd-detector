import os
import shutil
import subprocess
import fsevents
import time

# Function to listen for external drive attachment events
def listen_for_drive_events():
    event_script = '''
    tell application "System Events"
        set attachedDisks to name of every disk
    end tell
    '''
    attached_disks = subprocess.check_output(['osascript', '-e', event_script], universal_newlines=True).split()
    
    print("Buscando os HDs Externos...")

    # Store a list of currently connected drives
    connected_drives = set()

    while True:
        new_attached_disks = subprocess.check_output(['osascript', '-e', event_script], universal_newlines=True).split()
        
        # Detect new drives and ejections
        new_drives = set(new_attached_disks) - connected_drives
        ejected_drives = connected_drives - set(new_attached_disks)

        for disk in new_drives:
            if disk == 'mnt1,' or disk == 'mnt1':
                continue
            else:
                print(f"HD externo conectado: {disk}")
                path = f'/Volumes/{disk}'

                total, used, free = shutil.disk_usage(path)
                total_gb = round(total / (2**30))
                used_gb = round(used / (2**30))
                free_gb = round(free / (2**30))

                print(f'\n-----------------------\n')
                print(f"Total: {total_gb} GB")
                print(f"Usado: {used_gb} GB")
                print(f"Livre: {free_gb} GB")
                print('Todos os arquivos:')
                
                file_list = os.listdir(path)

                for file in file_list:
                    print(file)
                
                print(f'\n\nArquivos em .MOV:')
                movs = [file for file in file_list if file.endswith(".mov")]

                for mov in movs:
                    print(mov)
                
                print(f'\n-----------------------\n')
                print(f"...\nDados gerados com sucesso! Pode ejetar o HD Externo")
        
        for disk in ejected_drives:
            if disk == 'mnt1,' or disk == 'mnt1':
                continue
            else:
                print(f"HD externo ejetado: {disk}")

        connected_drives = set(new_attached_disks)
        time.sleep(2)  # Adjust the interval as needed

if __name__ == "__main__":
    listen_for_drive_events()
