# Install Cezzis Platform

## Setup the platform
Apply the argo cd application

``` shell
kubectl apply -f https://raw.githubusercontent.com/mtnvencenzo/cezzis-platform-ops/refs/heads/main/.iac/argocd/cezzis-platform-ops.yaml
```

### Integrate with azure container registry to pull images
Run this command to give the namespace the ability to pull images from ACR

```
kubectl create secret docker-registry acr-pull-secret \
  --docker-server=acrveceusgloshared001.azurecr.io \
  --docker-username=acrveceusgloshared001 \
  --docker-password=$ACR_ACCESS_KEY \
  -n cezzis
```

### Integrate with azure service principal credentials
Run this command to give the namespace the ability to pull images from ACR

```
kubectl create secret generic azure-sp-credentials \
  --namespace cezzis \
  --from-literal=client-id="${AZURE_CEZZIS_ONPREM_APPREG_CLIENTID}" \
  --from-literal=client-secret="${AZURE_CEZZIS_ONPREM_APPREG_SECRET}"
```

## Install Cezzi Applications

### cezzis.com bootstrapper

``` shell
kubectl apply -f https://raw.githubusercontent.com/mtnvencenzo/cezzis-com-local-bootstrapper/refs/heads/main/.iac/argocd/cezzis-com-local-boostrapper.yaml
kubectl apply -f https://raw.githubusercontent.com/mtnvencenzo/cezzis-com-local-bootstrapper/refs/heads/main/.iac/argocd/image-updater.yaml
```


## Troubleshooting

### Clearing a stuck argocd application from deleting
This is typically due to stuck finalizers.

``` shell
kubectl patch application/<appname> --type json --patch='[ { "op": "remove", "path": "/metadata/finalizers" } ]' -n argocd
```



