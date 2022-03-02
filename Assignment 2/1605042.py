from os import wait
import sys
import random
import numpy
import pandas

outputfile=open("output.txt",'w')
def main():
    inputFile=open(sys.argv[1],'r')
    simulation_termination=[int(x) for x in next(inputFile).split()][0]
    number_of_floors,number_of_elevators,capacity,batch_size=[int(x) for x in next(inputFile).split()]
    door_holding_time, interFloor_traveling_time, opening_time, closing_time=[float(x) for x in next(inputFile).split()]
    embarking_time,disembarking_time=[float(x) for x in next(inputFile).split()]
    mean_interarrival_time=[float(x) for x in next(inputFile).split()][0]
    mean_interarrival_time=mean_interarrival_time*60
    inputFile.close()
    Between=[] #time between successive arrivals of customers
    Arrive=[] #time of arrival from start of clock at t=0 for customer i 
    Floor=[] #floor selected by customer i
    Elevator=[] #time customer i spends in an elevator
    Delivery=[] #ime required to deliver customer i to destination floor from time of arrival, including any waiting time
    Selvec=[[0]*number_of_floors for i in range(number_of_elevators)] #representing the floors selected for elevator j , not counting the number of times a particular floor has been selected
    Flrvec=[[0]*number_of_floors for i in range(number_of_elevators)] #integer one-dimensional array representing the number of times each floor has been selected for elevator j for the group of passengers currently being transported to their respective floors
    Occup=[0]*number_of_elevators #number of current occupants of elevator j
    Available=[0]*number_of_elevators #Total time an elavator waits in floor 1
    Return=[0]*number_of_elevators #time from start of clock at t=0 that elevator j returns to the main floor and is available for receiving passengers
    First=[0]*number_of_elevators #an index, the customer number of the first passenger who enters elevator j after it returns to the main floor
    Load=[0]*number_of_elevators #Total customer carried by an elevator
    MaxLoad=[0]*number_of_elevators #number of time an elevator carried maximum loads
    Departs=[0]*number_of_elevators #number of time an elevator carried maximum departs
    quecust=0 #customer number of the first person waiting in the queue
    queue=0 #total length of current queue of customers waiting for an elevator to become available
    startque=0 #clock time at which the (possiblyupdated) current queue commences to form
    Stop=[0]*number_of_elevators #total number of stops made by elevator j during the entire simulation
    Eldel=[0]*number_of_elevators #total time elevator j spends in delivering its current load of passengers
    Operate=[0]*number_of_elevators #total time elevator j operates during the entire simulation
    limit=0 #customer number of the last person to enter an available elevator before it commences transport
    Max=0 #largest index of a non zero entry in the array selvecj
    remain=0 #number of customers left in the queue after loading next available elevator
    quetotal=0 #total number of customers who spent time waiting
    queueChangeTime=0 #the time when the last queue length changed
    areaQueueLen=0 #area for average queue length
    max_customer_limit=10000 # an upper-bound guess for the total number of customers
    Wait=[0]*max_customer_limit #time customer i waits before stepping into an elevator
    inter_arrival_times=[0]*max_customer_limit #generated inter-arrival time from exponential distribution
    i=0
    while i<max_customer_limit:
        temp_batch=numpy.random.binomial(batch_size-1,0.5)+1
        inter_arrival_times[i]=numpy.random.exponential(mean_interarrival_time)
        i=i+temp_batch
    DELTIME=ELEVTIME=MAXDEL=MAX_ELEV=QUELEN=QUETIME=MAXQUE=quetotal=remain=0
    i=0
    Between.append(inter_arrival_times[i])
    Floor.append(random.randint(1,number_of_floors-1))
    Delivery.append(door_holding_time+embarking_time)
    Elevator.append(0)
    Arrive.append(0)
    TIME=Between[i]
    step8=False
    while TIME<=simulation_termination: #Step 4-5
        if not step8:
            j=-1
            for e in range(number_of_elevators):
                if TIME>=Return[e]:
                    j=e
        if (j>=0 and not step8) or step8:
            if not step8:
                First[j]=i
                Occup[j]=0
                for k in range(number_of_floors):
                    Selvec[j][k]=0
                    Flrvec[j][k]=0
            while True: 
                if not step8:
                    Selvec[j][Floor[i]]=1
                    Flrvec[j][Floor[i]]+=1
                    Occup[j]+=1
                if step8:
                    step8=False
                i+=1
                Between.append(inter_arrival_times[i])
                Floor.append(random.randint(1,number_of_floors-1))
                Elevator.append(0)
                Arrive.append(0)
                TIME+=Between[i]
                Delivery.append(door_holding_time+embarking_time)
                for k in range(number_of_elevators):
                    if TIME>=Return[k]:
                        Available[k]+=TIME-Return[k]
                        Return[k]=TIME
                if Between[i]<=door_holding_time and Occup[j]<capacity:
                    for k in range(First[j],i):
                        Delivery[k]+=Between[i]+embarking_time
                    continue
                else:
                    limit=i-1
                    break
            for k in range(First[j],limit+1):
                N=Floor[k]
                Elevator[k]=(N*interFloor_traveling_time)+(disembarking_time*sum(Flrvec[j][0:N]))+disembarking_time+((opening_time+closing_time)*sum(Selvec[j][0:N]))+opening_time
                Delivery[k]+=Elevator[k]
                DELTIME+=Delivery[k]
                if Delivery[k]>MAXDEL:
                    MAXDEL=Delivery[k]
                if Elevator[k]>MAX_ELEV:
                    MAX_ELEV=Elevator[k]
            Stop[j]+=sum(Selvec[j])
            Load[j]+=sum(Flrvec[j])
            Departs[j]+=1
            if sum(Flrvec[j])==capacity:
                MaxLoad[j]+=1
            Max=0
            for l in range(number_of_floors):
                if Selvec[j][l]!=0:
                    Max=l
            Eldel[j]=(2*interFloor_traveling_time*Max)+(disembarking_time*sum(Flrvec[j]))+((opening_time+closing_time)*sum(Selvec[j]))
            Return[j]=TIME+Eldel[j]
            Operate[j]+=Eldel[j]
            continue
        quecust=i
        startque=TIME
        queue=1
        queueChangeTime=TIME
        Arrive[i]=TIME
        while True:
            i+=1
            Between.append(inter_arrival_times[i])
            Floor.append(random.randint(1,number_of_floors-1))
            TIME+=Between[i]
            Arrive.append(TIME)
            Delivery.append(0)
            Elevator.append(0)
            areaQueueLen+=(queue*(TIME-queueChangeTime))
            queue+=1
            queueChangeTime=TIME
            j=-1
            for e in range(number_of_elevators):
                if TIME>=Return[e]:
                    j=e
            if j<0:
                continue
            for k in range(number_of_elevators):
                Selvec[j][k]=0
                Flrvec[j][k]=0
            remain=queue-capacity
            R=i #last customer index who enters the newly available elevator
            if remain<=0:
                Occup[j]=queue
            else:
                R=quecust+capacity-1
                Occup[j]=capacity
            for k in range(quecust,R+1):
                Selvec[j][Floor[k]]=1
                Flrvec[j][Floor[k]]+=1
            if queue>QUELEN:
                QUELEN=queue
            quetotal+=Occup[j]
            for l in range(quecust,R+1):
                QUETIME+=(TIME-Arrive[l])
            if (TIME-startque)>=MAXQUE:
                MAXQUE=TIME-startque
            First[j]=quecust
            for k in range(First[j],R+1):
                Delivery[k]=door_holding_time+TIME-Arrive[k]+embarking_time
                Wait[k]=TIME-Arrive[k]
            if remain<=0:
                areaQueueLen+=(queue*(TIME-queueChangeTime))
                queueChangeTime=TIME
                queue=0
                step8=True
                break
            else:
                limit=R
                for k in range(First[j],R+1):
                    N=Floor[k]
                    Elevator[k]=(N*interFloor_traveling_time)+(disembarking_time*sum(Flrvec[j][0:N]))+disembarking_time+((opening_time+closing_time)*sum(Selvec[j][0:N]))+opening_time
                    Delivery[k]+=Elevator[k]
                    DELTIME+=Delivery[k]
                    if Delivery[k]>MAXDEL:
                        MAXDEL=Delivery[k]
                    if Elevator[k]>MAX_ELEV:
                        MAX_ELEV=Elevator[k]
                Stop[j]+=sum(Selvec[j])
                Load[j]+=sum(Flrvec[j])
                Departs[j]+=1
                if sum(Flrvec[j])==capacity:
                    MaxLoad[j]+=1
                Max=0
                for l in range(number_of_floors):
                    if Selvec[j][l]!=0:
                        Max=l
                Eldel[j]=(2*interFloor_traveling_time*Max)+(disembarking_time*sum(Flrvec[j]))+((opening_time+closing_time)*sum(Selvec[j]))
                Return[j]=TIME+Eldel[j]
                Operate[j]+=Eldel[j]
                areaQueueLen+=(queue*(TIME-queueChangeTime))
                queueChangeTime=TIME
                queue=remain
                quecust=R+1
                startque=Arrive[R+1]
    N=i-queue+1
    DELTIME/=N
    # sim=6
    # df=pandas.read_csv("out.csv")
    # print(df["Averag_Queue_length"].mean())
    # avg=round(df.mean(axis=0))
    # df=df.append(avg,ignore_index=True)
    # print(df)
    # df.to_csv("output.csv")
    outputfile.write("Total number of customers served : "+str(N)+"\n")
    # df["Simulation"][sim]=sim+1
    # df["Total_number_of_customers_served"][sim]=N
    outputfile.write("Maximum Queue Length : "+str(QUELEN)+"\n")
    # df["Maximum_Queue_Length"][sim]=QUELEN
    outputfile.write("Average Queue length : "+str(areaQueueLen/TIME)+"\n")
    # df["Averag_Queue_length"][sim]=areaQueueLen/TIME
    outputfile.write("Maximum Delay : "+str(round(MAXQUE))+"\n")
    # df["Maximum_Delay"][sim]=round(MAXQUE)
    if quetotal!=0:
        QUETIME/=quetotal
    outputfile.write("Average Delay : "+str(round(QUETIME))+"\n")
    # df["Average_Delay"][sim]=round(QUETIME)
    ELEVTIME=sum(Elevator[:limit+1])/(limit+1)
    outputfile.write("Maximum elevator time: "+str(round(MAX_ELEV))+"\n")
    # df["Maximum_elevator_time"][sim]=round(MAX_ELEV)
    outputfile.write("Average elevator time: "+str(round(ELEVTIME))+"\n")
    # df["Average_elevator_time"][sim]=round(ELEVTIME)
    outputfile.write("Maximum delivery time : "+str(round(MAXDEL))+"\n")
    # df["Maximum_delivery_time"][sim]=round(MAXDEL)
    outputfile.write("Average delivery time : "+str(round(DELTIME))+"\n")
    # df["Average_delivery_time"][sim]=round(DELTIME)
    
    for k in range(number_of_elevators):
        outputfile.write("***** Elevator "+str(k+1)+" *******\n")
        outputfile.write("Average load size : "+str(round(Load[k]/Departs[k]))+"\n")
        # df["Average_load_size_"+str(k+1)][sim]=round(Load[k]/Departs[k])
        outputfile.write("Operation Time : "+str(round(Operate[k]))+"\n")
        # df["Operation_Time_"+str(k+1)][sim]=round(Operate[k])
        outputfile.write("Available Time : "+str(round(Available[k]))+"\n")
        # df["Available_Time_"+str(k+1)][sim]=round(Available[k])
        outputfile.write("Number of Maximum Loads : "+str(MaxLoad[k])+"\n")
        # df["Number_of_Maximum_Loads_"+str(k+1)][sim]=MaxLoad[k]
        outputfile.write("Number of stops : "+str(Stop[k])+"\n")
        # df["Number_of_stops_"+str(k+1)][sim]=int(Stop[k])
    # df.to_csv("out.csv",index=False)
        

            
if __name__ == "__main__":
    main()