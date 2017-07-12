cp request/our.plan backup/our.plan$1
cp output backup/output$1

echo 'clean container_list.txt'
> container_list.txt

echo 'clean output'
> output

echo 'kill mosquitto_sub'
killall -9 mosquitto_sub
