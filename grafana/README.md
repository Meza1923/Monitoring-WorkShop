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

helm install <username>-grafana grafana/grafana -f grafana-values.yaml

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

 - Create token for authenticate Thanos
```
   oc create token grafana-sa --duration=31556926s
```
 - Login to grafana console
 - Go to "Connections" --> "Data sources"
 - On the left press on "Add new data source"
 - Choose Prometheus
 - Enter "https://thanos-querier.openshift-monitoring.svc.cluster.local:9091" in url
 - Mark "Skip TLS certificate validation"
 - Add HTTP headers
   Header: Authorization Value: Bearer <token>
 - Press "Save & test" and pray


5. Configure Loki as our datasource

 - Login to grafana console
 - Go to "Connections" --> "Data sources"
 - On the left press on "Add new data source"
 - Choose Loki
 - Enter "https://logging-loki-gateway-http.openshift-logging.svc.cluster.local:8080/api/logs/v1/infrastructure/" in url
 - Add HTTP headers
   Header: Authorization Value: Bearer <token>
 - Press "Save & test" and pray


6. Building graphes

  - Go to "Dashboards" --> "Add visualization"
  - Select the datasource you have created
  - Create dashboard with the next PromQL queris and add whatever you want
    
      - **sum(rate(node_cpu_seconds_total{mode!="idle"}[5m]))** - Aggregates CPU usage across all nodes (excluding idle time) to give total core utilization for the cluster.
      - **node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"} * 100** - Calculates the percentage of available disk space on the root           filesystem (/) for each node.
      - **sum(node_memory_MemAvailable_bytes)** - Sums the total available memory across all nodes as reported by the Node Exporter
      - **sum(kube_pod_status_phase{phase="Pending",namespace="oadp-user10"})** - Counts the total number of pods inside specific ns that are stuck in Pending.
      - **sum(rate(coredns_dns_responses_total{rcode!="NOERROR"}[5m]))** - Calculates the rate of non-successful DNS responses over the last 5 minutes. High values indicate         cluster network resolution issues.
        
  - PromQL Cheat Sheet - **https://promlabs.com/promql-cheat-sheet/**
