import sys
import json
import os

application = {0:['SCALE'],1:['YOLO'],2:['AUDIO']}

with open('device.json') as data_file:
    device = json.load(data_file)

def helm_record(request_name):
    f = open('deploy_request', 'a')
    f.write(request_name+"\n")  # python will convert \n to os.linesep
    f.close()

def container_record(op,reqIndex,app,qos):
    #print op
    f = open('container_list.txt', 'a')
    for i in range(len(op)):
        insert_data = "%s@%s,req%s-app%s-op%s-%s,%s,%s,%s,%s,%s,%s,%s" % \
            (device['device'][op[i][3]]['username'],device['device'][op[i][3]]['ip'], \
            str(reqIndex), str(app), str(i), device['device'][op[i][3]]['hostname'], \
            device['device'][op[i][3]]['iface'], \
            str(8000+int(reqIndex)*10+i), \
            device['device'][op[i][3]]['type'], \
            application[app][0],
            str(i),
            str(qos),
            str(reqIndex)
            )
        f.write(insert_data+"\n")  # python will convert \n to os.linesep
    f.close()

def parseReq(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    request=[]
    reqIndex = 0
    app = 0
    qos = 0
    for i in range(len(content)):
        line = [x.strip() for x in content[i].split(',')]
        if line[0][0]=='#':
            continue

        if line[0] != reqIndex and len(request)!=0:
            deployApp(request,reqIndex,app,qos)

            del request[:]
            reqIndex = line[0]
            app = int(line[1])
            qos = 1/float(line[2])
            request.append(line[3:])

        elif line[0] != reqIndex and len(request)==0:
            reqIndex = line[0]
            app = int(line[1])
            qos = 1/float(line[2])
            request.append(line[3:])

        elif line[0] == reqIndex:
            request.append(line[3:])
    deployApp(request,reqIndex,app,qos)



def deployApp(op,reqIndex,app,qos):
    print "Request: " + str(reqIndex)
    print "Application: " + application[app][0]
    print "QoS: " + str(qos)
    #print op

    port_base = 8000 + int(reqIndex)*10
    helm_name = "req"+str(reqIndex)

    global device
    if app == 0 :

        command='helm install --name %s \
        --set name.request=%s,name.application=%s,period=%s \
        --set mqtt.brokerIP="192.168.0.99",mqtt.topic=iot-1/d/b827ebdf52bd/evt/# \
        --set operator.op0.ip=%s,operator.op0.port=%s,operator.op0.device.type=%s,operator.op0.device.label=%s \
        --set operator.op0.device.hostname=%s,operator.op0.resource.cpu=%s,operator.op0.resource.mem=%s \
        --set operator.op1.ip=%s,operator.op1.port=%s,operator.op1.device.type=%s,operator.op1.device.label=%s \
        --set operator.op1.device.hostname=%s,operator.op1.resource.cpu=%s,operator.op1.resource.mem=%s \
        --set operator.op2.ip=%s,operator.op2.port=%s,operator.op2.device.type=%s,operator.op2.device.label=%s \
        --set operator.op2.device.hostname=%s,operator.op2.resource.cpu=%s,operator.op2.resource.mem=%s \
        --set operator.op3.ip=%s,operator.op3.port=%s,operator.op3.device.type=%s,operator.op3.device.label=%s \
        --set operator.op3.device.hostname=%s,operator.op3.resource.cpu=%s,operator.op3.resource.mem=%s \
        --set operator.op4.ip=%s,operator.op4.port=%s,operator.op4.device.type=%s,operator.op4.device.label=%s \
        --set operator.op4.device.hostname=%s,operator.op4.resource.cpu=%s,operator.op4.resource.mem=%s helmChart/scale/' \
        % (helm_name,reqIndex,app,qos, \
        device['device'][op[0][3]]['ip'], port_base+0, device['device'][op[0][3]]['type'], op[0][3], \
        device['device'][op[0][3]]['hostname'],str(float(op[0][4])*10).split('.')[0],op[0][5].split('.')[0], \
        device['device'][op[1][3]]['ip'], port_base+1, device['device'][op[1][3]]['type'], op[1][3], \
        device['device'][op[1][3]]['hostname'],str(float(op[1][4])*10).split('.')[0],op[1][5].split('.')[0], \
        device['device'][op[2][3]]['ip'], port_base+2, device['device'][op[2][3]]['type'], op[2][3], \
        device['device'][op[2][3]]['hostname'],str(float(op[2][4])*10).split('.')[0],op[2][5].split('.')[0], \
        device['device'][op[3][3]]['ip'], port_base+3, device['device'][op[3][3]]['type'], op[3][3], \
        device['device'][op[3][3]]['hostname'],str(float(op[3][4])*10).split('.')[0],op[3][5].split('.')[0], \
        device['device'][op[4][3]]['ip'], port_base+4, device['device'][op[4][3]]['type'], op[4][3], \
        device['device'][op[4][3]]['hostname'],str(float(op[4][4])*10).split('.')[0],op[4][5].split('.')[0]
        )
        #print "command:"
        os.system(command)
        helm_record(helm_name)

    elif app == 1:
        command='helm install --name %s\
        --set name.request=%s,name.application=%s,period=%s \
        --set mqtt.brokerIP="192.168.0.99", \
        --set operator.op0.ip=%s,operator.op0.port=%s,operator.op0.device.type=%s,operator.op0.device.label=%s \
        --set operator.op0.device.hostname=%s,operator.op0.resource.cpu=%s,operator.op0.resource.mem=%s \
        --set operator.op1.ip=%s,operator.op1.port=%s,operator.op1.device.type=%s,operator.op1.device.label=%s \
        --set operator.op1.device.hostname=%s,operator.op1.resource.cpu=%s,operator.op1.resource.mem=%s \
        --set operator.op2.ip=%s,operator.op2.port=%s,operator.op2.device.type=%s,operator.op2.device.label=%s \
        --set operator.op2.device.hostname=%s,operator.op2.resource.cpu=%s,operator.op2.resource.mem=%s  helmChart/yolo/' \
        % (helm_name,reqIndex,app,qos, \
        device['device'][op[0][3]]['ip'], port_base+0, device['device'][op[0][3]]['type'], op[0][3], \
        device['device'][op[0][3]]['hostname'],str(float(op[0][4])*10).split('.')[0],op[0][5].split('.')[0], \
        device['device'][op[1][3]]['ip'], port_base+1, device['device'][op[1][3]]['type'], op[1][3], \
        device['device'][op[1][3]]['hostname'],str(float(op[1][4])*10).split('.')[0],op[1][5].split('.')[0], \
        device['device'][op[2][3]]['ip'], port_base+2, device['device'][op[2][3]]['type'], op[2][3], \
        device['device'][op[2][3]]['hostname'],str(float(op[2][4])*10).split('.')[0],op[2][5].split('.')[0]
        )
        #print "command:"
        os.system(command)
        helm_record(helm_name)

    elif app == 2:
        command='helm install --name %s\
        --set name.request=%s,name.application=%s,period=%s \
        --set mqtt.brokerIP="192.168.0.99", \
        --set operator.op0.ip=%s,operator.op0.port=%s,operator.op0.device.type=%s,operator.op0.device.label=%s \
        --set operator.op0.device.hostname=%s,operator.op0.resource.cpu=%s,operator.op0.resource.mem=%s \
        --set operator.op1.ip=%s,operator.op1.port=%s,operator.op1.device.type=%s,operator.op1.device.label=%s \
        --set operator.op1.device.hostname=%s,operator.op1.resource.cpu=%s,operator.op1.resource.mem=%s \
        --set operator.op2.ip=%s,operator.op2.port=%s,operator.op2.device.type=%s,operator.op2.device.label=%s \
        --set operator.op2.device.hostname=%s,operator.op2.resource.cpu=%s,operator.op2.resource.mem=%s \
        --set operator.op3.ip=%s,operator.op3.port=%s,operator.op3.device.type=%s,operator.op3.device.label=%s \
        --set operator.op3.device.hostname=%s,operator.op3.resource.cpu=%s,operator.op3.resource.mem=%s \
        --set operator.op4.ip=%s,operator.op4.port=%s,operator.op4.device.type=%s,operator.op4.device.label=%s \
        --set operator.op4.device.hostname=%s,operator.op4.resource.cpu=%s,operator.op4.resource.mem=%s helmChart/audio/' \
        % (helm_name,reqIndex,app,qos, \
        device['device'][op[0][3]]['ip'], port_base+0, device['device'][op[0][3]]['type'], op[0][3], \
        device['device'][op[0][3]]['hostname'],str(float(op[0][4])*10).split('.')[0],op[0][5].split('.')[0], \
        device['device'][op[1][3]]['ip'], port_base+1, device['device'][op[1][3]]['type'], op[1][3], \
        device['device'][op[1][3]]['hostname'],str(float(op[1][4])*10).split('.')[0],op[1][5].split('.')[0], \
        device['device'][op[2][3]]['ip'], port_base+2, device['device'][op[2][3]]['type'], op[2][3], \
        device['device'][op[2][3]]['hostname'],str(float(op[2][4])*10).split('.')[0],op[2][5].split('.')[0], \
        device['device'][op[3][3]]['ip'], port_base+3, device['device'][op[3][3]]['type'], op[3][3], \
        device['device'][op[3][3]]['hostname'],str(float(op[3][4])*10).split('.')[0],op[3][5].split('.')[0], \
        device['device'][op[4][3]]['ip'], port_base+4, device['device'][op[4][3]]['type'], op[4][3], \
        device['device'][op[4][3]]['hostname'],str(float(op[4][4])*10).split('.')[0],op[4][5].split('.')[0]
        )
        #print "command:"
        os.system(command)
        helm_record(helm_name)

    container_record(op,reqIndex,app,qos)



    print "------\n\n"

if __name__ == "__main__":
    #os.system("mosquitto_sub -h 192.168.0.99 -t lab/# > output 2>&1 &")
    parseReq(sys.argv[1])
