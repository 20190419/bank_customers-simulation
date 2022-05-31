import random
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt


# ----------------------------------------------------------------Inputs.
def RandNum_From_0to1():
    return random.uniform(0, 1)


def get_TBA():  # Get Random values for the time between Arrivals
    RandomProbapility = RandNum_From_0to1()
    if RandomProbapility >= 0 and RandomProbapility < 0.09:
        TBA = 0
    elif RandomProbapility >= 0.09 and RandomProbapility < 0.28:
        TBA = 1
    elif RandomProbapility >= 0.28 and RandomProbapility < 0.58:
        TBA = 2
    elif RandomProbapility >= 0.58 and RandomProbapility < 0.79:
        TBA = 3
    elif RandomProbapility >= 0.79 and RandomProbapility < 0.91:
        TBA = 4
    else:
        TBA = 5
    return TBA


def get_ST():  # Get Random values for
    RandomProbapility = RandNum_From_0to1()
    if RandomProbapility >= 0 and RandomProbapility < 0.2:
        ST = 1
    elif RandomProbapility >= 0.2 and RandomProbapility < 0.6:
        ST = 2
    elif RandomProbapility >= 0.6 and RandomProbapility < 0.88:
        ST = 3
    else:
        ST = 4
    return ST


TBA = []  # Time Between Arrivals.
ST = []  # Service Time of All Customers.
ST_in = []  # Service Time inside-Bank teller.
ST_out = []  # Service Time.
WT_in = []  # Waiting Time inside-Bank teller.
WT_out = []  # Waiting Time.
AT = []  # Arrival Time of All Customers.
SST_out = []  # Start Service Time Drive-in teller.
SST_in = []  # Start Service Time inside-Bank teller.
CT = []  # Completion Time of All Customers.
TIS = []  # Time in System of All Customers.
ATM_In = []  # Completion Time inside-Bank teller.
ATM_Out = []  # Completion Time Drive-in teller.
Idle_Out = []  # Idle Time Drive-in teller.
Idle_In = []  # Idle Time inside-Bank teller.

Customers_num = 100

for i in range(Customers_num):
    x = get_TBA()
    if i == 0:
        AT.append(0)
    else:
        AT.append(x + AT[i - 1])

for i in range(len(AT)):
    x = get_ST()
    ST.append(x)

n = -1  # Counter for number of customers inside Bank teller.
m = -1  # Counter for number of customers Drive-in teller.
# -------------------------------------------------------------------------Cases of Customers.
for i in range(0, len(AT)):  # i is a counter for All Customers.
    if (i == 0):  # 1st ROW (Client)-------------------------------"START OF (DRIVE IN) CASE".
        m += 1
        SST_out.append(AT[0])
        WT_out.append(0)
        CT.append(SST_out[i] + ST[i])
        TIS.append(CT[i] - AT[i])
        ATM_Out.append(CT[i])
        ST_out.append(ST[i])
        Idle_Out.append(0)
        Idle_In.append(CT[i])
    elif (i == 1):  # 2nd ROW (Client)
        m += 1
        if (AT[i] >= CT[m - 1]):
            SST_out.append(AT[i])
            WT_out.append(0)
            Idle_Out.append(AT[i] - CT[m - 1])
        else:
            SST_out.append(CT[m - 1])
            WT_out.append(CT[m - 1] - AT[i])
            Idle_Out.append(0)
        CT.append(SST_out[m] + ST[i])
        ATM_Out.append(CT[m])
        TIS.append(CT[m] - AT[i])
        Idle_In.append(CT[m] - CT[m - 1])
        ST_out.append(ST[i])
    else:
        if (AT[i] >= ATM_Out[m]):
            # Third Customer enter to drive-in teller when AT is greater than or equal CT of previous customer.
            m += 1
            SST_out.append(AT[i])
            WT_out.append(0)
            Idle_Out.append(AT[i] - CT[m - 1])
            CT.append(SST_out[m] + ST[i])
            TIS.append(CT[i] - AT[i])
            ATM_Out.append(CT[m])
            if (SST_in):  # check if the Service list of inside-bank is empty or not.
                if (ATM_In[n] < AT[i]):
                    Idle_In.append(AT[i] - ATM_In[n])
            else:
                Idle_In.append(ATM_Out[m] - SST_out[m])
            # Idle_In.append(CT[m] - CT[m - 1])
            ST_out.append(ST[i])
        elif (AT[i] < ATM_Out[m] and AT[m] >= ATM_Out[m - 1]):
            # Third Customer enter to drive-in teller when AT is equal AT of previous customer
            # and The previous of the previous customer is done.
            m += 1
            SST_out.append(CT[m - 1])
            WT_out.append(CT[m - 1] - AT[i])
            CT.append(SST_out[m] + ST[i])
            ATM_Out.append(CT[m])
            TIS.append(CT[i] - AT[i])
            ST_out.append(ST[i])
            Idle_Out.append(0)
            if (SST_in):
                if (ATM_In[n] < AT[i]):
                    Idle_In.append(AT[i] - ATM_In[n])
            else:
                Idle_In.append(ATM_Out[m] - SST_out[m])  # --------------------"END OF (DRIVE IN) CASE".
        else:
            if (not SST_in):  # 1st ROW (Client) inside-bank------------------"START OF (Inside) CASE".
                n += 1
                SST_in.append(AT[i])
                WT_in.append(0)
                CT.append(SST_in[n] + ST[i])
                TIS.append(CT[i] - AT[i])
                ATM_In.append(CT[i])
                ST_in.append(ST[i])
                ST_out.append(0)
                Idle_In.append(0)
            else:
                if (AT[i] >= ATM_In[n]):
                    n += 1
                    SST_in.append(AT[i])
                    WT_in.append(0)
                    CT.append(SST_in[n] + ST[i])
                    ATM_In.append(CT[i])
                    TIS.append(CT[i] - AT[i])
                    ST_in.append(ST[i])
                    ST_out.append(0)
                    Idle_In.append(ATM_In[n] - AT[i])
                else:
                    n += 1
                    SST_in.append(ATM_In[n - 1])
                    WT_in.append(ATM_In[n - 1] - AT[i])
                    CT.append(SST_in[n] + ST[i])
                    ATM_In.append(CT[i])
                    TIS.append(CT[i] - AT[i])
                    ST_in.append(ST[i])
                    # ST_out.append(0)
                    Idle_In.append(0)  # ----------------------------------------"START OF (Inside) CASE"


