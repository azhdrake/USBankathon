import plotly.graph_objects as go
from tkinter import Tk, Label, Button
import requests

class usbankgui:
    def __init__(self, master):
        self.master = master
        master.title('INSERT TITLE OF APP')#put in title

        self.label = Label(master, text="Welcome Message")#enter welcome message
        self.label.pack()

        self.piechart_button = Button(master, text='My Spending', command=self.piechart)
        self.piechart_button.pack()

        self.close_button = Button(master, text='close', command=self.master.quit)
        self.close_button.pack()

    def piechart(self):
            url = "https://alpha-api.usbank.com/innovations/v1/account/transactions"

            querystring = {"": ""}

            payload = "{\n \"OperatingCompanyIdentifier\": \"424\",\n    \"ProductCode\": \"DDA\",\n    \"PrimaryIdentifier\": \"00000000000148725876996\"\n}"
            headers = {
                    'Content-Type': "application/json",
                    'apiKey': "nse93RFFDcFnaAq4sqqDylZ7jtH6PzmY",
                    'User-Agent': "PostmanRuntime/7.17.1",
                    'Accept': "*/*",
                    'Cache-Control': "no-cache",
                    'Postman-Token': "8d9defa1-6dc9-40b6-bf03-567aab2d4712,116f5112-52f1-48f9-bd09-2345ee9575e8",
                    'Host': "alpha-api.usbank.com",
                    'Accept-Encoding': "gzip, deflate",
                    'Content-Length': "118",
                    'Connection': "keep-alive",
                    'cache-control': "no-cache"
            }

            response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
            transactions = []
            amountSpent = []

            for transaction in response.json()["TransactionList"]:
                    transactions.append(transaction["Description1"])
                    amountSpent.append(float(transaction["PostedAmount"]))

            fig = go.Figure(data=[go.Pie(labels=transactions, values=amountSpent)])
            fig.show()

