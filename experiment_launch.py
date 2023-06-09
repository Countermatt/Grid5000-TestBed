import logging
import enoslib as en
import os
import datetime

def add_time(original_time, hours=0, minutes=0, seconds=0):
    time_delta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    new_time = original_time + time_delta
    return new_time

def convert_seconds_to_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds
dir_path = os.path.dirname(os.path.realpath(__file__))

en.init_logging(level=logging.INFO)
en.check()

#Change to your Grid5000 user
login = "mapigaglio"
nb_node = 1000
arguments = 600  # nb_second

nb_node_per_cpu = nb_node//10

network = en.G5kNetworkConf(type="prod", roles=["experiment_network"], site="nancy")

conf = (
    en.G5kConf.from_settings(job_name="Louvain-job-1", walltime="0:14:00")
    .add_network_conf(network)
    #.add_machine(roles=["experiment"], cluster="gros", nodes=nb_node-1, primary_network=network)
    .add_machine(roles=["first"], cluster="grisou", nodes=10, primary_network=network)
    .finalize()
)

# This will validate the configuration, but not reserve resources yet
provider = en.G5k(conf)
roles, networks = provider.init(force_deploy=True)
roles = en.sync_info(roles, networks)

#Network emulation
netem = en.NetemHTB()
(
    netem.add_constraints(
        src=roles["first"],
        dest=roles["first"],
        delay="70ms",
        rate="1gbit",
        symmetric=True,)
)

netem.deploy()
netem.validate()

with en.actions(roles=roles["first"], on_error_continue=True, background=True) as p:
    p.shell("/home/" + login + "/run1.sh " + str(arguments) + " " + str(roles["first"][0].address) + " " + str(roles["first"][-1].address) + " " + str(nb_node//10 + nb_node%10) + " " + str(nb_node//10))
#with en.actions(roles=roles["experiment"]) as p:
#    p.shell("/home/mapigaglio/run1.sh "  + str(arguments))
#launch script with list of nodes for arguments
#results = en.run_command("/home/mapigaglio/run1.sh "  + str(arguments), roles=roles["first"])
#results = en.run_command("/home/mapigaglio/run2.sh "  + str(arguments), roles=roles["experiments"])

x = datetime.datetime.now()
h,m,s = convert_seconds_to_time(arguments)
print("Begin at: ",x)
print("Expected to finish at: ",add_time(x,h,m,s))

# Release all Grid'5000 resources
#netem.destroy()
#provider.destroy()