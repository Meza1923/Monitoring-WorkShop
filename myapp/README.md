<h1>Monitoring workshop</h1>


<h2>Building Image</h2>

1. Our examaple python code is in metrics_exporter.py

Components:

metrics_exporter.py - contain the code of our example application
requirements.txt    - contain list of our python moudls
Containerfile       - our instructions file for the image

1. Build the image and push it to the registry

```
cd image/
podman build . -t my-app:v1
podman tag my-app:v1 harbor-harbor.apps.cluster-tkbfg.dynamic.redhatworkshops.io/workshop/<username>-my-app:v1
podman push harbor-harbor.apps.cluster-tkbfg.dynamic.redhatworkshops.io/workshop/<username>-my-app:v1
```

2. Deploy our deployment, svc and route

```
cd ../
oc apply -f deployment.yaml
oc apply -f service.yaml
oc apply -f route.yaml
```

3. Now we will add ServiceMonitor object in order to allow Prometheus to monitor my application
   
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

4. check if our service is being monitor

- login to openshift console
- go to Observe --> Targets
- filter source to only User
- validate the status is Up

<img width="1586" height="270" alt="image" src="https://github.com/user-attachments/assets/474a53c7-83d6-45b8-b661-2268e10210d4" />

5. Create Prometheus Role in order to get notify when something went wrong
   In this case the alert will be firing if the number of the users that connected to the application has cross 100.

- Create PrometheusRole
```
oc create -f prometheusrole.yaml
```
