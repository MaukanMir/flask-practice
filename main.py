import requests, json

URL = "https://us-central1-marcy-playground.cloudfunctions.net/ordoroCodingTest"
info = requests.get(URL).json()

def clean_data(info):
    unique_emails, april_emails, user_domain_counts = set(), [], {}

    if info is not None:
        check = info['data']

        for block in check:
            #Depending on the context, some companies reject data if either field contains null values. If Ordoro only wanted data that contained no null values. I would use this if condition, however if they wanted those values regardless. I would implement the following logic after this if commented out if statement.
            
            # if not block['email'] or not block['login_date']:
            #     continue

            #Clean data and use variables as check points
            email_check = block["email"].strip() if block["email"] else None
            login_check = block["login_date"].strip() if block["login_date"] else None
            domain_check = block["email"].strip().split("@")[1] if block["email"] else None

            if email_check and email_check not in unique_emails:
                unique_emails.add(email_check)

            if email_check and login_check and login_check[5:7] == '04':
                april_emails.append(email_check)

                # In the post example of the API, it asks the user to send a list of emails for users in april. However in the directions, it asks for a list of users that logged in for the month of april normailized to the UTC timezone. I was not sure how I was supposed to send the data so I decided to show you both ways. In the commented out code below this. I would send back the april emails users and the login_dates formatted as such in a dictionary object. I was not sure if this is what was desired based off the post request example but I wanted to showcase the option.

                # april_emails.append({"email": email_check, "login_date": login_check[:19] + "Z"})

            #Increment user_domain_count by 1
            user_domain_counts[domain_check] = user_domain_counts.get(domain_check, 0) + 1

    return [list(unique_emails), april_emails, user_domain_counts]


def postRequest(URL,info):
    unique_emails, april_emails, user_domain_counts = clean_data(info)

    sendingData = {
        "your_email_address": "engineermaukan@gmail.com",
        "unique_emails": unique_emails,
        "user_domain_counts": user_domain_counts,
        "april_emails": april_emails
    }
    
    result = json.dumps(sendingData, indent=4)

    # print(result)

    final = requests.post(URL +"/post", data=result)

    print(f'response from server:{final.status_code}')

    print(final.json())

postRequest(URL, info)


#<------- Space and Time Complexity: = O(N) and O(N) ------->:

#I loop through the data one time during the process, I make O(n) operations, the most intensive compute costs are checking through the dict if a potential key is already in the dict, this is also comparable with the lists. I split up the data in three different containers and call the function in the post request, splitting all three containers into three different variables. Now since I am only doing two steps, I thought about using async to decrease the cost of my operations but since I am only applying two different processes one time, in a get request and post request I decided against the added complexity. If there were multiple operations that depened on each other I would invoke using async as this would drastically improve the speed of my application.

#<------- Time Spent: 1 Hour ------->:
#This program took me 1 hour to work through the logic, unfortunately I could not make a succesful post request. If you uncomment the "print(result)" line above, you will see that the structure is identical to the post request example. Most likely there is something I am doing incorrectly, I was not sure what was the correct url to make the post request on. I tried a backslash "/post" or "/POST" but was still receiving an error. My apologies if this is not what you asked for. I spent about another three hours trying to figure out what might the issue be.


