
import psycopg2 
from datetime import date, datetime
import json


hostname = 'caworks.csfqincyfecb.us-east-2.rds.amazonaws.com'
username = 'sarciadmin'
password = 'sarci-123'
database = 'caworksprod'

dbconnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

def retrieveData( conn,query,data ) :
    cur = conn.cursor()
    cur.execute(query,data)
    items =[]
    for rows in cur.fetchall() :
        
        for index in range(0,len(rows)-1):
            if isinstance(rows[index], (datetime,date)):
                rows[index] = rows[index].__str__()
                
        items.append(rows)
    cur.close()
    return items
    

def authorizeUser(orgid,phonenumber):
    serviceid = 1
    
    # authorization rules
    # 1. phonenumber should be mapped to org
    # 2. org should me mapped to service
    
    # For now making an assumption that all users can access 
    # all services subscribed by their org. 
    
    phonenumber = phonenumber.replace("+","")
    statusCode = 400
    
    try:
        fetchServiceIdQuery  =  """select serviceid from subscriptions."SUBSCRIBERS"
                                 where orgid = %s ;"""
            
        userdetails = (orgid,)
        returndata = retrieveData( dbconnection, fetchServiceIdQuery, userdetails )
        print("return data is {}".format(returndata))
        print(serviceid in returndata[0])
        if serviceid in returndata[0]:
            statusCode = 200
        else:
            statusCode = 401 # not authorized
         
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        statusCode = 500 #error
    
    print("status code is {}".format(statusCode))
    return statusCode
        
    
      
    
    