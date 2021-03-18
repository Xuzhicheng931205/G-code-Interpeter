import base64
import tensorflow as tf
import streamlit as st
from itertools import groupby
import pandas as pd
import numpy as np

st.title("Manufacturing Innovation Network Laboratory")
st.header("APP:G-CODE INTERPRETER")
st.subheader("APP description:This APP is designed to obtain the work status information and generate the working status matrix.")
st.markdown('Let' "'s" " " "begin!!!!")

uploaded_file = st.file_uploader("Choose the G-code file")

if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file, header=None)
    Number_lines=len(dataframe)
###############Show dataframe#############################
    agree = st.checkbox('Show G-code File')
    if agree:
        st.dataframe(dataframe)
###############Genarate working matrix#############################
    agree = st.checkbox('Genarate Working Matrix')
    if agree:
        X = st.number_input("X_load/(g)")
        Y = st.number_input("Y_load/(g)")
        Spindle = st.number_input("Spindel_speed/(r/min)")
        sum=st.number_input("initial time/(s)")
        step_size=st.number_input("Window size/(s)",min_value=0.00,step=0.01)
        if step_size==0:
          st.warning('Please input a value that bigger than zero.')
          st.stop()
        my_slot1 = st.empty() # Appends an empty slot to the app. We'll use this later.
        #my_slot2 = st.empty() # Appends an empty slot to the app. We'll use this later.
        # Appends another empty slot.
     ################################################################
        X_positon=[0 for i in range(Number_lines)]
        Y_positon=[0 for i in range(Number_lines)]
        Z_positon=[0 for i in range(Number_lines)]
        B_positon=[0 for i in range(Number_lines)]
        C_positon=[0 for i in range(Number_lines)]
        Feed_Rate=[0 for i in range(Number_lines)]
        X_load=[float(X) for i in range(Number_lines)]
        Y_load=[float(Y) for i in range(Number_lines)]
        Z_load=[float(Y) for i in range(Number_lines)]
        B_load=[float(X) for i in range(Number_lines)]
        C_load=[float(Y) for i in range(Number_lines)]
        #Spindle=input("Spindel_speed/(r/min):",)
        Spindle_speed=[float(Spindle) for i in range(Number_lines)]
        ########### Other auxiliary components ###########################################################
        Coolant_pump=[0 for i in range(Number_lines)]
        Mist_Collecter=[0 for i in range(Number_lines)]
        #########Maximum move speed#######################################################################
        X_Max_feedrate=1000  #mm/min
        Y_MAX_feedrate=50 #mm/min
        Z_MAX_feedrate=500 #mm/min
        B_MAX_feedrate=3600 # Degree/min
        C_MAX_feedrate=3600  # Degree/min
        ###################################################################################################
        Time_duration=[0 for i in range(Number_lines)]
        k=0
        M=0 ###0 is G90 absolute, 1 is G91 incremently
        G_code=[]
        my_slot1.write("Progross in reading G-code:")
        bar1 = st.progress(0) #读取程序进度
        for i in range(Number_lines):

            line=str(dataframe.iloc[i,:])
            #st.write(line)
            line=line.replace(".","")
            line=line.replace(";","")
            line=line.replace('\n',"")
            line=line.rstrip(' ')
            # line=line.replace(' ','')
            line = line.replace(" ", '')
            ss = [''.join(list(g)) for k, g in groupby(line, key=lambda x: x.isdigit())][1:-3]

            if  'O' in ss: #G-code_name
                O_index=[i for i,x in enumerate(ss) if x == 'O' ]
                if O_index[0]==0:
                    G_code_Name=ss[0]+ss[1]
                #print("G-code name:",G_code_Name)
                X_positon[k]=0
                Y_positon[k]=0
                Z_positon[k]=0
                B_positon[k]=0
                C_positon[k]=0
                Coolant_pump[k]=0
                Mist_Collecter[k]=0
                Feed_Rate[k]=0
                Time_duration[k]=0

            if 'G' in ss: #，G04
                G_index=[i for i,x in enumerate(ss) if x == 'G' ]
                if len(G_index)==1:
                    if ss[G_index[0]+1]=='04':
                        Time_duration[k]=float(ss[len(ss)-1])
                        X_positon[k]=X_positon[k-1]
                        Y_positon[k]=Y_positon[k-1]
                        Z_positon[k]=Z_positon[k-1]
                        B_positon[k]=B_positon[k-1]
                        C_positon[k]=C_positon[k-1]
                        Coolant_pump[k]=Coolant_pump[k-1]
                        Mist_Collecter[k]=Mist_Collecter[k-1]
                        Feed_Rate[k]=Feed_Rate[k-1]

            if 'O' not in ss and 'M' not in ss and 'G' not in ss and '%' not in ss:
                if 'X' in ss:
                    X_index=[i for i,x in enumerate(ss) if x == 'X' ]
                    if M==0:
                        X_positon[k]=float(ss[X_index[0]+1])
                    if M==1:
                        X_positon[k]=float(X_positon[k-1])+float(ss[X_index[0]+1])
                    else:
                        X_positon[k]= X_positon[k-1]
                if 'Y' in ss:
                    Y_index=[i for i,x in enumerate(ss) if x == 'Y' ]
                    if M==0:
                        Y_positon[k]=float(ss[Y_index[0]+1])
                    if M==1:
                        Y_positon[k]=float(Y_positon[k-1])+float(ss[Y_index[0]+1])
                    else:
                        Y_positon[k]= Y_positon[k-1]
                if 'Z' in ss:
                    Z_index=[i for i,x in enumerate(ss) if x == 'Z' ]
                    if M==0:
                        Z_positon[k]=float(ss[Z_index[0]+1])
                    if M==1:
                        Z_positon[k]=float(Z_positon[k-1])+float(ss[Z_index[0]+1])
                    else:
                        Z_positon[k]= Z_positon[k-1]
                if 'B' in ss:
                    B_index=[i for i,x in enumerate(ss) if x == 'B' ]
                    if M==0:
                        B_positon[k]=float(ss[B_index[0]+1])
                    if M==1:
                        B_positon[k]=float(B_positon[k-1])+float(ss[B_index[0]+1])
                    else:
                        B_positon[k]= B_positon[k-1]
                if 'C' in ss:
                    C_index=[i for i,x in enumerate(ss) if x == 'C' ]
                    if M==0:
                        C_positon[k]=float(ss[C_index[0]+1])
                    if M==1:
                        C_positon[k]=float(C_positon[k-1])+float(ss[C_index[0]+1])
                    else:
                        C_positon[k]= C_positon[k-1]
                Coolant_pump[k]=Coolant_pump[k-1]
                Mist_Collecter[k]=Mist_Collecter[k-1]
                Feed_Rate[k]=Feed_Rate[k-1]
                if Feed_Rate[k]!=0:
                    t1=((X_positon[k]-X_positon[k-1])**2+(Y_positon[k]-Y_positon[k-1])**2+(Z_positon[k]-Z_positon[k-1])**2)**(1/2)/Feed_Rate[k]
                    t2=abs(B_positon[k]-B_positon[k-1])/Feed_Rate[k]
                    t3=abs(C_positon[k]-C_positon[k-1])/Feed_Rate[k]
                else:
                    t1=0
                    t2=0
                    t3=0
                Time_duration[k]=max([t1,t2,t3])*60

            if  'M' in ss: #G-code_name
                O_index=[i for i,x in enumerate(ss) if x == 'M' ]
                if ss[O_index[0]+1]=='28': #Pump start
                    Coolant_pump[k]=1   #1-On
                    Mist_Collecter[k]=Mist_Collecter[k-1]
                if ss[O_index[0]+1]=='29': #Pump start
                    Coolant_pump[k]=0   #0-off
                    Mist_Collecter[k]=Mist_Collecter[k-1]
                if ss[O_index[0]+1]=='26': #Mistcollect  start
                    Mist_Collecter[k]=1   #1-On
                    Coolant_pump[k]=Coolant_pump[k-1]
                if ss[O_index[0]+1]=='27': #Pump start
                    Mist_Collecter[k]=0   #0-off
                    Coolant_pump[k]=Coolant_pump[k-1]
                X_positon[k]=X_positon[k-1]
                Y_positon[k]=Y_positon[k-1]
                Z_positon[k]=Z_positon[k-1]
                B_positon[k]=B_positon[k-1]
                C_positon[k]=C_positon[k-1]
                Feed_Rate[k]=Feed_Rate[k-1]
                Time_duration[k]=0
                if ss[O_index[0]+1]=='30':
                    Feed_Rate[k]=0
                    Time_duration[k]=0

            if 'G' in ss: #，G01
                G_index=[i for i,x in enumerate(ss) if x == 'G' ]
                if len(G_index)==1:
                    if ss[G_index[0]+1]=='01':
                        if 'X' in ss:
                            X_index=[i for i,x in enumerate(ss) if x == 'X' ]
                        if M==0:
                            X_positon[k]=float(ss[X_index[0]+1])
                        if M==1:
                            X_positon[k]=float(X_positon[k-1])+float(ss[X_index[0]+1])
                        else:
                            X_positon[k]= X_positon[k-1]
                        if 'Y' in ss:
                            Y_index=[i for i,x in enumerate(ss) if x == 'Y' ]
                            if M==0:
                                Y_positon[k]=float(ss[Y_index[0]+1])
                            if M==1:
                                Y_positon[k]=float(Y_positon[k-1])+float(ss[Y_index[0]+1])
                            else:
                                Y_positon[k]= Y_positon[k-1]
                        if 'Z' in ss:
                            Z_index=[i for i,x in enumerate(ss) if x == 'Z' ]
                            if M==0:
                                Z_positon[k]=float(ss[Z_index[0]+1])
                            if M==1:
                                Z_positon[k]=float(Z_positon[k-1])+float(ss[Z_index[0]+1])
                            else:
                                Z_positon[k]= Z_positon[k-1]
                        if 'B' in ss:
                            B_index=[i for i,x in enumerate(ss) if x == 'B' ]
                            if M==0:
                                B_positon[k]=float(ss[B_index[0]+1])
                            if M==1:
                                B_positon[k]=float(B_positon[k-1])+float(ss[B_index[0]+1])
                            else:
                                B_positon[k]= B_positon[k-1]
                        if 'C' in ss:
                            C_index=[i for i,x in enumerate(ss) if x == 'C' ]
                            if M==0:
                                C_positon[k]=float(ss[C_index[0]+1])
                            if M==1:
                                C_positon[k]=float(C_positon[k-1])+float(ss[C_index[0]+1])
                            else:
                                C_positon[k]= C_positon[k-1]
                        if 'F' in ss:
                            F_index=[i for i,x in enumerate(ss) if x == 'F' ]
                            Feed_Rate[k]=float(ss[F_index[0]+1])
                        Coolant_pump[k]=Coolant_pump[k-1]
                        Mist_Collecter[k]=Mist_Collecter[k-1]

                        if Feed_Rate[k-1]!=0:
                            t1=((X_positon[k]-X_positon[k-1])**2+(Y_positon[k]-Y_positon[k-1])**2+(Z_positon[k]-Z_positon[k-1])**2)**(1/2)/Feed_Rate[k]
                            t2=abs(B_positon[k]-B_positon[k-1])/Feed_Rate[k]
                            t3=abs(C_positon[k]-C_positon[k-1])/Feed_Rate[k]
                        else:
                            t1=0
                            t2=0
                            t3=0
                        Time_duration[k]=max([t1,t2,t3])*60

            if 'G' in ss: #G-function  #G00 initial positon
                G_index=[i for i,x in enumerate(ss) if x == 'G' ]
                if len(G_index)==1:
                    if ss[G_index[0]+1]=='00':
                        if 'X' in ss:
                            X_index=[i for i,x in enumerate(ss) if x == 'X' ]
                            X_positon[k]=float(ss[X_index[0]+1])
                        else:
                            X_positon[k]= X_positon[k-1]
                        if 'Y' in ss:
                            Y_index=[i for i,x in enumerate(ss) if x == 'Y' ]
                            Y_positon[k]=float(ss[Y_index[0]+1])
                        else:
                            Y_positon[k]= Y_positon[k-1]
                        if 'Z' in ss:
                            Z_index=[i for i,x in enumerate(ss) if x == 'Z' ]
                            Z_positon[k]=float(ss[Z_index[0]+1])
                        else:
                            Z_positon[k]= Z_positon[k-1]
                        if 'B' in ss:
                            B_index=[i for i,x in enumerate(ss) if x == 'B' ]
                            B_positon[k]=float(ss[B_index[0]+1])
                        else:
                            B_positon[k]= B_positon[k-1]
                        if 'C' in ss:
                            C_index=[i for i,x in enumerate(ss) if x == 'C' ]
                            C_positon[k]=float(ss[C_index[0]+1])
                        else:
                            C_positon[k]= C_positon[k-1]
                        Coolant_pump[k]=Coolant_pump[k-1]
                        Mist_Collecter[k]=Mist_Collecter[k-1]
                        Feed_Rate[k]=Feed_Rate[k-1]
                        t1=((X_positon[k]-X_positon[k-1])**2+(Y_positon[k]-Y_positon[k-1])**2+(Z_positon[k]-Z_positon[k-1])**2)**(1/2)/1000
                        t2=abs(B_positon[k]-B_positon[k-1])/3600
                        t3=abs(C_positon[k]-C_positon[k-1])/3600
                        Time_duration[k]=max([t1,t2,t3])*60

            if 'G' in ss: #G-function  #G92 initial positon
                G_index=[i for i,x in enumerate(ss) if x == 'G' ]
                if len(G_index)==1:
                    if ss[G_index[0]+1]=='92':
                        if 'X' in ss:
                            X_index=[i for i,x in enumerate(ss) if x == 'X' ]
                            X_positon[k]=float(ss[X_index[0]+1])
                        else:
                            X_positon[k]= X_positon[k-1]
                        if 'Y' in ss:
                            Y_index=[i for i,x in enumerate(ss) if x == 'Y' ]
                            Y_positon[k]=float(ss[Y_index[0]+1])
                        else:
                            Y_positon[k]= Y_positon[k-1]
                        if 'Z' in ss:
                            Z_index=[i for i,x in enumerate(ss) if x == 'Z' ]
                            Z_positon[k]=float(ss[Z_index[0]+1])
                        else:
                            Z_positon[k]= Z_positon[k-1]
                        if 'B' in ss:
                            B_index=[i for i,x in enumerate(ss) if x == 'B' ]
                            B_positon[k]=float(ss[B_index[0]+1])
                        else:
                            B_positon[k]= B_positon[k-1]
                        if 'C' in ss:
                            C_index=[i for i,x in enumerate(ss) if x == 'C' ]
                            C_positon[k]=float(ss[C_index[0]+1])
                        else:
                            C_positon[k]= C_positon[k-1]
                        Coolant_pump[k]=Coolant_pump[k-1]
                        Mist_Collecter[k]=Mist_Collecter[k-1]
                        Feed_Rate[k]=0
                        Time_duration[k]=0

            if 'G' in ss: #G90，G01 absolute
                G_index=[i for i,x in enumerate(ss) if x == 'G' ]
                if len(G_index)==2:
                    if ss[G_index[0]+1]=='90'and ss[G_index[1]+1]=='01':
                        M=0 #G90就设置M=0
                        if 'X' in ss:
                            X_index=[i for i,x in enumerate(ss) if x == 'X' ]
                            X_positon[k]=float(ss[X_index[0]+1])
                        else:
                            X_positon[k]= X_positon[k-1]
                        if 'Y' in ss:
                            Y_index=[i for i,x in enumerate(ss) if x == 'Y' ]
                            Y_positon[k]=float(ss[Y_index[0]+1])
                        else:
                            Y_positon[k]= Y_positon[k-1]
                        if 'Z' in ss:
                            Z_index=[i for i,x in enumerate(ss) if x == 'Z' ]
                            Z_positon[k]=float(ss[Z_index[0]+1])
                        else:
                            Z_positon[k]= Z_positon[k-1]
                        if 'B' in ss:
                            B_index=[i for i,x in enumerate(ss) if x == 'B' ]
                            B_positon[k]=float(ss[B_index[0]+1])
                        else:
                            B_positon[k]= B_positon[k-1]
                        if 'C' in ss:
                            C_index=[i for i,x in enumerate(ss) if x == 'C' ]
                            C_positon[k]=float(ss[C_index[0]+1])
                        else:
                            C_positon[k]= C_positon[k-1]
                        if 'F' in ss:
                            F_index=[i for i,x in enumerate(ss) if x == 'F' ]
                            Feed_Rate[k]=float(ss[F_index[0]+1])
                        Coolant_pump[k]=Coolant_pump[k-1]
                        Mist_Collecter[k]=Mist_Collecter[k-1]
                        if Feed_Rate[k]!=0:
                            t1=((X_positon[k]-X_positon[k-1])**2+(Y_positon[k]-Y_positon[k-1])**2+(Z_positon[k]-Z_positon[k-1])**2)**(1/2)/Feed_Rate[k]
                            t2=abs(B_positon[k]-B_positon[k-1])/Feed_Rate[k]
                            t3=abs(C_positon[k]-C_positon[k-1])/Feed_Rate[k]
                        else:
                            t1=0
                            t2=0
                            t3=0
                        Time_duration[k]=max([t1,t2,t3])*60


            if 'G' in ss: #G91，G01 icremently
                G_index=[i for i,x in enumerate(ss) if x == 'G' ]
                if len(G_index)==2:
                    if ss[G_index[0]+1]=='91'and ss[G_index[1]+1]=='01':
                        M=1 #G90就设置M=0
                        if 'X' in ss:
                            X_index=[i for i,x in enumerate(ss) if x == 'X' ]
                            X_positon[k]=float(X_positon[k-1])+float(ss[X_index[0]+1])
                        else:
                            X_positon[k]= X_positon[k-1]
                        if 'Y' in ss:
                            Y_index=[i for i,x in enumerate(ss) if x == 'Y' ]
                            Y_positon[k]=float(Y_positon[k-1])+float(ss[Y_index[0]+1])
                        else:
                            Y_positon[k]= Y_positon[k-1]
                        if 'Z' in ss:
                            Z_index=[i for i,x in enumerate(ss) if x == 'Z' ]
                            Z_positon[k]=float(Z_positon[k-1])+float(ss[Z_index[0]+1])
                        else:
                            Z_positon[k]= Z_positon[k-1]
                        if 'B' in ss:
                            B_index=[i for i,x in enumerate(ss) if x == 'B' ]
                            B_positon[k]=float(B_positon[k-1])+float(ss[B_index[0]+1])
                        else:
                            B_positon[k]= B_positon[k-1]
                        if 'C' in ss:
                            C_index=[i for i,x in enumerate(ss) if x == 'C' ]
                            C_positon[k]=float(C_positon[k-1])+float(ss[C_index[0]+1])
                        else:
                            C_positon[k]= C_positon[k-1]
                        if 'F' in ss:
                            F_index=[i for i,x in enumerate(ss) if x == 'F' ]
                            Feed_Rate[k]=float(ss[F_index[0]+1])
                        Coolant_pump[k]=Coolant_pump[k-1]
                        Mist_Collecter[k]=Mist_Collecter[k-1]
                        if Feed_Rate[k]!=0:
                            t1=((X_positon[k]-X_positon[k-1])**2+(Y_positon[k]-Y_positon[k-1])**2+(Z_positon[k]-Z_positon[k-1])**2)**(1/2)/Feed_Rate[k]
                            t2=abs(B_positon[k]-B_positon[k-1])/Feed_Rate[k]
                            t3=abs(C_positon[k]-C_positon[k-1])/Feed_Rate[k]
                        else:
                            t1=0
                            t2=0
                            t3=0
                        Time_duration[k]=max([t1,t2,t3])*60

            if '%' in ss:
                print("程序已经读完结束")

            k=k+1
            bar1.progress((i+1)/Number_lines)

        Work_Status_df=pd.DataFrame([G_code,Time_duration,X_positon,Y_positon,Z_positon,B_positon,C_positon,X_load,Y_load,Z_load,B_load,C_load,
                                     Spindle_speed, Mist_Collecter,Coolant_pump,Feed_Rate])
        Work_Status=pd.DataFrame(Work_Status_df.values.T,columns=['G_code','Time_duration','X_positon','Y_positon','Z_positon','B_positon','C_positon','X_load','Y_load','Z_load','B_load','C_load',
                                                                  'Spindle_speed', 'Mist_Collecter','Coolant_pump',"Feed_Rate"])
        # print(Work_Status)
        ##############################Calculate the accmulate time##########################################################################################
        Accumulate_time=[]
        #sum=30 #duration-time before start the machine
        for i in range(len(Time_duration)): #构建新的一列
            sum=sum+Time_duration[i]
            Accumulate_time.append(sum)
        #print("Accumulate_time",len(Accumulate_time),Accumulate_time)
        Work_Status["Accumulate_time"]=Accumulate_time
        ##############################Generate the working status matrix#############################################################################
        Work_Status=Work_Status.iloc[:,1:]
        #step_size=0.5 #Window size
        df_Working_status_matrix=Work_Status.iloc[0:2,:] #构建一个初始dataframe
        my_slot2=st.empty()
        my_slot2.write("Progross in generating working matrix:")
        bar2=st.progress(0)
        for i in range(1,Work_Status.shape[0]):
            t1=Work_Status["Accumulate_time"].values[i]
            t2=Work_Status["Accumulate_time"].values[i-1]
            if (t1-t2)==0:
                continue
            if (t1-t2)!=0:
                Time_difference=t1-t2
                interplote_unmber=Time_difference/step_size
                df=Work_Status.iloc[i-1:i+1,]
                New_index=[i for i in range(int(df.shape[0]))]
                df=df.reset_index(drop=True) #对没有的index的进行index
                #print("df",i,df)
                df.index = df.index * int(interplote_unmber) # 对原有数据集的index进行扩增
                #print(df)
                for k in range(1,int(interplote_unmber),1):
                    df.loc[k]=[np.nan for i in range(df.shape[1])]
                df = df.sort_index()  # index 进行排序
                df = df.astype(float)
                df["Time_duration"]=df["Time_duration"].bfill()  #进行线性插值
                df["Feed_Rate"]=df["Feed_Rate"].bfill()  #进行线性插值
                df=df.interpolate(method='linear', axis=0)  #进行线性插值
                #print("df",df)
                df_Working_status_matrix=df_Working_status_matrix.append(df.iloc[1:,:], ignore_index=True) #拼接
                bar2.progress((i+1)/Work_Status.shape[0])

        # print(df_Working_status_matrix.head(10))
        order=['Accumulate_time','Time_duration','X_positon','Y_positon','Z_positon','B_positon','C_positon','X_load','Y_load','Z_load','B_load','C_load',
                                                                  'Spindle_speed', 'Mist_Collecter','Coolant_pump','Feed_Rate']
        df=df_Working_status_matrix[order]
        st.dataframe(df)
        st.balloons()

        def get_table_download_link(df):
            """Generates a link allowing the data in a given panda dataframe to be downloaded
            in:  dataframe
            out: href string
            """
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
            href = f'<a href="data:file/csv;base64,{b64}" download="Working Matrix.csv"> Download Working Matrix CSV File</a>'
            return href

        st.markdown(get_table_download_link(df), unsafe_allow_html=True)

