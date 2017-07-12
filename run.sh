SECONDS=0

# check the label
label_node

# clean the record from the last time
sh clean_record.sh 

# create request plan
(cd ALGO && bash run_testbed.sh)

# start the mqtt to record the data
mosquitto_sub -h 192.168.0.99 -t lab/# > output 2>&1 &
mqtt_record_pid=$!

# deploy the app
python parse_request.py request/our.plan
cp container_list.txt ~/Record/ 

# waiting for pending
for i in {1..60}
do  
  if kubectl get pods | grep -m 1 -E "Pending|ContainerCreating"; then sleep 10 ; fi
done
echo "End waiting..."
bash end_waiting.sh


duration=$SECONDS
echo "=========="
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
echo "=========="

# record the resource usage
(cd ~/Record/ && sh record.sh)

sleep $1

# delete helm release
#delete_helm

# end mqtt
kill $mqtt_record_pid

# end record resource
(cd ~/Record/ && sh stop_record.sh)
