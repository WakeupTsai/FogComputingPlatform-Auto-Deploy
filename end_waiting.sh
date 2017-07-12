#!/bin/bash

i=0

kubectl get pods | grep -E "Pending|ContainerCreating" |awk -F- '{print $1}' | uniq

kubectl get pods | grep -E "Pending|ContainerCreating" |awk -F- '{print $1}' | uniq | 
{
  while read -r line;
    do
      i=$(( $i + 1 ))
      cat container_list.txt | grep "$line"
      sed -i.bak "/$line-app/d" container_list.txt

      echo "helm del --purge $line"
      helm del --purge $line

      sed -i.bak "/$line/d" deploy_request 
      # do something on $var
    done

  echo "Fail to deploy $i requests."
}
