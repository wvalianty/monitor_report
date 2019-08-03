#!/usr/bin/env bash

set -o pipefail
set -e

# 每次修改这个名字
export PROVIDER_NAME="python-dingding"
# 每次修改这个名字


#export SSH_PRIVATE_KEY="`cat /home/deploy_manager/.ssh/id_rsa`"
#export GITLAB_USER="deploy_manager"

DATE=`date +%Y%m%d-%H%M`
IMAGE="registry.cn-beijing.aliyuncs.com/zeus-mall/${PROVIDER_NAME}:${DATE}"
#docker build --build-arg  SSH_PRIVATE_KEY="$SSH_PRIVATE_KEY" --build-arg GITLAB_USER="$GITLAB_USER" -t ${IMAGE} .
docker build -t ${IMAGE} .
docker push ${IMAGE}
export KUBECONFIG=/Users/ci/wvalianty/.kube/config.product.monitoring
kubectl get pod
kubectl set image deploy ${PROVIDER_NAME} ${PROVIDER_NAME}=${IMAGE}
