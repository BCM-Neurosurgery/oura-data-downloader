import toml
from listener import fetch_all_webhooks, fetch_patient_metadata, remove_old_webhooks
from oura import fetch_by_webhook
from local import inject_payload


# Load the config we should use for this run
try:
    with open("config.toml") as f:
        config = toml.load(f)
except FileNotFoundError:
    print('Could not find config.toml! Did you create a custom config.toml for your deployment?')
    print('Exiting...')
    exit(1)
ssh_config = config["listener-ssh"]

# Get the most recent authentication and webhook data from the listener server
auth_data = fetch_patient_metadata(ssh_config, config["token_path"], config["map_path"])
listener_webhooks = fetch_all_webhooks(ssh_config, config["webhook_path"])

success_files = []
failed_files = []

# For each retrieved webhook, endeavor to fetch the relevant data from the Oura API, and save that data locally
for fullpath, patient, modality, filename, payload in listener_webhooks:
    try:
        new_data = fetch_by_webhook(payload, auth_data)
        path = config['output_path_format'].format(
            {'patient': patient, 'date': filename, 'modality': modality}
        )
        inject_payload(path, new_data)
    except Exception as e:
        failed_files.append([fullpath])
        print(e)
    else:
        success_files.append(fullpath)

# Remove all the webhooks that we correctly fetched data for, to avoid re-querying the same data
remove_old_webhooks(ssh_config, success_files)