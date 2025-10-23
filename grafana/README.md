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

3. Configure Thanos as our datasource

 - login to grafana console
 - go to "Connections" --> "Data sources"
 - on the left press on "Add new data source"
 - choose Prometheus
 - in the url enter "https://thanos-querier.openshift-monitoring.svc.cluster.local:9091"
 - mark "Skip TLS certificate validation"
 - add HTTP headers
   Header: Authorization Value: Bearer <token>
 - press "Save & test" and pray

4. Configure Loki as our datasource
   
