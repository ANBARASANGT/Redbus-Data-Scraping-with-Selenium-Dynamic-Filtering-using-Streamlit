import streamlit as st   #web application package
import pandas as pd       #data analy and manip
import mysql.connector    #connecting python to sql db

from streamlit_option_menu import option_menu  #custo. navi menu option for displaying options


# Andhra bus
lists_a=[]     #creating an empty list 
df_a=pd.read_csv("C:/Users/anbar/OneDrive/Desktop/Redbus/df_andhra.csv")   #reading csv file
for i,r in df_a.iterrows():      #iterate over each row so the iterrow function returns i and r , i means index r means row as pandas series
    lists_a.append(r["routename"])  #routename from each row getting added to the list

#Assam bus
lists_as=[]
df_as=pd.read_csv("C:/Users/anbar/OneDrive/Desktop/Redbus/df_assam.csv")
for i,r in df_as.iterrows():
    lists_as.append(r["routename"])

#Bengal bus
lists_b=[]
df_b=pd.read_csv("C:/Users/anbar/OneDrive/Desktop/Redbus/df_bengal.csv")
for i,r in df_b.iterrows():
    lists_b.append(r["routename"])

#chand bus
lists_c=[]
df_c=pd.read_csv("C:/Users/anbar/OneDrive/Desktop/Redbus/df_chand.csv")
for i,r in df_c.iterrows():
    lists_c.append(r["routename"])

#hp bus
lists_hp=[]
df_hp=pd.read_csv("C:/Users/anbar/OneDrive/Desktop/Redbus/df_hp.csv")
for i,r in df_hp.iterrows():
    lists_hp.append(r["routename"])


# kerla bus 
lists_k=[]
df_k=pd.read_csv("C:/Users/anbar/OneDrive/Desktop/Redbus/df_kerla.csv")
for i,r in df_k.iterrows():
    lists_k.append(r["routename"])

# punjab bus
lists_p=[]
df_p=pd.read_csv("C:/Users/anbar/OneDrive/Desktop/Redbus/df_punjab.csv")
for i,r in df_p.iterrows():
    lists_p.append(r["routename"])

#rajasthan bus
lists_r=[]
df_r=pd.read_csv("C:/Users/anbar/OneDrive/Desktop/Redbus/df_rajasthan.csv")
for i,r in df_r.iterrows():
    lists_r.append(r["routename"])

#UP bus
lists_up=[]
df_up=pd.read_csv("C:/Users/anbar/OneDrive/Desktop/Redbus/df_up.csv")
for i,r in df_up.iterrows():
    lists_up.append(r["routename"])

#West bengal bus
lists_wb=[]
df_wb=pd.read_csv("C:/Users/anbar/OneDrive/Desktop/Redbus/df_wb.csv")
for i,r in df_wb.iterrows():
    lists_wb.append(r["routename"])

#setting up streamlit page
st.set_page_config(layout="wide")   #allowing space for content
st.image("C:/Users/anbar/Downloads/redbus-logo-13648C0E43-seeklogo.com.png")  #showing image on the top of the page
opt=option_menu(menu_title="Bus booking",options=["Home","Account","Helpline","Career","About us"],icons=["house","person","headphones","briefcase","info"],orientation="horizontal")
# creating horizontal navigation menu

