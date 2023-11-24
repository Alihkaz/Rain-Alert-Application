#

import requests
from twilio.rest import client 
from twilio.http.http_client import TwilioHttpClient
import os

proxy_client=TwilioHttpClient()
proxy_client.session.proxies={'https': (' YOUR https_proxy')}# here we created the proxy server in order to tell the twilio api where to run the code in it ,
                                                             # to avoid the connection error 
                                                             # , since we are using the free version of the twilio app ! 


account_sid= "YOUR ACCOUNT SID FROM TWILIO"
auth_token= " YOUR AUTH_TOKEN" # we can get from the twilio dashboard and the environ stabds for the environment variables where the secret ket is stored there and hidden from the public !


My_lat="YOUR LATITUDE"
My_lng="YOUR LANGITUDE"


parameters={

  "lat": My_lat,
  "lng":My_lng,
  "appid": ("YOUR OWM_API_KEY"),
  "exclude": "current,minutely,daily"
  #this parameter will remove some items from the data bringed by the api , were we are interested only by the hourly data .it makes the dic more simpler 

  
}


response=requests.get(url="https://api.openweathermap.org/data/2.5/onecall",params=parameters)


response.raise_for_status()


data=response.json()

# if we put the data from the console on a json data viewer , it will give us hours , lat , lon, timezone ,
#  and more data , what we care about is the weather data of the hours , so we should expand the hours ,
#  and get weather informations like temp , pressure , humidity , and much more .


weather_condions=[]

hours_list=(data["hourly"])[0:12]#extracting only 12 hours from the list hours through slicing 


for list in hours_list:
  weather_condition=int(list["weather"][0]["id"])
  weather_condions.append(weather_condition)


# sending the alert via SMS:

for condition in weather_condions :
  if condition < 700 :# its a code used in weather science which indicates the weather condition . 
    client=Client(account_sid,auth_token,http_client=proxy_client)
    message=client.messages\
        .create(
          body =" Its going to rain , bring an umbrella ☔️",
          from ="phone number we get from twilio", 
          to ="the phone number we want to send to it , and it should be a verified phone number",
        )


print(message.status)# to check if the message is sended succefully . 







#DESCRIPTIONS:

# hourly is a list inside the dictionary data , so to access to the hourly weather data , we just say data["hourly"]
#  hourly list contains 48 items , which represents the number of hours 
# these items are dictionaries , so each item is hour , formatted as dictionary that contains keys and values 
# ! and we will have 48 dictionary ! and if we want just to call and see the condition of the first hour ,
#  we call [hourly], then act with it as a list [hourly][0]
#inside this item which is a dictionary , we will call the weather list , which also contains items
# as exception , that list contains only one item , so we call it by :  [hourly][0]["weather"][0]
#thyat first item is a dictionary , which contains keys and value ,
#  and we can work with them as we want ,
#  here we want to use the id , so we call it by :  [hourly][0]["weather"][0]["id"], its very correct to my version bellow 
#through slicing we didnot change the content , we just let the first list we want to work with less smaller , then we want to loop through all of the lists 
# , and apply the same process of extraction the id , we didnot change any method for the id path , we just saved the first part as  hours_list!



