# Cluster Setup

## Setup

EKS

```sh
eksctl create cluster \
  --name ec2-cluster \
  --region us-west-2
```

Minikube

```sh
minikube start --cpus 4 --memory 7962
```

Install Istio

```sh
## from https://istio.io/latest/docs/setup/install/operator/
istioctl operator init
kubectl label namespace default istio-injection=enabled
kubectl apply -f istio.yaml
```

Install sample app

```sh
## from https://istio.io/latest/docs/setup/getting-started/#bookinfo
kubectl apply -f bookinfo/platform/kube/bookinfo.yaml
kubectl apply -f addons # prometheus, jaeger, etc.
```

Install kube cost

```sh
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
kubectl create namespace kubecost
helm install kubecost/cost-analyzer --namespace kubecost --generate-name kubecost --set kubecostToken="some-token"
```