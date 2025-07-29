#!/usr/bin/env python
import json
import time
import sys
import urllib3
import xmlhelpy

# Put the URL and port of the REST API server here.
default_url = "localhost"
default_port = 8080


def check_workflow_state(workflow_id, url, port=8080):
    """Queries the workflow status and returns its 'state' property.

    @return
        One of the following self-explanatory strings:
         - "Ready"
         - "Running"
         - "Needs_interaction"
         - "Cancelling"
         - "Cancelled"
         - "Error"
         - "Finished"
         - "Unknown state"
    """
    http = urllib3.PoolManager()
    workflow = http.request(
        'GET',
        url + ':' + str(port) + '/workflows/' + str(workflow_id),
    )
    if workflow.status != 200:  # 200: "OK"
        print("Workflow status query failed. Returned HTTP response:")
        print("HTTP status code:", workflow.status)
        print("HTTP headers:", workflow.headers)
        print("HTTP content:", workflow.data)
    state = json.loads(workflow.data.decode('utf-8'))['state']
    return state


def get_workflow_interactions(workflow_id, url, port=8080):
    """Queries the interactions of the workflow and returns them.

    @return
        A list of interactions.
    """
    http = urllib3.PoolManager()
    interactions = http.request(
        'GET',
        url + ':' + str(port) + '/workflows/' + str(workflow_id)
        + '/interactions',
    )
    if interactions.status != 200:  # 200: "OK"
        print("Workflow interactions query failed. Returned HTTP response:")
        print("HTTP status code:", interactions.status)
        print("HTTP headers:", interactions.headers)
        print("HTTP content:", interactions.data)
    return json.loads(interactions.data.decode('utf-8'))["interactions"]


@xmlhelpy.command(version='1.0')
@xmlhelpy.argument(
    'file-name',
    default=None,
    param_type=xmlhelpy.String,
    description="Path to the workflow to execute."
)
@xmlhelpy.option(
    'url',
    char='a',
    default=default_url,
    param_type=xmlhelpy.String,
    description="URL of the server hosting the REST API."
)
@xmlhelpy.option(
    'port',
    char='p',
    default=default_port,
    param_type=xmlhelpy.Integer,
    description="Port the REST API is configured to listen on."
)
@xmlhelpy.option(
    'block-on-output',
    char='b',
    default=True,
    param_type=xmlhelpy.Bool,
    description=(
        "When True, each output interaction and the finish of the workflow "
        "execution block the command line until a key is pressed."
    )
)
@xmlhelpy.option(
    'first-check',
    char='c',
    default=5,
    param_type=xmlhelpy.Integer,
    description="Time (in seconds) until the first status update request."
)
@xmlhelpy.option(
    'periodic-checks',
    char='u',
    default=10,
    param_type=xmlhelpy.Integer,
    description="Time (in seconds) betweeen periodic status update requests."
)
@xmlhelpy.option(
    'log-file',
    char='l',
    default=None,
    param_type=xmlhelpy.String,
    description=(
        "Path where the log file of the workflow gets saved afterwards. "
        "Default is printing the log file to the console."
    )
)
def execute_workflow_remotely(
    file_name,
    url,
    port,
    block_on_output,
    first_check,
    periodic_checks,
    log_file
):
    """Start a workflow via REST API and perform interactions."""
    http = urllib3.PoolManager()

    path = file_name
    with open(path, 'r') as f:
        creation = http.request(
            'POST',
            url + ':' + str(port) + '/workflows',
            body=json.dumps({
                # 'engine': 'SequentialPE',
                'workflow': json.load(f),
            }).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        if creation.status != 201:  # 201: "Created"
            print("Workflow creation failed. Returned HTTP response:")
            print("HTTP status code:", creation.status)
            print("HTTP headers:", creation.headers)
            print("HTTP content:", creation.data)
            sys.exit(1)

    workflow_id = json.loads(creation.data.decode('utf-8'))['id']

    time.sleep(first_check)

    while ((state := check_workflow_state(workflow_id, url, port)) not in [
            'Cancelled',
            'Error',
            'Finished',
            'Unknown state'
    ]):
        if state == 'Needs_interaction':
            interactions = get_workflow_interactions(workflow_id, url, port)
            for interaction in interactions:
                if (
                    interaction['value'] is None
                    and
                    interaction['direction'] == 'input'
                ):
                    print("Workflow requires input of type "
                          + interaction['type'] + ". Node description:")
                    print(interaction['description'])
                    try:
                        interaction['default_value']
                        print("Default input value:")
                        print(interaction['default_value'])
                        user_value = (
                            input("Input: ") or interaction['default_value']
                        )
                    except KeyError:
                        user_value = input("Input: ")

                    if interaction['type'] == 'string':
                        pass
                    elif interaction['type'] == 'int':
                        user_value = int(user_value)
                    elif interaction['type'] == 'float':
                        user_value = float(user_value)
                    elif interaction['type'] == 'bool':
                        user_value = bool(user_value)
                    else:
                        raise NotImplementedError(
                            "Type of interaction is not implemented in the "
                            "automatic script. Please interact with the "
                            "REST API directly to perform the interaction."
                        )
                    interaction_data = json.dumps([{
                        'id': interaction['id'],
                        'value': user_value,
                    }]).encode('utf-8')
                    interaction_patch = http.request(
                        'PATCH',
                        url + ':' + str(port) + '/workflows/'
                        + str(workflow_id) + '/input',
                        body=interaction_data,
                        headers={'Content-Type': 'application/json'}
                    )
                    if interaction_patch.status != 200:  # 200: "OK"
                        print("Interaction failed. Returned HTTP response:")
                        print("HTTP status code:", interaction_patch.status)
                        print("HTTP headers:", interaction_patch.headers)
                        print("HTTP content:", interaction_patch.data)
                elif interaction['direction'] == 'output':
                    print("Workflow gave output of type " + interaction['type']
                          + ". Node description:")
                    print(interaction('description'))
                    print("Node value:")
                    print(interaction['value'])
                    if block_on_output:
                        input("Press any key to continue.")
            restart = http.request(
                'PUT',
                url + ':' + str(port) + '/workflows/'
                + str(workflow_id) + '/state'
            )
            if restart.status != 200:  # 200: "OK"
                print("Workflow continuation failed. "
                      "Returned HTTP response:")
                print("HTTP status code:", restart.status)
                print("HTTP headers:", restart.headers)
                print("HTTP content:", restart.data)
        time.sleep(periodic_checks)

    print("Finished workflow execution with status " + state + ".")

    log = http.request(
        'GET',
        url + ':' + str(port) + '/workflows/' + str(workflow_id) + '/log',
    )
    if log_file is None:
        print(log.data)
    else:
        with open(log_file, 'w') as f:
            f.write(log.data)
    if block_on_output:
        input("Press any key to close the window.")


if __name__ == '__main__':
    execute_workflow_remotely()
