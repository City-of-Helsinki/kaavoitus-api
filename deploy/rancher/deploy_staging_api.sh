#!/bin/bash


#echo "TODO: fix deployment.yaml env before using this script! There is env that points to testing domain"
#exit 1

if test "$2" == ""; then
	echo "Usage: $0 <version> <test/run>"
	echo "Check image version from Rancher UI or from CLI: kubectl -n xxx get deployment -o wide"
	exit 1
fi



VERSION=$1
RUN=$2
NS="kaavapino-staging"
REGISTRY="127.0.0.1:34522"



TMP=$(mktemp)
echo "Using temporary file $TMP"
cat deployment.yaml | sed 's,${CICD_REGISTRY},'$REGISTRY',g' | sed 's,${CICD_EXECUTION_SEQUENCE}-${CICD_GIT_COMMIT},'$VERSION',g' > $TMP
cat $TMP
KUBECTL="kubectl -n $NS apply -f $TMP"
if test $RUN == "run"; then
	$KUBECTL
else
	echo "Not applying unless 'run' is set from cli"
	echo $KUBECTL
fi
