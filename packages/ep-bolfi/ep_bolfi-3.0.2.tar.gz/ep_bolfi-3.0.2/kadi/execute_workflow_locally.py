#!/usr/bin/env python
import json
import time
import os
import xmlhelpy


def check_workflow_state(workflow_id):
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

    with os.popen(
        'process_manager status '
        + str(workflow_id),
        'r'
    ) as p:
        workflow = p.read()
    state = json.loads(workflow)['state']
    return state


def get_workflow_interactions(workflow_id):
    """Queries the interactions of the workflow and returns them.

    @return
        A list of interactions.
    """
    with os.popen(
        'process_manager interactions '
        + str(workflow_id),
        'r'
    ) as p:
        interactions = p.read()
    return json.loads(interactions)["interactions"]


@xmlhelpy.command(version='1.0')
@xmlhelpy.argument(
    'file-name',
    default=None,
    param_type=xmlhelpy.String,
    description="Path to the workflow to execute."
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
    default=1,
    param_type=xmlhelpy.Integer,
    description="Time (in seconds) until the first status update request."
)
@xmlhelpy.option(
    'periodic-checks',
    char='u',
    default=2,
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
def execute_workflow_locally(
    file_name,
    block_on_output,
    first_check,
    periodic_checks,
    log_file
):
    """Start a workflow via shell and perform interactions."""

    path = file_name
    with os.popen(
        'process_manager start '
        + path,
        # + ' -e SequentialPE'
        'r'
    ) as p:
        creation = p.read()

    workflow_id = json.loads(creation)['id']

    time.sleep(first_check)

    while ((state := check_workflow_state(workflow_id)) not in [
            'Cancelled',
            'Error',
            'Finished',
            'Unknown state'
    ]):
        if state == 'Needs_interaction':
            interactions = get_workflow_interactions(workflow_id)
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
                    with os.popen(
                        'process_manager input '
                        + str(workflow_id) + ' ' + str(interaction['id'])
                        + ' ' + str(user_value),
                        'r'
                    ) as p:
                        p.read()
                elif interaction['direction'] == 'output':
                    print("Workflow gave output of type " + interaction['type']
                          + ". Node description:")
                    print(interaction('description'))
                    print("Node value:")
                    print(interaction['value'])
                    if block_on_output:
                        input("Press any key to continue.")
                with os.popen(
                    'process_manager continue '
                    + str(workflow_id),
                    'r'
                ) as p:
                    p.read()
        time.sleep(periodic_checks)

    print("Finished workflow execution with status " + state + ".")

    with os.popen(
        'process_manager log '
        + str(workflow_id),
        'r'
    ) as p:
        log = p.read()
        if log_file is None:
            print(log)
        else:
            with open(log_file, 'w') as f:
                f.write(log)
    if block_on_output:
        input("Press any key to close the window.")


if __name__ == '__main__':
    execute_workflow_locally()