# Display content based on the selected option
if opt == "Home": #if home is selected means the below content will be shown
    st.title("Welcome to RedBus!")  #title
    st.write("Explore our wide range of bus booking options. Find the best deals and travel comfortably.")  #paragraph
    s = st.selectbox("Select State", ["","Assam", "Andhra Pradesh", "Kerla", "Bengal", "Rajastan", 
                                          "West Bengal", "Uttar Pradesh", "Punjab", "Himachal Pradesh", "Chandigargh"])  #creating dropdown option and the selected option will be stored in the variable s
    t = st.selectbox("select bus type", ("","sleeper", "semi-sleeper","A/C Seater","NON A/C Seater", "others"))          #same here tooo
    f = st.selectbox("select bus fare range", ("","10-300", "301-500","501-700","701-1000","1001-1500","1501-2000","2001 and above"))
    o = st.selectbox("select private or public",("","private bus","public bus"))
    time=st.time_input("timing") #creates a time input widget

    if s=="Assam":  #checking if the selected name is assam
        ass=st.selectbox("Routes",lists_as)  #creeating selectbox the routes for assam will be shown which we stored in a list using variable list_as and again selected route is stored in the variable ass

        def bustype_busfare(bus_type,bus_fare,pvt_pub):  #three parameters are taken to filter the bus details type,cost,pvt or public. So three criteria was given
            mydb = mysql.connector.connect(host="localhost", user="root", password="Sql@10",database="redbus")
            print(mydb)  #connecting to sql and connection object is mydb
            mycursor = mydb.cursor(buffered=True)  #purpose of mycursor is to execute sql queries and buffered true ensures that the cursor fetches all rows at a single time and it will be useful for large datasets

            if bus_type == "sleeper":  #logic filtering based on bustype
                busclass = "Bus_type LIKE '%Sleeper%'" #if customer select sleeper means it will be stored in separate variable and query will be assigned
            elif bus_type == "semi-sleeper":
                busclass = "Bus_type LIKE '%A/c Semi Sleeper%'"
            elif bus_type=="A/C Seater":
                busclass = "Bus_type LIKE '%A/C Seater%'"
            elif bus_type=="NON A/C Seater":
                busclass = "Bus_type LIKE '%Non A/C Seater%'"
            else:
                busclass = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi Sleeper%' AND Bus_type NOT LIKE '%A/C Seater%' AND Bus_type NOT LIKE '%Non A/C Seater%' "
           
            if bus_fare == "10-300": #logic filtering based on fare
                fare_min, fare_max = 10, 300 #bus_fare is a paramater in def function and it will be passed
            elif bus_fare == "301-500":
                fare_min, fare_max = 301, 500
            elif bus_fare == "501-700":
                fare_min, fare_max = 501, 700
            elif bus_fare == "701-1000":
                fare_min, fare_max = 701, 1000  
            elif bus_fare == "1001-1500":
                fare_min, fare_max = 1001, 1500
            elif bus_fare == "1501-2000":
                fare_min, fare_max = 1501, 2000
            else:
                fare_min, fare_max = 2001, 5000

            if pvt_pub == "public bus":   #here it is based on ownership
                busowner = "Bus_name LIKE '%SRTC%'"
            else:
                busowner = "Bus_name NOT LIKE '%SRTC%'"

            insert_query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{ass}"
                AND {busclass} AND {busowner} AND Start_time>='{time}'
                ORDER BY price and Start_time DESC
            '''
            mycursor.execute(insert_query)      #using mycursor object to execute this query
            out=mycursor.fetchall()             #getting all the rows and stored in a variable named out
            mydb.close()                        #closing the connection of my sql database
            df = pd.DataFrame(out, columns=["ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Price", "Seats_Available", "Ratings", "Route_link", "Route_name"])
            return df     #filtered data in out variable will be matched as per the column name and the filtered data will shown as df

            
        df_result =bustype_busfare(t,f,o)      #calling the function using three parameters("bustype","busfare","ownersip")
        st.dataframe(df_result)                #the filtered result will be shown as dataframe

    if s=="Kerla":
        k=st.selectbox("Routes",lists_k)

        def bustype_busfare(bus_type,bus_fare,pvt_pub):
            mydb = mysql.connector.connect(host="localhost", user="root", password="Sql@10",database="redbus")
            print(mydb)
            mycursor = mydb.cursor(buffered=True)

            if bus_type == "sleeper":
                busclass = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                busclass = "Bus_type LIKE '%A/c Semi Sleeper%'"
            elif bus_type=="A/C Seater":
                busclass = "Bus_type LIKE '%A/C Seater%'"
            elif bus_type=="NON A/C Seater":
                busclass = "Bus_type LIKE '%Non A/C Seater%'"
            else:
                busclass = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi Sleeper%' AND Bus_type NOT LIKE '%A/C Seater%' AND Bus_type NOT LIKE '%Non A/C Seater%' "
           
            if bus_fare == "10-300":
                fare_min, fare_max = 10, 300
            elif bus_fare == "301-500":
                fare_min, fare_max = 301, 500
            elif bus_fare == "501-700":
                fare_min, fare_max = 501, 700
            elif bus_fare == "701-1000":
                fare_min, fare_max = 701, 1000  
            elif bus_fare == "1001-1500":
                fare_min, fare_max = 1001, 1500
            elif bus_fare == "1501-2000":
                fare_min, fare_max = 1501, 2000
            else:
                fare_min, fare_max = 2001, 5000

            if pvt_pub == "public bus":
                busowner = "Bus_name LIKE '%SRTC%'"
            else:
                busowner = "Bus_name NOT LIKE '%SRTC%'"

            insert_query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{k}"
                AND {busclass} AND {busowner} AND  Start_time>='{time}'
                ORDER BY price and Start_time DESC
            '''
            mycursor.execute(insert_query)
            out=mycursor.fetchall()
            mydb.close()
            df = pd.DataFrame(out, columns=["ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Price", "Seats_Available", "Ratings", "Route_link", "Route_name"])
            return df

            
        df_result =bustype_busfare(t,f,o)
        st.dataframe(df_result)   
        
         
    if s=="Andhra Pradesh":
        ap=st.selectbox("Routes",lists_a)

        def bustype_busfare(bus_type,bus_fare,pvt_pub):
            mydb = mysql.connector.connect(host="localhost", user="root", password="Sql@10",database="redbus")
            print(mydb)
            mycursor = mydb.cursor(buffered=True)

            if bus_type == "sleeper":
                busclass = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                busclass = "Bus_type LIKE '%A/c Semi Sleeper%'"
            elif bus_type=="A/C Seater":
                busclass = "Bus_type LIKE '%A/C Seater%'"
            elif bus_type=="NON A/C Seater":
                busclass = "Bus_type LIKE '%Non A/C Seater%'"
            else:
                busclass = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi Sleeper%' AND Bus_type NOT LIKE '%A/C Seater%' AND Bus_type NOT LIKE '%Non A/C Seater%' "
           
            if bus_fare == "10-300":
                fare_min, fare_max = 10, 300
            elif bus_fare == "301-500":
                fare_min, fare_max = 301, 500
            elif bus_fare == "501-700":
                fare_min, fare_max = 501, 700
            elif bus_fare == "701-1000":
                fare_min, fare_max = 701, 1000  
            elif bus_fare == "1001-1500":
                fare_min, fare_max = 1001, 1500
            elif bus_fare == "1501-2000":
                fare_min, fare_max = 1501, 2000
            else:
                fare_min, fare_max = 2001, 5000

            if pvt_pub == "public bus":
                busowner = "Bus_name LIKE '%SRTC%'"
            else:
                busowner = "Bus_name NOT LIKE '%SRTC%'"

            insert_query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{ap}"
                AND {busclass} AND {busowner} AND Start_time>='{time}'
                ORDER BY price and Start_time DESC
            '''
            mycursor.execute(insert_query)
            out=mycursor.fetchall()
            mydb.close()
            df = pd.DataFrame(out, columns=["ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Price", "Seats_Available", "Ratings", "Route_link", "Route_name"])
            return df

            
        df_result =bustype_busfare(t,f,o)
        st.dataframe(df_result)
        

    if s=="Bengal":
        ben=st.selectbox("Routes",lists_b)

        def bustype_busfare(bus_type,bus_fare,pvt_pub):
            mydb = mysql.connector.connect(host="localhost", user="root", password="Sql@10",database="redbus")
            print(mydb)
            mycursor = mydb.cursor(buffered=True)

            if bus_type == "sleeper":
                busclass = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                busclass = "Bus_type LIKE '%A/c Semi Sleeper%'"
            elif bus_type=="A/C Seater":
                busclass = "Bus_type LIKE '%A/C Seater%'"
            elif bus_type=="NON A/C Seater":
                busclass = "Bus_type LIKE '%Non A/C Seater%'"
            else:
                busclass = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi Sleeper%' AND Bus_type NOT LIKE '%A/C Seater%' AND Bus_type NOT LIKE '%Non A/C Seater%' "
           
            if bus_fare == "10-300":
                fare_min, fare_max = 10, 300
            elif bus_fare == "301-500":
                fare_min, fare_max = 301, 500
            elif bus_fare == "501-700":
                fare_min, fare_max = 501, 700
            elif bus_fare == "701-1000":
                fare_min, fare_max = 701, 1000  
            elif bus_fare == "1001-1500":
                fare_min, fare_max = 1001, 1500
            elif bus_fare == "1501-2000":
                fare_min, fare_max = 1501, 2000
            else:
                fare_min, fare_max = 2001, 5000

            if pvt_pub == "public bus":
                busowner = "Bus_name LIKE '%SRTC%'"
            else:
                busowner = "Bus_name NOT LIKE '%SRTC%'"

            insert_query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{ben}"
                AND {busclass} AND {busowner} AND Start_time>='{time}'
                ORDER BY price and Start_time DESC
            '''
            mycursor.execute(insert_query)
            out=mycursor.fetchall()
            mydb.close()
            df = pd.DataFrame(out, columns=["ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Price", "Seats_Available", "Ratings", "Route_link", "Route_name"])
            return df

            
        df_result =bustype_busfare(t,f,o)
        st.dataframe(df_result)


    if s=="Rajastan":
        raj=st.selectbox("Routes",lists_r)

        def bustype_busfare(bus_type,bus_fare,pvt_pub):
            mydb = mysql.connector.connect(host="localhost", user="root", password="Sql@10",database="redbus")
            print(mydb)
            mycursor = mydb.cursor(buffered=True)

            if bus_type == "sleeper":
                busclass = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                busclass = "Bus_type LIKE '%A/c Semi Sleeper%'"
            elif bus_type=="A/C Seater":
                busclass = "Bus_type LIKE '%A/C Seater%'"
            elif bus_type=="NON A/C Seater":
                busclass = "Bus_type LIKE '%Non A/C Seater%'"
            else:
                busclass = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi Sleeper%' AND Bus_type NOT LIKE '%A/C Seater%' AND Bus_type NOT LIKE '%Non A/C Seater%' "
           
            if bus_fare == "10-300":
                fare_min, fare_max = 10, 300
            elif bus_fare == "301-500":
                fare_min, fare_max = 301, 500
            elif bus_fare == "501-700":
                fare_min, fare_max = 501, 700
            elif bus_fare == "701-1000":
                fare_min, fare_max = 701, 1000  
            elif bus_fare == "1001-1500":
                fare_min, fare_max = 1001, 1500
            elif bus_fare == "1501-2000":
                fare_min, fare_max = 1501, 2000
            else:
                fare_min, fare_max = 2001, 5000

            if pvt_pub == "public bus":
                busowner = "Bus_name LIKE '%SRTC%'"
            else:
                busowner = "Bus_name NOT LIKE '%SRTC%'"

            insert_query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{raj}"
                AND {busclass} AND {busowner} AND Start_time>='{time}'
                ORDER BY price and Start_time DESC
            '''
            mycursor.execute(insert_query)
            out=mycursor.fetchall()
            mydb.close()
            df = pd.DataFrame(out, columns=["ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Price", "Seats_Available", "Ratings", "Route_link", "Route_name"])
            return df

            
        df_result =bustype_busfare(t,f,o)
        st.dataframe(df_result)

    if s=="West Bengal":
        wb=st.selectbox("Routes",lists_wb)

        def bustype_busfare(bus_type,bus_fare,pvt_pub):
            mydb = mysql.connector.connect(host="localhost", user="root", password="Sql@10",database="redbus")
            print(mydb)
            mycursor = mydb.cursor(buffered=True)

            if bus_type == "sleeper":
                busclass = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                busclass = "Bus_type LIKE '%A/c Semi Sleeper%'"
            elif bus_type=="A/C Seater":
                busclass = "Bus_type LIKE '%A/C Seater%'"
            elif bus_type=="NON A/C Seater":
                busclass = "Bus_type LIKE '%Non A/C Seater%'"
            else:
                busclass = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi Sleeper%' AND Bus_type NOT LIKE '%A/C Seater%' AND Bus_type NOT LIKE '%Non A/C Seater%' "
           
            if bus_fare == "10-300":
                fare_min, fare_max = 10, 300
            elif bus_fare == "301-500":
                fare_min, fare_max = 301, 500
            elif bus_fare == "501-700":
                fare_min, fare_max = 501, 700
            elif bus_fare == "701-1000":
                fare_min, fare_max = 701, 1000  
            elif bus_fare == "1001-1500":
                fare_min, fare_max = 1001, 1500
            elif bus_fare == "1501-2000":
                fare_min, fare_max = 1501, 2000
            else:
                fare_min, fare_max = 2001, 5000

            if pvt_pub == "public bus":
                busowner = "Bus_name LIKE '%SRTC%'"
            else:
                busowner = "Bus_name NOT LIKE '%SRTC%'"

            insert_query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{wb}"
                AND {busclass} AND {busowner} AND Start_time>='{time}'
                ORDER BY price and Start_time DESC
            '''
            mycursor.execute(insert_query)
            out=mycursor.fetchall()
            mydb.close()
            df = pd.DataFrame(out, columns=["ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Price", "Seats_Available", "Ratings", "Route_link", "Route_name"])
            return df

            
        df_result =bustype_busfare(t,f,o)
        st.dataframe(df_result)        


    if s=="Uttar Pradesh":
        up=st.selectbox("Routes",lists_up)

        def bustype_busfare(bus_type,bus_fare,pvt_pub):
            mydb = mysql.connector.connect(host="localhost", user="root", password="Sql@10",database="redbus")
            print(mydb)
            mycursor = mydb.cursor(buffered=True)

            if bus_type == "sleeper":
                busclass = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                busclass = "Bus_type LIKE '%A/c Semi Sleeper%'"
            elif bus_type=="A/C Seater":
                busclass = "Bus_type LIKE '%A/C Seater%'"
            elif bus_type=="NON A/C Seater":
                busclass = "Bus_type LIKE '%Non A/C Seater%'"
            else:
                busclass = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi Sleeper%' AND Bus_type NOT LIKE '%A/C Seater%' AND Bus_type NOT LIKE '%Non A/C Seater%' "
           
            if bus_fare == "10-300":
                fare_min, fare_max = 10, 300
            elif bus_fare == "301-500":
                fare_min, fare_max = 301, 500
            elif bus_fare == "501-700":
                fare_min, fare_max = 501, 700
            elif bus_fare == "701-1000":
                fare_min, fare_max = 701, 1000  
            elif bus_fare == "1001-1500":
                fare_min, fare_max = 1001, 1500
            elif bus_fare == "1501-2000":
                fare_min, fare_max = 1501, 2000
            else:
                fare_min, fare_max = 2001, 5000

            if pvt_pub == "public bus":
                busowner = "Bus_name LIKE '%SRTC%'"
            else:
                busowner = "Bus_name NOT LIKE '%SRTC%'"

            insert_query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{up}"
                AND {busclass} AND {busowner} AND Start_time>='{time}'
                ORDER BY price and Start_time DESC
            '''
            mycursor.execute(insert_query)
            out=mycursor.fetchall()
            mydb.close()
            df = pd.DataFrame(out, columns=["ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Price", "Seats_Available", "Ratings", "Route_link", "Route_name"])
            return df

            
        df_result =bustype_busfare(t,f,o)
        st.dataframe(df_result)

    if s=="Punjab":
        pun=st.selectbox("Routes",lists_p)

        def bustype_busfare(bus_type,bus_fare,pvt_pub):
            mydb = mysql.connector.connect(host="localhost", user="root", password="Sql@10",database="redbus")
            print(mydb)
            mycursor = mydb.cursor(buffered=True)

            if bus_type == "sleeper":
                busclass = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                busclass = "Bus_type LIKE '%A/c Semi Sleeper%'"
            elif bus_type=="A/C Seater":
                busclass = "Bus_type LIKE '%A/C Seater%'"
            elif bus_type=="NON A/C Seater":
                busclass = "Bus_type LIKE '%Non A/C Seater%'"
            else:
                busclass = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi Sleeper%' AND Bus_type NOT LIKE '%A/C Seater%' AND Bus_type NOT LIKE '%Non A/C Seater%' "
           
            if bus_fare == "10-300":
                fare_min, fare_max = 10, 300
            elif bus_fare == "301-500":
                fare_min, fare_max = 301, 500
            elif bus_fare == "501-700":
                fare_min, fare_max = 501, 700
            elif bus_fare == "701-1000":
                fare_min, fare_max = 701, 1000  
            elif bus_fare == "1001-1500":
                fare_min, fare_max = 1001, 1500
            elif bus_fare == "1501-2000":
                fare_min, fare_max = 1501, 2000
            else:
                fare_min, fare_max = 2001, 5000

            if pvt_pub == "public bus":
                busowner = "Bus_name LIKE '%SRTC%'"
            else:
                busowner = "Bus_name NOT LIKE '%SRTC%'"

            insert_query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{pun}"
                AND {busclass} AND {busowner} AND Start_time>='{time}'
                ORDER BY price and Start_time DESC
            '''
            mycursor.execute(insert_query)
            out=mycursor.fetchall()
            mydb.close()
            df = pd.DataFrame(out, columns=["ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Price", "Seats_Available", "Ratings", "Route_link", "Route_name"])
            return df

            
        df_result =bustype_busfare(t,f,o)
        st.dataframe(df_result)

    if s=="Himachal Pradesh":
        hp=st.selectbox("Routes",lists_hp)

        def bustype_busfare(bus_type,bus_fare,pvt_pub):
            mydb = mysql.connector.connect(host="localhost", user="root", password="Sql@10",database="redbus")
            print(mydb)
            mycursor = mydb.cursor(buffered=True)

            if bus_type == "sleeper":
                busclass = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                busclass = "Bus_type LIKE '%A/c Semi Sleeper%'"
            elif bus_type=="A/C Seater":
                busclass = "Bus_type LIKE '%A/C Seater%'"
            elif bus_type=="NON A/C Seater":
                busclass = "Bus_type LIKE '%Non A/C Seater%'"
            else:
                busclass = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi Sleeper%' AND Bus_type NOT LIKE '%A/C Seater%' AND Bus_type NOT LIKE '%Non A/C Seater%' "
           
            if bus_fare == "10-300":
                fare_min, fare_max = 10, 300
            elif bus_fare == "301-500":
                fare_min, fare_max = 301, 500
            elif bus_fare == "501-700":
                fare_min, fare_max = 501, 700
            elif bus_fare == "701-1000":
                fare_min, fare_max = 701, 1000  
            elif bus_fare == "1001-1500":
                fare_min, fare_max = 1001, 1500
            elif bus_fare == "1501-2000":
                fare_min, fare_max = 1501, 2000
            else:
                fare_min, fare_max = 2001, 5000

            if pvt_pub == "public bus":
                busowner = "Bus_name LIKE '%SRTC%'"
            else:
                busowner = "Bus_name NOT LIKE '%SRTC%'"

            insert_query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{hp}"
                AND {busclass} AND {busowner} AND Start_time>='{time}'
                ORDER BY price and Start_time DESC
            '''
            mycursor.execute(insert_query)
            out=mycursor.fetchall()
            mydb.close()
            df = pd.DataFrame(out, columns=["ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Price", "Seats_Available", "Ratings", "Route_link", "Route_name"])
            return df

            
        df_result =bustype_busfare(t,f,o)
        st.dataframe(df_result)    

    if s=="Chandigargh":
        chand=st.selectbox("Routes",lists_c)

        def bustype_busfare(bus_type,bus_fare,pvt_pub):
            mydb = mysql.connector.connect(host="localhost", user="root", password="Sql@10",database="redbus")
            print(mydb)
            mycursor = mydb.cursor(buffered=True)

            if bus_type == "sleeper":
                busclass = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                busclass = "Bus_type LIKE '%A/c Semi Sleeper%'"
            elif bus_type=="A/C Seater":
                busclass = "Bus_type LIKE '%A/C Seater%'"
            elif bus_type=="NON A/C Seater":
                busclass = "Bus_type LIKE '%Non A/C Seater%'"
            else:
                busclass = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi Sleeper%' AND Bus_type NOT LIKE '%A/C Seater%' AND Bus_type NOT LIKE '%Non A/C Seater%' "
           
            if bus_fare == "10-300":
                fare_min, fare_max = 10, 300
            elif bus_fare == "301-500":
                fare_min, fare_max = 301, 500
            elif bus_fare == "501-700":
                fare_min, fare_max = 501, 700
            elif bus_fare == "701-1000":
                fare_min, fare_max = 701, 1000  
            elif bus_fare == "1001-1500":
                fare_min, fare_max = 1001, 1500
            elif bus_fare == "1501-2000":
                fare_min, fare_max = 1501, 2000
            else:
                fare_min, fare_max = 2001, 5000

            if pvt_pub == "public bus":
                busowner = "Bus_name LIKE '%SRTC%'"
            else:
                busowner = "Bus_name NOT LIKE '%SRTC%'"

            insert_query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{chand}"
                AND {busclass} AND {busowner} AND Start_time>='{time}'
                ORDER BY price and Start_time DESC
            '''
            mycursor.execute(insert_query)
            out=mycursor.fetchall()
            mydb.close()
            df = pd.DataFrame(out, columns=["ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Price", "Seats_Available", "Ratings", "Route_link", "Route_name"])
            return df

            
        df_result =bustype_busfare(t,f,o)
        st.dataframe(df_result)    


