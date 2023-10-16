import os 
import shutil
import subprocess


# Function to listen for external drive attachment events
def listen_for_drive_events():
    event_script = '''
    tell application "System Events"
        set attachedDisks to name of every disk
    end tell
    '''
    attached_disks = subprocess.check_output(['osascript', '-e', event_script], universal_newlines=True).split()

    print("Buscando os HDs Externos...")
    external_drive_path = None
    flag = True
    while flag:
        new_attached_disks = subprocess.check_output(['osascript', '-e', event_script], universal_newlines=True).split()
        new_disks = list(set(new_attached_disks) - set(attached_disks))

        for disk in new_disks:
            if disk == 'mnt1,' or disk == 'mnt1':
                continue
            else:
                print(f"HD externo conectado: {disk}")
                path = f'/Volumes/{disk}'                        

                total, used, free = shutil.disk_usage(path)
                total_gb = round(total // (2**30))
                used_gb = round(used // (2**30))
                free_gb = round(free // (2**30))
                print(f'\n-----------------------\n')
                print("Total: %d GB" % (total_gb))  
                print("Usado: %d GB" % (used_gb))
                print("Livre: %d GB" % (free_gb))
                print('Todos os arquivos:')
                movs = []
                file_list = []
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_list.append(os.path.join(root, file))
                        if ".mov" in file:
                            movs.append(file)
                            
                
                for file in file_list:
                    print(file)

                print(f'\n\nArquivos em .MOV:')
                for mov in movs:
                    print(mov)
                print(f'\n-----------------------\n')
                print(f"...\nDados gerados com sucesso! Pode ejetar o HD Externo") 

        attached_disks = new_attached_disks
        

listen_for_drive_events()

