import tkinter
import plotly.graph_objects as go

import plotly.graph_objects as go
from tkinter import *
import requests

class usbankgui(tkinter.Tk):
    def __init__(self, master):
        self.master = master
        master.title('Spiff')

        checkingAmount, savingsAmount = self.retieveAccountAmounts()

        self.label = Label(master, text="Welcome US Bank user!\nYou have $%s in checking.\nYou have $%s in savings." % (checkingAmount, savingsAmount))#enter welcome message
        self.label.pack()

        self.piechart_button = Button(master, text='My Spending', command=self.piechart)
        self.piechart_button.pack()

        self.map_button = Button(master, text="Map", command=self.mapTime)
        self.map_button.pack()

        self.close_button = Button(master, text='close', command=self.master.quit)
        self.close_button.pack()

    def piechart(self):

        transactions = []
        amountSpent = []

        response = self.getAPITransData()

        for transaction in response.json()["TransactionList"]:
                transactions.append(transaction["Description1"])
                amountSpent.append(float(transaction["PostedAmount"]))

        fig = go.Figure(data=[go.Pie(labels=transactions, values=amountSpent)])
        fig.show()

    def mapTime(self):
        token = "pk.eyJ1IjoiYXpoZHJha2UiLCJhIjoiY2sweThta2ZzMGRlYzNjbWl6a3NtOWZiOSJ9.3Uf0fpWgUzCmSZxHaVIu2w"
        fig = go.Figure(go.Scattermapbox(
            lat=[44.9724,44.9748819,44.9507527],
            lon=[-93.2835,-93.2742919,-93.2375519],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9
            ),
            hovertemplate=['<b>Minneapolis College Bookstore</b><br>'
                          'Systems Analysis and Design in a Changing World: $225.99<br>'
                          'HTML and CSS_ Design and Build Websites: $50.00',
                           '<b>Target</b><br>'
                           'Transaction: $4.13',
                           '<b>Cub Foods</b><br>'
                           'Food Time: $102.50<br>'
                           'Food Time, 2!: $6.12',
                           ],
        ))

        fig.update_layout(
            autosize=True,
            hovermode='closest',
            mapbox=go.layout.Mapbox(
                accesstoken=token,
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=44.9778,
                    lon=-93.2650
                ),
                pitch=0,
                zoom=12
            ),
        )

        fig.show()

    def retieveAccountAmounts(self):
        checkingBalance = 0
        savingBalance = 0

        response = self.getAPIAccountData()

        for item in response.json()["AccessibleAccountDetailList"]:
            if item["BasicAccountDetail"]["Codes"]["CategoryCode"] == "CHCK":
                checkingBalance = (item["BasicAccountDetail"]["Balances"]["CurrentBalanceAmount"])
            elif item["BasicAccountDetail"]["Codes"]["CategoryCode"] == "SAVG":
                savingBalance = (item["BasicAccountDetail"]["Balances"]["CurrentBalanceAmount"])

        return checkingBalance, savingBalance

    def getAPIAccountData(self):
        url = "https://alpha-api.usbank.com/innovations/v1/user/accounts"

        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"LegalParticipantIdentifier\"\r\n\r\n000995928731567433\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'apiKey': "nse93RFFDcFnaAq4sqqDylZ7jtH6PzmY",
            'User-Agent': "PostmanRuntime/7.17.1",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Postman-Token': "0e34c55a-e98c-4110-84b3-83a3e009f345,89793c4a-f7df-454d-a840-1491af30de09",
            'Host': "alpha-api.usbank.com",
            'Accept-Encoding': "gzip, deflate",
            'Content-Length': "199",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        return requests.request("POST", url, data=payload, headers=headers)

    def getAPITransData(self):
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

        return requests.request("POST", url, data=payload, headers=headers, params=querystring)
