import asyncio
import asyncssh
import yaml

async def scp_blackbox(user_info, config):
    try:
        async with asyncssh.connect(hostname=user_info['ip'], username=user_info['username'], password=config['SSH_PASSWORD']) as conn:
            local_path = f"{config['LOCAL_PATH']}/{user_info['username']}_blackbox.csv"
            await asyncssh.scp((conn, config['BLACKBOX_PATH']), local_path)
            print(f"Blackbox.csv copied from {user_info['username']} successfully.")

    except (OSError, asyncssh.Error) as e:
        print(f"Failed to copy from {user_info['username']}: {e}")

async def main():
    with open("./configs.yaml", "r") as f:
        config = yaml.safe_load(f)

    tasks = [scp_blackbox(user_info, config) for user_info in config['SSH_USERNAMES']]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
