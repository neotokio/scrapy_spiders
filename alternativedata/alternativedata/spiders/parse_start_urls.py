import json
import csv

#Link to parse JSON urls from, used in scrapy spider in start_urls parameter.
#https://alternativedata.org/wp-json/wp/v2/data-providers?_embed=true&per_page=999&page=1&provider=data-providers

with open('/home/user/Download/data-providers.json') as access_json:
   read_content = json.load(access_json)
   outputFile = open("ConvertedJSON.csv", "w")
   outputWriter = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
   outputWriter.writerow(["Name","Date","Link","Employees","Year"])

for var in read_content:
  link_holder = []
  link_holder.append(var["link"]
  outputWriter.writerow([link_holder])


  #title_holder = []
  #date_holder = []
  #employes_holder = []
  #founded_holder = []
  #client_holder = []
  #sectors_holder = []
  #hq_holder = []
  #funding_holder = []
  #title_holder.append(var["title"]["rendered"])
  #link_holder.append(var["acf"]["website"])
  #date_holder.append(var["date"])
  #employes_holder.append(var["acf"]["employees"])
  #founded_holder.append(var["acf"]["founded"])
  #client_holder.append(var["acf"]["client_focus"])
  #hq_holder.append(var["acf"]["headquaters"])
  #funding_holder.append(var["acf"]["funding"])
  #print "Name of company:", title_holder, "Date added:", date_holder, "Link:", link_holder, "Employes:", employes_holder, "Year Funded:", founded_holder
  #outputWriter.writerow([title_holder,date_holder,link_holder,employes_holder,founded_holder])
