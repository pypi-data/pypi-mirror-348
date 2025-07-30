import json
import subprocess
import sys
import os
import tempfile

from prettytable import PrettyTable
from termcolor import colored


def is_json(line):
    try:
        json.loads(line)
    except ValueError:
        return False
    return True


command = "kubectl get deployments --all-namespaces -o json"
result = subprocess.run(command, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, universal_newlines=True, shell=True)

if result.returncode != 0:
    print("Error: Unable to connect to the Kubernetes cluster.")
    print("Please check your credentials and ensure kubectl is configured correctly.")
    sys.exit(1)


deployments = json.loads(result.stdout)["items"]

table = PrettyTable()
table.field_names = ["NS", "Name", "Des. Pods", "Avail. Pods", "CPU Req.",
                     "Mem Req.", "CPU Lim.", "Mem Lim.", "Read.", "Start.", "Live."]

for deployment in deployments:
    namespace = deployment["metadata"]["namespace"]
    name = deployment["metadata"]["name"]
    desired_pods = deployment["spec"].get("replicas", 0)
    available_pods = deployment["status"].get("availableReplicas", 0)
    container = deployment["spec"]["template"]["spec"]["containers"][0]
    resources = container["resources"]
    cpu_request = resources["requests"].get(
        "cpu", "N/A") if "requests" in resources else "N/A"
    memory_request = resources["requests"].get(
        "memory", "N/A") if "requests" in resources else "N/A"
    cpu_limit = resources["limits"].get(
        "cpu", "N/A") if "limits" in resources else "N/A"
    memory_limit = resources["limits"].get(
        "memory", "N/A") if "limits" in resources else "N/A"

    probe_types = {
        "readiness": "NONE",
        "startup": "NONE",
        "liveness": "NONE",
    }

    for probe_type in probe_types:
        probe_data = container.get(f"{probe_type}Probe", None)
        if probe_data:
            if "httpGet" in probe_data:
                probe_types[probe_type] = f"HTTP {probe_data['httpGet']['path']}"
            elif "tcpSocket" in probe_data:
                probe_types[probe_type] = "TCP"
            elif "exec" in probe_data:
                probe_types[probe_type] = "Exec"

    if desired_pods == available_pods:
        color = "green"
    elif int(available_pods) > 0:
        color = "yellow"
    else:
        color = "red"

    row = [
        colored(namespace, color),
        colored(name, color),
        colored(desired_pods, color),
        colored(available_pods, color),
        colored(cpu_request, color),
        colored(memory_request, color),
        colored(cpu_limit, color),
        colored(memory_limit, color),
        colored(probe_types["readiness"], color),
        colored(probe_types["startup"], color),
        colored(probe_types["liveness"], color),
    ]
    table.add_row(row)

# Save table to a temporary file
with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    temp_file.write(table.get_string().encode("utf-8"))
    temp_file_name = temp_file.name

# Use less command to display the file with horizontal scrolling
os.system(f"less -R -S {temp_file_name}")

# Remove temporary file after displaying it
os.remove(temp_file_name)
