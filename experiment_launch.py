import logging
import enoslib as en

en.init_logging(level=logging.INFO)
en.check()

nb_node = 10
my_script = "$HOME/test.sh"
network = en.G5kNetworkConf(type="prod", roles=["experiment_network"], site="nancy", walltime="0:01:00")

conf = (
    en.G5kConf.from_settings(job_name="Louvain-job-1")
    .add_network_conf(network)
    .add_machine(
        roles=["experiment"], cluster="grisou", nodes=nb_node, primary_network=network
    )
    #.add_machine(
    #    roles=["control"], cluster="grisou", nodes=1, primary_network=network,
    #)
    .finalize()
)

# This will validate the configuration, but not reserve resources yet
provider = en.G5k(conf)

# Get actual resources
roles, networks = provider.init()
#Job

#get list of all nodes:
nodes = provider.hosts
nodes_arg = ""
for node in nodes:
    nodes_arg += str(node)

#launch script with list of nodes for arguments
results = en.run_command("/bin/bash" + str(my_script) +" "+ str(nodes_arg), roles=["experiments"])

# Release all Grid'5000 resources
provider.destroy()