import json
from pathlib import Path
from paramiko import SSHClient



def read_json_file(sftp, path):
    """Read in the contents of a json file remotely via SSH/SFTP"""
    with sftp.open(path, "r") as f:
        return json.load(f)

def connect_to_server(ssh_config):
    print("Connecting to remote SSH...")

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=ssh_config["hostname"],
                     username=ssh_config["username"],
                     key_filename=ssh_config["key_filename"])
    sftp = ssh.open_sftp()
    return ssh, sftp


def fetch_all_webhooks(ssh_config, webhook_post_path):
    ssh, sftp = connect_to_server(ssh_config)
    try:
        user_dirs = sftp.listdir(webhook_post_path.as_posix())
        for user in user_dirs:
            user_path = Path(webhook_post_path, user)
            modality_dirs = sftp.listdir(user_path.as_posix())
            for modality in modality_dirs:
                modality_path = Path(user_path, modality)
                webhooks_jsons = [f for f
                                  in sftp.listdir(modality_path.as_posix())
                                  if f.endswith(".json")]
                for filename in webhooks_jsons:
                    fullpath = modality_path / filename
                    payload = read_json_file(sftp, modality_path / filename)
                    yield fullpath, user, modality, filename, payload
    finally:
        sftp.close()
        sftp.close()


def fetch_patient_metadata(ssh_config, token_path, map_path):
    ssh, sftp = connect_to_server(ssh_config)
    try:
        tokens = read_json_file(sftp, token_path.as_posix())
        patient_map = read_json_file(sftp, map_path.as_posix())
    finally:
        sftp.close()
        ssh.close()
    return {'tokens': tokens, 'patient_map': patient_map}

def remove_old_webhooks(ssh_config, old_webhooks):
    ssh, sftp = connect_to_server(ssh_config)
    try:
        for webhook in old_webhooks:
            sftp.remove(webhook)
    finally:
        sftp.close()
        ssh.close()


