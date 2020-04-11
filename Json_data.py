import requests
import dateutil.parser
from datetime import (datetime, timedelta)


def is_list_hourly(time_list):
        flag = True
        for i in range(0, len(time_list)):
                if i + 1 == len(time_list):
                        break

                diff = get_time_diff_mins(time_list[i], time_list[i + 1])
                flag = is_time_diff_valid(diff)
                if flag == False:
                        break
        return flag



def get_time_diff_mins(time_1, time_2):
        time_diff = time_1 - time_2
        time_diff_day_mins = time_diff.days * 24 * 60
        time_diff_secs_mins = divmod(time_diff.seconds, 60)[0]
        time_diff_total = time_diff_day_mins + time_diff_secs_mins
        return time_diff_total


def is_time_diff_valid(time_diff):
        if time_diff == 60:
                return True

        return False


def get_openweather_response():     # Getting response from API
        req = requests.get("https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us&appid=b6907d289e10d714a6e88b30761fae22")


        if req.status_code == 200:
                return  req.json()

        else:
                print("Invalid Response  ::: Status Code "+str(req.status_code))
                return None


def validate_temperature(data):  # Validating temp should not be less than temp_min and not more than temp_max
        for list in data['list']:
                if list["main"]['temp_min'] <=list["main"]["temp"] and list["main"]["temp"]<=list["main"]["temp_max"]:
                        return True

                else:
                        print("Exact_Temp=" ,list['main']["temp"], " Min_Temp=",list["main"]["temp_min"]," Max_temp=",list["main"]["temp_max"])
                        return False
def validate_weather_desc(data):    #the weather id is 500, the description should be light rain and if the weather id is 800, the description should be a clear sky
        Weather_list=[]

        for list in data['list']:
                for weather in list['weather']:
                        if weather['id'] ==500:
                                weather['description']=='light rain'
                                Weather_list.append("500:light rain")
                        elif weather['id']==800:
                                weather['description'] == 'clear sky'
                                Weather_list.append("800: clear sky")
        print("Test_Case 4/5: " + "Weather_id/Description: ", Weather_list ,"\n")

def validate_four_days_response(data):  #Validating response contains 4 days of data

        day=[]
        for list in data['list']:
                day.append((dateutil.parser.parse(list['dt_txt']).date()))
        day1=set(day)
        if len(day1)>=4:
                print("Test_Case 1: " + "The response contains 4 or more than 4 days of data: ", day1,"\n")
        else:
                print("The response does not contains 4 days of data")


def validate_hourly_interval(data):   #Validating forecast in the hourly interval
        date_dict={}
        for obj in data['list']:
                key = str(dateutil.parser.parse(obj['dt_txt']).date())

                if date_dict.get(key) is None:
                        date_dict[key] = []

                date_dict[key].append(dateutil.parser.parse(obj['dt_txt']))

        for x in date_dict.values():
                x.sort(reverse=True)
                flag = is_list_hourly(x)

                if flag == True:
                        # list returned is valid hourly
                        return  True
                else :
                        #list returned is not valid hourly
                        return
                        print("Forecast is not in hourly interval")

def main():
        data = get_openweather_response()

        if data is None:
                return
        validate_four_days_response(data)
        if validate_hourly_interval(data):
                print("Test_Case 2: " + "Forecast is in hourly_Interval\n")
        if validate_temperature(data):
                print("Test_Case 3: " + "Valid Temp is present in the response : between temp_min and temp_max\n")
        validate_weather_desc(data)



if __name__ == "__main__" :
        main()










