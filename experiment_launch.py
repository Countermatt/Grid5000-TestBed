import logging
import enoslib as en

en.init_logging(level=logging.INFO)
en.check()

nb_node = 2
arguments = 5  # nb_second
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
#launch script with list of nodes for arguments
results = en.run_command("/bin/bash" + " ./run1.sh "  + str(arguments), roles=["first"])
for result in results:
    print(result.payload["stdout"])
    
results = en.run_command("/bin/bash" + " ./run2.sh "  + str(arguments), roles=["experiments"])
for result in results:
    print(result.payload["stdout"])

# Release all Grid'5000 resources
provider.destroy()