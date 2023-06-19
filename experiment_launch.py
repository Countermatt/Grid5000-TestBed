import logging
import enoslib as en
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

en.init_logging(level=logging.INFO)
en.check()

#Change to your Grid5000 user
nb_node = 5
arguments = 20  # nb_second
network = en.G5kNetworkConf(type="prod", roles=["experiment_network"], site="nancy")

conf = (
    en.G5kConf.from_settings(job_name="Louvain-job-1", walltime="0:00:50")
    .add_network_conf(network)
    .add_machine(roles=["experiment"], cluster="gros", nodes=nb_node-1, primary_network=network)
    .add_machine(roles=["first"], cluster="gros", nodes=1, primary_network=network)
    .finalize()
)

# This will validate the configuration, but not reserve resources yet
provider = en.G5k(conf)
roles, networks = provider.init()

with en.actions(roles=roles["first"]) as p:
    p.shell("/home/mapigaglio/run1.sh " + str(arguments + 10) +" &")

with en.actions(roles=roles["experiment"]) as p:
    p.shell("/home/mapigaglio/run1.sh "  + str(arguments))
#launch script with list of nodes for arguments
#results = en.run_command("/home/mapigaglio/run1.sh "  + str(arguments), roles=roles["first"])
#results = en.run_command("/home/mapigaglio/run2.sh "  + str(arguments), roles=roles["experiments"])

# Release all Grid'5000 resources
provider.destroy()