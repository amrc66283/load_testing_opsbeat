import requests
import json

url = "https://leadgen-api.dglide.com/api/v1/table/ticket/data/save"
payload = json.dumps({
  "uuid": "00072dff-7a0e-457d-b7a8-87a6c422aab1",
  "ticketid": "TKT17025",
  "requester": "000969b2-a59b-4de6-a6aa-8f92494a0ec6",
  "subject": "Check-in Process Improvement11",
  "type": "1",
  "source": "2",
  "status": "1",
  "invalid_ticket": "1",
  "priority": "1",
  "group": "ea46757f-a68b-4877-bbb6-c924fccc9c2a",
  "agent": "30b6e2b2-691e-49b9-a279-a480d881e298",
  "description": "e3lmdedeqqq",
  "terminal": "Terminal 1",
  "complainer_type": "1",
  "airport": "Terminal 1",
  "area": "International Gate G",
  "level": "Level 4",
  "category": "Security",
  "subcategory": "LAG restrictions",
  "pending_actions": 1
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJzeXNhZG1pbkBleGFtcGxlLmNvbSIsImV4cCI6MTcyODk3NDA1NSwiaWF0IjoxNzI4OTcwNDU1fQ.PlTDdHtdrMAHBjY7BoM57T9q_j79PGUfofOuy6asRGtWcLvkVnjn0Zk6X4aZGs5HYyFUgg9DP8KyJv550zC9Ug'
}

# Open the text file in write mode
with open('api_responses.txt', 'w') as file:
    for i in range(100):
        # Send the request
        response = requests.request("POST", url, headers=headers, data=payload)
        # Write each response on a new line in the file
        file.write(response.text + '\n')
        print(f"Response Code: {response.status_code}")

print("API calls completed and responses saved to api_responses.txt")
