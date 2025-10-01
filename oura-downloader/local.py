import json
import copy
from pathlib import Path

DOC_ID_KEY = 'document_id'


def inject_payload(target_file, payload):
    """
    Attempt to update a file on disk with the given payload, making a new file otherwise

    :param target_file: Path to (potentially extant) .json file on disk to inject the payload into
    :param payload: the payload to be injected, identified by a unique document id
    """

    # If any data already exists, load it first as a reference
    if Path(target_file).exists():
        with open(target_file) as json_file:
            contents = json.load(json_file)
    else:
        contents = []

    payload_id = payload[DOC_ID_KEY]

    # Determine if this payload needs to be appended or replace an existing payload
    placement_loc = None
    for idx, doc in enumerate(contents):
        this_id = doc[DOC_ID_KEY]
        if payload_id == this_id:
            placement_loc = idx
            break

    # Insert this payload into the appropriate location into the file contents
    if placement_loc is None:
        contents.append(payload)
    else:
        contents[placement_loc] = payload

    # Write the updated file contents to the file
    with open(target_file, 'w') as json_file:
        json_file.write(contents)