############################加载AI模型预测功率消耗###########################################
    agree = st.checkbox('Show predict power consumption using AI model')
    if agree:
        Data_read=df
        Column=['Accumulate_time','Time_duration','X_positon','Y_positon','Z_positon','B_positon','C_positon','X_load','Y_load','Z_load','B_load','C_load',
                'Spindle_speed', 'Mist_Collecter','Coolant_pump','Feed_Rate']
        Goal_column=['X_positon','Y_positon','Z_positon','B_positon','C_positon','X_load','Y_load','Z_load','B_load','C_load',
                     'Spindle_speed', 'Mist_Collecter','Coolant_pump','Feed_Rate']
        df1=Data_read[Goal_column]

        model = tf.keras.models.load_model('./save_model/model_comsumption.h5')
        st.write("AI model is ready for loading")

        value_arry=[]#功率预测初始值
        st.write("Progross in prediction process:")
        bar3=st.progress(0)

        for i in range(df1.shape[0]): #df1.shape[0] 对能耗进行预测
            df2=np.array(df1.iloc[i,:]).reshape(-1,14)
            value=model.predict(df2).flatten()
            #print(value)
            value_arry.append(value)
            bar3.progress((i+1)/df1.shape[0])
            # plt.plot(np.array(Data_read["Accumulate_time"])[0:i].flatten(),value_arry)
            # plt.pause(0.01)
        x=Data_read["Accumulate_time"].values
        y=np.array(value_arry).flatten().tolist()

        ###################计算总能耗#################################
        s=0
        for i  in range(len(y)):
            s=s+y[i]
        Total_Energy=s*step_size/1000
        df=pd.DataFrame({"Time":x,"Consumption power":y})
        #df = df.rename(columns={'Time':'index'}).set_index('index')
        #st.line_chart(df)

        import altair as alt
        # Basic Altair line chart where it picks automatically the colors for the lines
        basic_chart = alt.Chart(df).mark_line().encode(
            x="Time",
            y="Consumption power",
            #color='red',
            #color='Origin',
            #legend=alt.Legend(title='Prediction power from G_code')
        ).interactive()
        st.altair_chart(basic_chart)
        st.write("Total energy consumption(kJ):",Total_Energy)


        import base64
        def get_table_download_link(df):
            """Generates a link allowing the data in a given panda dataframe to be downloaded
            in:  dataframe
            out: href string
            """
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
            href = f'<a href="data:file/csv;base64,{b64}" download="Power consumption.csv"> Download Working Matrix CSV File</a>'
            return href

        st.markdown(get_table_download_link(df), unsafe_allow_html=True)
