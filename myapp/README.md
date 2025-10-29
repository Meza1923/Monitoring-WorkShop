<h1>Monitoring workshop</h1>


<h2>Building Image</h2>

1. Our examaple python code is in metrics_exporter.py

Application Components
Our example Python code is in metrics_exporter.py. The relevant files are:

metrics_exporter.py: Contains the code for our example application.
requirements.txt: Lists the required Python modules/dependencies.
Containerfile: The instructions file used to build the container image.

1. Build the image and push it to the registry. (Make sure to replace the registry URL and <username> placeholder)

```
cd image/
podman build . -t my-app:v1
podman tag my-app:v1 harbor-harbor.apps.cluster-tkbfg.dynamic.redhatworkshops.io/workshop/<username>-my-app:v1
podman push harbor-harbor.apps.cluster-tkbfg.dynamic.redhatworkshops.io/workshop/<username>-my-app:v1
```

2. Deploy the application using the Deployment, Service (SVC), and Route definitions.

```
cd ../
oc apply -f deployment.yaml
oc apply -f service.yaml
oc apply -f route.yaml
```

3. Create the ServiceMonitor
 - Now, we will add a ServiceMonitor object to allow Prometheus to scrape metrics from our application.
 - Examine the service.yaml and servicemonitor.yaml definitions:
   
```
cat service.yaml
# service.yaml
kind: Service
apiVersion: v1
metadata:
  name: workshop-app
  namespace: <ns>
  labels:
    app: workshop-app-svc <-- should match 
spec:
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
  selector:
    app: workshop-app


cat servicemonitor.yaml
# servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: workshop-app
  namespace: <ns>
spec:
  selector:
    matchLabels:
      app: workshop-app-svc <-- should match
  endpoints:
  - port: http
    interval: 30s
    path: /metrics
```

4. Check if our application's service is being monitored by Prometheus


- Log in to the OpenShift Console
- Go to Observe --> Targets
- Filter the Source to "User"
- Validate that the target status for workshop-app is "Up".

<img width="1586" height="270" alt="image" src="https://github.com/user-attachments/assets/474a53c7-83d6-45b8-b661-2268e10210d4" />

5. Finally, we will create a PrometheusRule object to define an alert.

- In this case, the alert will fire if the number of users connected to the application exceeds 100.

- Create the PrometheusRule
```
oc create -f prometheusrole.yaml
```

