# Before deploying
make sure this step is followed

Take note of the arn of secrets manager that was provisioned together with the RDS in the output step "Get RDS secrets arn"

Update the arn value in test-app/helm/appcharts/templates/externalsecrets.yaml

        DATABASE_URL: >- # to update with dbname connection details

          postgresql://dbadmin:{{.password}}@<connection details>:5432/postgresdb

  dataFrom: # to update with secrets manager arn

    - extract:

        key: <rds_arn> #to update with secrets arn after terraform provisioned the db

# To trigger the pipeline
add a trailing "#" in any of the terraform file

git add .

git commit -m "update"

git push

Triggering the pipeline will deploy the fastapi application and monitoring into AWS EKS. more details of the steps is covered in the documentation

# Test app
From AWS console or kubectl get ingress to see the DNS name of the load balancer

Open a browser and go to this link to monitor webhook updates https://webhook.site/#!/view/ebfb63af-9a95-4c79-9560-18ad320f08be/445dad5d-94bb-41b8-b3ba-0f229e8a64ee/1

## API calls
curl -X POST "http://<Load balancer DNS>/items?name=test"

curl -X GET "http://<Load balancer DNS>/items"

curl -X PUT "http://<Load balancer DNS>/items/1?name=updated"

curl -X DELETE "http://<Load balancer DNS>/items/1"


you should be able to see the records as you enter these curl commands

Go back to the webhook page on your browser and you should see the POST requests



# Test grafana dashboard
## Get IP address of the NLB
This value was extracted from the Get IP of Network Load balancer step

## Update host file 
Update local hostfile under C:\Windows\System32\drivers\etc\hosts add in a record for "<IP addr> grafana-dashboard.com"

## Get grafana password for log in page
This value was extracted from the Get Grafana password step

## Open browser enter URL
http://grafana-dashboard.com

log in to console
username: admin
password: <from above step>

# Test prometheus alerts
## set up port forwarding to prometheus
kubectl port-forward -n monitoring svc/kube-prom-kube-prometheus-prometheus 9090:9090

## Open browser enter URL
http://localhost:9090

Go to Alerts tab, scroll to fastapi.rules and there you can see the prometheus rules threshold set
