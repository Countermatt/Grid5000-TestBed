import logging
import enoslib as en
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

en.init_logging(level=logging.INFO)
en.check()

#Change to your Grid5000 user
nb_node = 180
arguments = 50  # nb_second
nb_cpu_node = 18
network = en.G5kNetworkConf(type="prod", roles=["experiment_network"], site="nancy")
nb_real_node = nb_node//nb_cpu_node if nb_node%nb_cpu_node == 0 else nb_node//nb_cpu_node + 1

print(nb_real_node)
conf = (
    en.G5kConf.from_settings(job_name="Louvain-job-1", walltime="0:03:00")
    .add_network_conf(network)
    #.add_machine(roles=["experiment"], cluster="gros", nodes=nb_node-1, primary_network=network)
    .add_machine(roles=["first"], cluster="gros", nodes=nb_real_node, primary_network=network)
    .finalize()
)

# This will validate the configuration, but not reserve resources yet
provider = en.G5k(conf)
roles, networks = provider.init()
with en.actions(roles=roles["first"]) as p:
    p.shell("/home/mapigaglio/run1.sh " + str(arguments) + " " + str(roles["first"][0].address) + " " + str(roles["first"][-1].address) + " " + str(nb_node - nb_node//nb_cpu_node) + " " + str(nb_cpu_node))

#with en.actions(roles=roles["experiment"]) as p:
#    p.shell("/home/mapigaglio/run1.sh "  + str(arguments))
#launch script with list of nodes for arguments
#results = en.run_command("/home/mapigaglio/run1.sh "  + str(arguments), roles=roles["first"])
#results = en.run_command("/home/mapigaglio/run2.sh "  + str(arguments), roles=roles["experiments"])

# Release all Grid'5000 resources
provider.destroy()