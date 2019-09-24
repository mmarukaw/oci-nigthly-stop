import oci

resource_name = 'compute instances'

def stop_compute_instances(config, signer, compartments):
    target_resources = []

    print("Listing all {}... (* is marked for stop)".format(resource_name))
    for compartment in compartments:
        # print("  compartment: {}".format(compartment.name))
        resources = _get_resource_list(config, signer, compartment.id)
        for resource in resources:
            go = 0
            if (resource.lifecycle_state == 'RUNNING'):
                if ('control' in resource.defined_tags) and ('nightly_stop' in resource.defined_tags['control']): 
                    if (resource.defined_tags['control']['nightly_stop'].upper() != 'FALSE'):
                        go = 1
                else:
                    go = 1

            if (go == 1):
                print("    * {} ({}) in {}".format(resource.display_name, resource.lifecycle_state, compartment.name))
                target_resources.append(resource)
            else:
                print("      {} ({}) in {}".format(resource.display_name, resource.lifecycle_state, compartment.name))

    print('\nStopping * marked {}...'.format(resource_name))
    for resource in target_resources:
        try:
            response = _resource_action(config, signer, resource.id, 'STOP')
        except oci.exceptions.ServiceError as e:
            print("---------> error. status: {}".format(e))
            pass
        else:
            if response.lifecycle_state == 'STOPPING':
                print("    stop requested: {} ({})".format(response.display_name, response.lifecycle_state))
            else:
                print("---------> error stopping {} ({})".format(response.display_name, response.lifecycle_state))

    print("\nAll {} stopped!".format(resource_name))


def _get_resource_list(config, signer, compartment_id):
    object = oci.core.ComputeClient(config=config, signer=signer)
    resources = oci.pagination.list_call_get_all_results(
        object.list_instances,
        compartment_id
    )
    return resources.data

def _resource_action(config, signer, resource_id, action):
    object = oci.core.ComputeClient(config=config, signer=signer)
    response = object.instance_action(
        resource_id,
        action
    )
    return response.data
