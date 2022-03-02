from os import error
import random
import math
import argparse
from tabulate import tabulate
import statistics
import matplotlib.pyplot as plt
import numpy as np

BUSY=1
IDLE=0
Q_LIMIT=100
errorstatus=False
errormessage=""
next_event_type=num_custs_delayed=num_delays_required=num_events=server_status=None
area_num_in_q=area_server_status=sim_time=time_last_event=total_of_delays=mean_interarrival=mean_service=None
time_arrival=[]
time_next_event=[None]*2
outputfile=open("output1.txt","w")
table=[]
uniform_rv=[]
service_exp_rv=[]
interarrival_exp_rv=[]

def px(x,samples):
    y=[0]*len(x)
    for sample in samples:
        if sample<=x[0]:
            y[0]+=1
        for index,value in enumerate(x[1:]):
            if sample<=value and sample>x[index]:
                y[index+1]+=1
    return y

def fx(x,samples):
    y=[0]*len(x)
    for sample in samples:
        for index,value in enumerate(x):
            if sample<=value:
                y[index]+=1
    return y





def report():
    global outputfile,total_of_delays,num_custs_delayed,area_num_in_q,sim_time,area_server_status,uniform_rv,interarrival_exp_rv,service_exp_rv,mean_service,mean_interarrival
    outputfile.write("Average delay in queue : "+str(total_of_delays/num_custs_delayed)+"\n")
    outputfile.write("Average number in queue : "+str(area_num_in_q / sim_time)+"\n")
    outputfile.write("Server utilization : "+str(area_server_status / sim_time)+"\n")
    outputfile.write("Time simulation ended : "+str(sim_time)+"\n\n\n")
    outputfile.write("Uniform Distribution\n-------------------------\n")
    outputfile.write("Min : "+str(min(uniform_rv))+"\n")
    outputfile.write("Max : "+str(max(uniform_rv))+"\n")
    outputfile.write("Median : "+str(statistics.median(uniform_rv))+"\n\n")
    

    x=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    fig, axis = plt.subplots(2)
    y=px(x,uniform_rv)
    for index,value in enumerate(y):
        y[index]=value/len(uniform_rv)
    outputfile.write("P(x) :\n")
    temptable=[]
    for index,value in enumerate(x):
        temptable.append([x[index],y[index]])
    outputfile.write(tabulate(temptable)+"\n\n")
    axis[0].plot(x,y)
    axis[0].set_title("P(X)")
    axis[0].set_ylim([0,1])
    y=fx(x,uniform_rv)
    for index,value in enumerate(y):
        y[index]=value/len(uniform_rv)
    outputfile.write("F(x) :\n")
    temptable=[]
    for index,value in enumerate(x):
        temptable.append([x[index],y[index]])
    outputfile.write(tabulate(temptable)+"\n\n")
    axis[1].plot(x,y)
    axis[1].set_title("F(X)")
    axis[1].set_ylim([0,1])
    fig.suptitle('Uniform Distribution', fontsize=16)
    plt.show()

    outputfile.write("Exponential Distribution : Interarrival Time\n--------------------------------------------\n")
    outputfile.write("Min : "+str(min(interarrival_exp_rv))+"\n")
    outputfile.write("Max : "+str(max(interarrival_exp_rv))+"\n")
    outputfile.write("Median : "+str(statistics.median(interarrival_exp_rv))+"\n\n\n")

    x=[0.5*mean_interarrival,mean_interarrival,2*mean_interarrival,3*mean_interarrival]
    fig, axis = plt.subplots(2)
    y=px(x,interarrival_exp_rv)
    for index,value in enumerate(y):
        y[index]=value/len(interarrival_exp_rv)
    outputfile.write("P(x) :\n")
    temptable=[]
    for index,value in enumerate(x):
        temptable.append([x[index],y[index]])
    outputfile.write(tabulate(temptable)+"\n\n")
    axis[0].plot(x,y)
    axis[0].set_title("P(X)")
    axis[0].set_ylim([0,1])
    y=fx(x,interarrival_exp_rv)
    for index,value in enumerate(y):
        y[index]=value/len(interarrival_exp_rv)
    outputfile.write("F(x) :\n")
    temptable=[]
    for index,value in enumerate(x):
        temptable.append([x[index],y[index]])
    outputfile.write(tabulate(temptable)+"\n\n")
    axis[1].plot(x,y)
    axis[1].set_title("F(X)")
    axis[1].set_ylim([0,1])
    fig.suptitle('Exponential Distribution : Interarrival Time', fontsize=16)
    plt.show()

    outputfile.write("Exponential Distribution : Service Time\n---------------------------------------\n")
    outputfile.write("Min : "+str(min(service_exp_rv))+"\n")
    outputfile.write("Max : "+str(max(service_exp_rv))+"\n")
    outputfile.write("Median : "+str(statistics.median(service_exp_rv))+"\n\n\n")

    x=[0.5*mean_service,mean_service,2*mean_service,3*mean_service]
    fig, axis = plt.subplots(2)
    y=px(x,service_exp_rv)
    for index,value in enumerate(y):
        y[index]=value/len(service_exp_rv)
    outputfile.write("P(x) :\n")
    temptable=[]
    for index,value in enumerate(x):
        temptable.append([x[index],y[index]])
    outputfile.write(tabulate(temptable)+"\n\n")
    axis[0].plot(x,y)
    axis[0].set_title("P(X)")
    axis[0].set_ylim([0,1])
    y=fx(x,service_exp_rv)
    for index,value in enumerate(y):
        y[index]=value/len(service_exp_rv)
    outputfile.write("F(x) :\n")
    temptable=[]
    for index,value in enumerate(x):
        temptable.append([x[index],y[index]])
    outputfile.write(tabulate(temptable)+"\n\n")
    axis[1].plot(x,y)
    axis[1].set_title("F(X)")
    axis[1].set_ylim([0,1])
    fig.suptitle('Exponential Distribution : Service Time', fontsize=16)
    plt.show()

    