# ------------------------------------------------------------------------------------- Calculations
def Display_ST_out():  # calculate
    print("1/AVG Service Time of Drive-in teller-------> ", sum(ST_out) / len(ST_out))


#Display_ST_out()


def Display_ST_in():  # calculate
    if ST_in:
        print("1/AVG Service Time of inside-Bank teller----> ", sum(ST_in) / len(ST_in))
    else:
        print("No Customers are Serviced inside-Bank teller!")


#Display_ST_in()


def Display_WT_in():  # calculate
    if ST_in:
        print("2/AVG Waiting Time of inside-Bank teller----> ", sum(WT_in) / len(WT_in))
    else:
        print("No Customers are Serviced inside-Bank teller!")


#Display_WT_in()


def Display_WT_out():  # calculate
    print("2/AVG Waiting Time of Drive-in teller-------> ", sum(WT_out) / len(WT_out))


#Display_WT_out()
Max_len = 0
if len(WT_in)>0:
    for x in range(len(WT_in)):
        if (WT_in[n] > 0 and WT_in[n + 1] > 0):
            Max_len = 2
        else:
            Max_len = 1


def Display_max():
    if (SST_in):
        print("3/The Max inside-Bank teller queue length---> ", Max_len)
    else:
        print("3/No Customers are Serviced inside-Bank teller!")


Prob_ofWT_in = 0
for i in range(0, len(WT_in)):
    if WT_in[i] > 0:
        Prob_ofWT_in += 1


def Display_prob():
    if WT_in: print("4/The Probability that A Customer wait inside-Bank teller queue ---> ",
                    (Prob_ofWT_in / len(WT_in)) * 100, "%")


def Display_idle_in():
    print("5/The total of idle time of the inside-Bank teller----> ", sum(Idle_In))  # calculate
# ----------------------------------------------------------------------------------------------Start of Histogram
plt.hist(ST_in, density=True, bins=200)
plt.ylabel('probability')
plt.xlabel('Values of Service Time inside Bank teller')
plt.show()

plt.hist(ST_out, density=True, bins=200)
plt.ylabel('probability')
plt.xlabel('Values of Service Time Drive-in Bank teller')
plt.show()

plt.hist(WT_in, density=True, bins=200)
plt.ylabel('probability')
plt.xlabel('Values of Waiting Time inside Bank teller')
plt.show()

plt.hist(WT_out, density=True, bins=200)
plt.ylabel('probability')
plt.xlabel('Values of Waiting Time Drive-in Bank teller')
plt.show()
# --------------------------------------------------------------End of Histogram
root = Tk()
root.geometry('700x100')

# This will create a LabelFrame
label_frame = LabelFrame(root, text='Bank Teller')
label_frame.pack(expand='yes', fill='both')

# Buttons
btn1 = ttk.Button(root, text='AVG of ST inside bank')
btn1.pack()
btn1.place(x=50, y=20)
btn1.config(command=lambda: Display_ST_in())
# ***********************************************
btn2 = Button(root, text='AVG of ST Drive-in bank')
btn2.pack()
btn2.place(x=200, y=20)
btn2.config(command=lambda: Display_ST_out())
# ***********************************************
btn3 = Button(root, text='AVG of WT inside bank')
btn3.pack()
btn3.place(x=350, y=20)
btn3.config(command=lambda: Display_WT_in())
# ***********************************************
btn4 = Button(root, text='AVG of WT Drive-in bank')
btn4.pack()
btn4.place(x=500, y=20)
btn4.config(command=lambda: Display_WT_out())
# ***********************************************
btn5 = Button(root, text='Max length inside queue')
btn5.pack()
btn5.place(x=50, y=70)
btn5.config(command=lambda: Display_max())
# ***********************************************
btn6 = Button(root, text='Prob of A Customer wait inside')
btn6.pack()
btn6.place(x=240, y=70)
btn6.config(command=lambda: Display_prob())
# ***********************************************
btn7 = Button(root, text='Total of idle inside-Bank')
btn7.pack()
btn7.place(x=460, y=70)
btn7.config(command=lambda: Display_idle_in())
# ***********************************************
mainloop()
