import requests
import time
import json
from bs4 import BeautifulSoup
import threading
import re
from dhooks import Webhook
from time import time, sleep
from discord_webhook import DiscordWebhook, DiscordEmbed


hook = Webhook("https://discord.com/api/webhooks/795450641114857502/EN1I9-QexxVO-fR7eOF39VN0ckMJqn1hd8CzPNK-N3aAdqkN5U40-eCy3wAPENf1_E5P")
webhook = DiscordWebhook(url ='https://discord.com/api/webhooks/795450641114857502/EN1I9-QexxVO-fR7eOF39VN0ckMJqn1hd8CzPNK-N3aAdqkN5U40-eCy3wAPENf1_E5P')
CounterUpdates = 0

embedsDict = {}

class shoeVariable():

      def __init__(self, p_name, p_date, p_nikePageURL, p_SQU, p_retail, p_stockXsearch):
            self.name = p_name
            self.date = p_date
            self.squ = p_SQU
            self.retail = p_retail
            self.page = p_nikePageURL
            self.stockXSearchLink = p_stockXsearch

      def printShoe(self):

            hook.send("----------------------------------------------------------------------------------------------------------------" + "\n" + "Product Name: " + self.name + "\n" +  "Date: " + self.date[:3] + " " + self.date[3:] + "\n" + "Nike page: "+self.page + "\n" + "SQU: " + str(self.squ) +"\n" +  "Retail: " + str(self.retail) + "\n" + "StockXLinkSearch: " + self.stockXSearchLink)
            #embedsDict[self.name] = DiscordEmbed(title= self.name, description= self.date[:3] + " " + self.date[3:], color=242424)
            #embedsDict[self.name].add_embed_field(name = 'Retail', value = self.retail)
            #embedsDict[self.name].add_embed_field(name = 'Retail', value = self.retail)
            #embedsDict[self.name].add_embed_field(name = 'Nike Page', value = self.page)
            #embedsDict[self.name].add_embed_field(name = 'Stock X Search', value = self.stockXSearchLink)
            #embedsDict[self.name].add_embed_field(name = 'SQU', value = self.squ)
            sleep(1)
            #webhook.add_embed(embedsDict[self.name])
            #response = webhook.execute()


                       
      def updateNikepage(self, NikePage):
            self.page = NikePage
            p_nikePageURL = NikePage

      def updateRetailprice(self, newprice):
            self.retail = newprice
            p_retail = newprice

      def updateSQU(self, newSQU):
            self.squ = newSQU
            p_SQU = newSQU

      def updatestockXLink(self, newstocklink):
            self.stockXSearchLink = newstocklink
            p_stockXsearch = newstocklink




def monitor():

      counter = 0
      counter2 = 0
      i = 0
      months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
      shoesInv = {}     



      url = 'https://www.nike.com/launch?cp=65052578087_search_%7Cnike%20snkrs%7Cg%7C11856077755%7C115377939556%7Ce%7Cc&s=upcoming'
      headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}

      runWeb = requests.get(url, headers = headers)
      
      soup = BeautifulSoup(runWeb.content, 'html.parser')


      for shoeVars in soup.find_all( class_='ncss-col-sm-12 full'):
            if(shoeVars.get_text().lower().startswith(tuple(months))):
                  counter+=1
                  if(shoeVars.get_text()[5].isdigit()):
                        shoesInv[str(i)] = shoeVariable(shoeVars.get_text()[5:], shoeVars.get_text()[:5],"" ,"SQU 123", "", "")
                  else:
                        shoesInv[str(i)] = shoeVariable(shoeVars.get_text()[4:], shoeVars.get_text()[:4],"" ,"SQU 123", "", "")
                  i+=1

      for link in soup.findAll('a'):
            if(link.get('href').startswith("/launch/t/")):

                  url = "https://www.nike.com" + link.get('href')
                  headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}

                  childShoePage = requests.get(url, headers = headers)
      
                  parserGuy = BeautifulSoup(childShoePage.content, 'html.parser')

                  shoesInv.get(str(counter2)).updateNikepage(url)
                  shoesInv.get(str(counter2)).updateRetailprice(parserGuy.find(class_ = "headline-5 pb6-sm fs14-sm fs16-md").get_text())
                  shoesInv.get(str(counter2)).updateSQU(parserGuy.find('p').get_text()[-10:])
                  shoesInv.get(str(counter2)).updatestockXLink("https://stockx.com/search/sneakers?s=" + shoesInv.get(str(counter2)).squ)

                  #shoeVars.get_text()[4:]
                  counter2+= 1
            if(counter2 >= counter):
                  break
      printShoestock(shoesInv)

      sleep(1000)
      #deleteAllHooks(shoesInv)
      monitor()

def printShoestock(shoesDict):
      keys = list(shoesDict.keys())
      for key in keys:
            shoesDict.get(key).printShoe()

def deleteAllHooks(shoesDict):
      keys = list(shoesDict.keys())
      for key in keys:
            shoesDict.get(key).delete()

monitor()