def timing():
    global errormessage,errorstatus,next_event_type,num_events,time_next_event,outputfile,sim_time
    min_time_next_event = float('inf')
    next_event_type = -1
    for i in range(num_events):
        if time_next_event[i]<min_time_next_event:
            min_time_next_event=time_next_event[i]
            next_event_type=i
    if next_event_type<0:
        errormessage="Event list empty at time : "+str(sim_time)+"\n"
        errorstatus=True
        return
    sim_time = min_time_next_event

def update_time_avg_stats():
    global sim_time,time_last_event,area_num_in_q,area_server_status,server_status
    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time
    area_num_in_q += len(time_arrival) * time_since_last_event
    area_server_status += server_status * time_since_last_event

def expon(mean):
    global uniform_rv
    random_number=random.random()
    uniform_rv.append(random_number)
    return -1*mean*math.log(random_number)

def initialize():
    global errormessage,errorstatus,sim_time,server_status,time_last_event,num_custs_delayed,total_of_delays,area_num_in_q,area_server_status,time_next_event,time_arrival,mean_interarrival,uniform_rv,interarrival_exp_rv,service_exp_rv
    time_arrival=[]
    interarrival_exp_rv=[]
    service_exp_rv=[]
    uniform_rv=[]
    sim_time=0.0
    server_status = IDLE
    time_last_event = 0.0
    num_custs_delayed = 0
    total_of_delays = 0.0
    area_num_in_q = 0.0
    area_server_status = 0.0
    temp=expon(mean_interarrival)
    interarrival_exp_rv.append(temp)
    time_next_event[0] = sim_time+temp
    time_next_event[1] = float('inf')
    errorstatus=False
    errormessage=""

def arrive():
    global errormessage,errorstatus,time_next_event,sim_time,mean_interarrival,BUSY,server_status,Q_LIMIT,sim_time,time_arrival,mean_service,num_custs_delayed,outputfile,interarrival_exp_rv,service_exp_rv
    temp=expon(mean_interarrival)
    interarrival_exp_rv.append(temp)
    time_next_event[0]=sim_time+temp
    if server_status==BUSY:
        if(len(time_arrival)+1>Q_LIMIT):
            errormessage="Overflow of the array time_arrival at : "+str(sim_time)+"\n"
            errorstatus=True
            return
        time_arrival.append(sim_time)
    else:
        num_custs_delayed+=1
        server_status=BUSY
        temp=expon(mean_service)
        service_exp_rv.append(temp)
        time_next_event[1]=sim_time+temp

def depart():
    global server_status,IDLE,time_next_event,sim_time,time_arrival,total_of_delays,num_custs_delayed,mean_service,service_exp_rv
    if len(time_arrival)==0:
        server_status=IDLE
        time_next_event[1]=float('inf')
    else:
        delay=sim_time-time_arrival[0]
        total_of_delays+=delay
        num_custs_delayed+=1
        temp=expon(mean_service)
        service_exp_rv.append(temp)
        time_next_event[1]=sim_time+temp
        time_arrival.pop(0)

        
def generate_statistics():
    global mean_service,mean_interarrival,table,outputfile,total_of_delays,num_custs_delayed,area_num_in_q,sim_time,area_server_status
    fraction=[0.5,0.6,0.7,0.8,0.9]
    for k in fraction:
        mean_service=k*mean_interarrival
        initialize()
        while num_custs_delayed<num_delays_required:
            timing()
            update_time_avg_stats()
            if next_event_type==0:
                arrive()
                if errorstatus:
                    break
            elif next_event_type==1:
                depart()
        if not errorstatus:
            table.append([k,total_of_delays/num_custs_delayed,area_num_in_q / sim_time,area_server_status/sim_time,sim_time])
        else:
            table.append([k,errormessage])
    outputfile.write(tabulate(table))

def main():
    parser = argparse.ArgumentParser(description='path to input file')
    parser.add_argument('--i',metavar='input',type=str,help='the path to the input file')
    args = parser.parse_args()
    input_file_path=args.i
    inputfile=open(input_file_path,"r")
    global mean_interarrival,mean_service,num_events,num_delays_required,next_event_type,table,errormessage,outputfile
    mean_interarrival=float(inputfile.readline())
    mean_service=float(inputfile.readline())
    num_delays_required=int(inputfile.readline())
    inputfile.close()
    outputfile.write("Single-server queueing system \n")
    outputfile.write("Mean interarrival time : "+str(mean_interarrival)+"\n")
    outputfile.write("Mean service time : "+str(mean_service)+"\n")
    outputfile.write("Number of customers : "+str(num_delays_required)+"\n\n")
    num_events=2
    initialize()
    while num_custs_delayed<num_delays_required:
        timing()
        update_time_avg_stats()
        if next_event_type==0:
            arrive()
            if errorstatus:
                break
        elif next_event_type==1:
            depart()
    if not errorstatus:
        report()
    else:
        outputfile.write(errormessage)
    table = [["k","average delay in queue","average number in queue","server utilization","time the simulation ended"],["---","----------------------","-----------------------","------------------","-------------------------"]]
    generate_statistics()
    outputfile.close()
    

if __name__ == "__main__":
    main()
