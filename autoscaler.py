import docker
import os
import time

# Create a docker client:
client = docker.from_env()
services_autoscale = []

def log(str):
    print("LOG: " + str)

def do_scale(service, number):
    os.system("docker service scale {}={}".format(service.attrs['Spec']['Name'], number))

def get_services_for_autoscaling():
    for service in client.services.list():
        labels = service.attrs['Spec']['Labels']
        if not 'as88.autoscale' in labels.keys():
            log("Skipping {} since no as88.autoscale label is defined".format(service))
            continue

        min = labels['as88.autoscale.min'] if 'as88.autoscale.min' in labels.keys() else 1
        max = labels['as88.autoscale.max'] if 'as88.autoscale.max' in labels.keys() else 2

        services_autoscale.push({'service': service, 'min': min, 'max': max, 'current': len(service.tasks())})

get_services_for_autoscaling()
print(services_autoscale)
print(services_autoscale[1])