# coding: utf-8

import sys
import oci
from oci.signer import Signer
from modules.identity import *
from modules.compute import *
from modules.autonomous_db import *
from modules.db_system import *

########## Configuration ####################
# Specify your config file
configfile = '~/.oci/config'

# Specify your profile name
profile = 'orasejapan'

# Set true if using instance principal signing
use_instance_principal = 'TRUE'

# Set top level compartment OCID. Tenancy OCID will be set if null.
top_level_compartment_id = ''

# List compartment names to exclude
excluded_compartments = ['MANAGEMENT', 'CommonResources', 'ManagedCompartmentForPaaS', 'NetworkCompartmentForPaaS', 'SharedObjectCompartment']

# List target regions. All regions will be counted if null.
# target_region_names = ['us-ashburn-1']
target_region_names = []

#############################################

# Default config file and profile
config = oci.config.from_file(configfile, profile)
tenancy_id = config['tenancy']

if use_instance_principal == 'TRUE':
    signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
else:
    signer = Signer(
        tenancy = config['tenancy'],
        user = config['user'],
        fingerprint = config['fingerprint'],
        private_key_file_location = config['key_file'],
        pass_phrase = config['pass_phrase']
    )


print ("\n===========================[ Login check ]=============================")
login(config, signer)

print ("\n==========================[ Target regions ]===========================")
all_regions = get_region_subscription_list(config, signer, tenancy_id)
target_regions=[]
for region in all_regions:
    if (not target_region_names) or (region.region_name in target_region_names):
        target_regions.append(region)
        print (region.region_name)

print ("\n========================[ Target compartments ]========================")
if not top_level_compartment_id:
    top_level_compartment_id = tenancy_id
compartments = get_compartment_list(config, signer, top_level_compartment_id)
target_compartments=[]
for compartment in compartments:
    if compartment.name not in excluded_compartments:
        target_compartments.append(compartment)
        print (compartment.name)

for region in target_regions:
    print ("\n============[ {} ]================".format(region.region_name))

    config["region"] = region.region_name

    change_autonomous_db_license(config, signer, target_compartments)
    stop_compute_instances(config, signer, target_compartments)
    stop_database_systems(config, signer, target_compartments)
    stop_autonomous_dbs(config, signer, target_compartments)