if opt == "Account":
    st.title("Your Account")
    st.write("Manage your account details here. Update personal information, change password, and more.")
    st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    st.button("Submit")
    st.button("Forgot password?")
    

if opt == "Helpline":
    st.image("C:/Users/anbar/OneDrive/Pictures/Screenshots/t1.png")
    st.title("Customer Care")
    st.write("Our customer care team is here to help you. Reach out to us for support with bookings, refunds, or any other queries.")
    st.write("Contact us at: redbus@bus.com")
    st.write("Phone: +91 1234567890")

if opt == "Career":
    st.title("Career Opportunities")
    st.write("Join our team and help us make bus travel better. Explore current job openings and apply to become a part of our dynamic team.")
    st.link_button("current openings",'https://www.redbus.in/careers/')

if opt == "About us":
    st.title("About Us")
    st.write("Learn more about RedBus. Discover our mission, values, and the team behind the platform.")
    st.write("RedBus is India’s largest online bus ticketing platform that has transformed bus travel in the country by bringing ease and convenience to millions of Indians who travel using buses. Founded in 2006, redBus is part of India’s leading online travel company MakeMyTrip Limited (NASDAQ: MMYT). By providing widest choice, superior customer service, lowest prices and unmatched benefits, redBus has served over 18 million customers. redBus has a global presence with operations across Indonesia, Singapore, Malaysia, Colombia and Peru apart from India.")