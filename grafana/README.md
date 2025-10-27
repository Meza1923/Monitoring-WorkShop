<h1>Monitroing WorkShop</h1>

<h2>Deploy Grafana</h2>

1. Examine grafana values in garfana-values.yaml file and change the password of the admin username under .adminPassword

```
cd grafana/chart
vim grafana-values.yaml
```
   
2. Install grafana helm repository with our new values

```
helm repo add grafana https://grafana.github.io/helm-charts

helm install my-grafana grafana/grafana -f grafana-values.yaml

oc get pod -n <ns>
```

3. Create route for grafana
```
cd ../
cat route.yaml
# route.yaml
kind: Route
apiVersion: route.openshift.io/v1
metadata:
  name: grafana-<username>
  namespace: <ns>
spec:
  host: <username>.apps.cluster-tkbfg.dynamic.redhatworkshops.io
  path: /
  to:
    kind: Service
    name: my-grafana-<username>
    weight: 100
  port:
    targetPort: service
  tls:
    termination: edge
```

4. Configure Thanos as our datasource

 - login to grafana console
 - go to "Connections" --> "Data sources"
 - on the left press on "Add new data source"
 - choose Prometheus
 - in the url enter "https://thanos-querier.openshift-monitoring.svc.cluster.local:9091"
 - mark "Skip TLS certificate validation"
 - add HTTP headers
   Header: Authorization Value: Bearer <token>
 - press "Save & test" and pray

5. Configure Loki as our datasource
   

6. Building graphes

  - Go to "Dashboards" --> "Add visualization"
  - Select the datasource you have created
  - Create dashboard with the next metrics and add whatever you want
      - cluster:capacity_memory_bytes:sum
      - 
