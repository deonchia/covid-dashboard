# covid-dashboard
A simple dashboard to reflect Singapore's Covid-19 Situation. Built on Dash, served by Gunicorn with a MongoDB backend packaged as a helm chart.  

## TL;DR
```
$ helm repo add dc-repo https://deonchia@github.io/covid-dashboard
$ helm repo update
$ helm install release-name dc-repo/db
```  

## Table of Contents
1. [Introduction](https://github.com/deonchia/covid-dashboard/blob/master/README.md#introduction)
2. [Prerequisites](https://github.com/deonchia/covid-dashboard/blob/master/README.md#prerequisites)
3. [Installation](https://github.com/deonchia/covid-dashboard/blob/master/README.md#installing-the-chart)
4. [Accessing the App](https://github.com/deonchia/covid-dashboard/blob/master/README.md#accessing-the-app)
5. [Monitoring MongoDB](https://github.com/deonchia/covid-dashboard/blob/master/README.md#monitoring-mongodb)
6. [Uninstallation](https://github.com/deonchia/covid-dashboard/blob/master/README.md#uninstalling-the-chart)
7. [Parameters](https://github.com/deonchia/covid-dashboard/blob/master/README.md#parameters)
  

## Introduction
This chart bootstaps a Dash app, Gunicorn server and a MongoDB&reg; deployment on a Kubernetes cluster with the Helm package manager.  

## Prerequisites
Ensure that the following prerequisites are fulfilled before proceeding.
* Kubernetes 1.19+
* Helm 3.2.0+
  

## Installing the Chart
To install the chart with the release-name `rel-name`:
```
$ helm install rel-name dc-repo/db
```
> **Note**: This installs the release in the default namespace.  

> **Note**: Once a chart is deployed, it is not possible to apply changes to the MongoDB's access credentials. Please access the application's administrative tool to do so.  

## Accessing the app
Upon installation of the chart, a small printout will display a set of commands to retrieve the endpoint where the Gunicorn is serving at. 

Running the suggested commands will echo the endpoint that you can access 
```
$ helm install rel-name dc-repo/db
NAME: rel-name
LAST DEPLOYED: Fri Mar 18 09:33:47 2022
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
1. Get the application URL by running these commands:
     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
           You can watch the status of by running 'kubectl get --namespace default svc -w rel-name-gunicorn-service'
  export SERVICE_IP=$(kubectl get svc --namespace default rel-name-gunicorn-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  echo http://$SERVICE_IP:8050
```  

## Monitoring MongoDB
Using MongoDB's built-in monitoring, it is possible to monitor the health of the database with the following commands.  

Obtain the password for the MongoDB server:  
`$ kubectl get secrets --namespace default rel-name-mongodb -o jsonpath='{.data.mongodb-root-password}' | base64 --decode`
> AS3dovnm2o

Fire up a shell in the mongodb pod:  
`$ kubectl exec -ti --namespace default rel-name-mongodb-7b786c68d4-q7fz7 -- /bin/bash`

Access the server:  
`$mongo --authenticationDatabase admin -u root -p AS3dovnm2o`
> MongoDB shell Version v4.4.13

You will be prompted to enable the monitoring service with:   
`db.enableFreeMonitoring()`  

and can then access the monitoring page with the URL provided.  

## Uninstalling the Chart
To uninstall/delete the `rel-name` deployment:
```
$ helm delete rel-name
```
This command removes all components (Deployments, Cronjob, Services) related to the Helm chart.  

## Parameters

Below contains the customisable parameters when running the Helm Chart.  
Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`.  

For example;
```
$ helm install rel-name --set replicaCount=10
```

| Name | Description | Value |
| :--- | :--- | :---: |
| replicaCount | Number of dashboard replicas to be created. | 1 |
| labels.frontend | Label for the frontend app (aka deployment.yaml) | "gunicorn" |
| labels.init | Label for the intialisation pod (aka init-db.yaml) | "init-db"
| image.repository | Image to be used in the deployment.yaml | "continuumio/miniconda3" |
| image.pullPolicy | Pull policy for the image in deployment.yaml | "IfNotPresent" |
| image.tag | Image tag in deployment.yaml | "latest" |
| links.pkg | Package of MongoDB tools, required to upload data onto the database | "mongodb-database-tools-ubuntu2004-x86_64-100.5.2" |
| links.mongotools | Link to pull the specified MongoDB tool package | https://fastdl.mongodb.org/tools/db/mongodb-database-tools-ubuntu2004-x86_64-100.5.2.tgz |
| links.datagov | Link to pull data from | https://data.gov.sg/api/action/datastore_search?resource_id=6c14814b-09b7-408e-80c4-db3d393c7c15 | 
| service.frontend.type | Type of Service exposed for Gunicorn | "LoadBalancer" |
| service.frontend.port | Port of Service exposed for Gunicorn | 8050 |
| ingress.enabled | Ingress Service | false |
| resources.limits.cpu | CPU limit for all pods | 2 |
|resources.limits.memory | Memory limit for all pods | 4G | 
| resources.requests.cpu | CPU request for all pods | 1 |
| resources.requests.memory | Memory request for all pods | 2G |  
