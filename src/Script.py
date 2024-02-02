import yaml
import subprocess
import os
from simple_term_menu import TerminalMenu

def scp_blackbox(user_info, LOCAL_PATH, SSH_PASSWORD, BLACKBOX_PATH, MACHINE):
    ip = user_info['ip']
    username = user_info['username']
    print(f"Copying blackbox.csv from {username}, {user_info['ip']}...")
    if MACHINE == "Pi": # Pi
        csv_name = username + '.csv'
        cmd = ["sshpass","-p",SSH_PASSWORD,"scp","-O","-o",
               "StrictHostKeyChecking=no",
               f"pi@{ip}:{BLACKBOX_PATH}",
               f'{os.path.join(LOCAL_PATH,csv_name)}']
    elif MACHINE == "Coral": # Coral
        log_path = os.path.join(LOCAL_PATH,username)
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        cmd = ["sshpass","-p",SSH_PASSWORD,"scp","-r","-O","-o",
               "StrictHostKeyChecking=no",
               f"mendel@{ip}:{BLACKBOX_PATH}",
               f'{log_path}']
    else: # for testing purposes
        log_path = os.path.join(LOCAL_PATH,username)
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        cmd = ["sshpass","-p",SSH_PASSWORD,"scp","-r","-O","-o",
               "StrictHostKeyChecking=no",
               f"davis@{ip}:{BLACKBOX_PATH}",
               f'{log_path}']
    try:
        print(f'Running:{cmd}')
        subprocess.run(args=cmd, check=True)
        print(f"Blackbox.csv copied from {user_info['username']} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to copy from {user_info['username']}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return

def main():
    try:
        with open('./configs.yaml', 'r') as file:
            config = yaml.safe_load(file) 
    except FileNotFoundError:
        config = {}

    LOCAL_PATH = config['LOCAL_PATH']
    SSH_PASSWORD = config['SSH_PASSWORD']

    if os.path.exists(config['LOCAL_PATH']) == False:
        os.makedirs(config['LOCAL_PATH'])

    options = ["Pi", "Coral", "Test"]
    menu = TerminalMenu(options, 
                            accept_keys=["enter"],
                            title="From what machine would you like to copy the blackbox.csv?")
    selection = menu.show()
    if selection == 0:
        MACHINE = "Pi"
        BLACKBOX_PATH = config['BLACKBOX_PATH_PI']
        SSH_PASSWORD = config['SSH_PASSWORD_PI']
    elif selection == 1:
        MACHINE = "Coral"
        BLACKBOX_PATH= config['BLACKBOX_PATH_CORAL']
        SSH_PASSWORD = config['SSH_PASSWORD_CORAL']
    else:
        MACHINE = "Test"
        BLACKBOX_PATH = config['BLACKBOX_PATH']
        SSH_PASSWORD = config['SSH_PASSWORD']
    print(f"Attempt to SCP from {config['SSH_USERNAMES']}...")
    for user_info in config['SSH_USERNAMES']:
        scp_blackbox(user_info, LOCAL_PATH, SSH_PASSWORD, BLACKBOX_PATH, MACHINE) 
    print("All blackbox.csv files copied successfully.")

def get_user_input(prompt):
    """Function to get user input."""
    return input(prompt)

def update_config():
    try:
        with open('./configs.yaml', 'r') as file:
            config = yaml.safe_load(file)
            print("current config: ", config)
    except FileNotFoundError:
        print(os.listdir('./src'))
        print("No config file found. Creating a new one.")
        config = {}

    ssh_usernames = config.get('SSH_USERNAMES', [])

    while True:
        print("\nEnter SSH user and IP details. Leave username empty to proceed.")
        username = get_user_input("Enter username: ")
        if username == "":
            break
        ip = get_user_input("Enter IP address: ")
        
        ssh_usernames.append({'username': username, 'ip': ip})

    config['SSH_USERNAMES'] = ssh_usernames
    with open('./configs.yaml', 'w') as file:
        yaml.dump(config, file, sort_keys=False)
    print("Updated config: ", config)
    print("\nConfig updated and saved to config.yaml")

if __name__ == '__main__':
    update_config()
    main()