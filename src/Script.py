import yaml
import subprocess
import os


with open("./configs.yaml", "r") as f:
        config = yaml.safe_load(f)
BLACKBOX_PATH = config['BLACKBOX_PATH']
LOCAL_PATH = config['LOCAL_PATH']
SSH_PASSWORD = config['SSH_PASSWORD']


if os.path.exists(config['LOCAL_PATH']) == False:
    os.makedirs(config['LOCAL_PATH'])

def scp_blackbox(user_info):
    ip = user_info['ip']
    username = user_info['username']
    print(f"Copying blackbox.csv from {user_info['username']}, {user_info['ip']}...")
    cmd = ["sshpass","-p",SSH_PASSWORD,"scp","-O","-o","StrictHostKeyChecking=no",f"{username}@{ip}:{BLACKBOX_PATH}", f'{LOCAL_PATH}']
    try:
        print(cmd)
        result = subprocess.run(args=cmd, check=True)
        print(os.listdir(LOCAL_PATH))
        print(f"Blackbox.csv copied from {user_info['username']} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to copy from {user_info['username']}: {e}")

def main():
    for user_info in config['SSH_USERNAMES']:
        scp_blackbox(user_info) 
    
if __name__ == '__main__':
    main()