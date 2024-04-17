import re
import pandas as pd
import os

folder = "campaigns"
results = pd.DataFrame()

for file in os.listdir(folder):
    filename = os.path.abspath(f"{folder}/{file}")
    cols = dict()
    mode = 't'
    with open(filename) as campaign:
        details = campaign.readlines()
        for line in details:
            # Flag to read alternate format
            if line == '"Clicks by URL"\n':
                mode = 'u'
                continue

            if mode == 't':
                deets = line.split('","', 1)
                # If the split by comma is more than 2 it denotes a statistic
                if len(deets) > 1:
                    rowname = deets[0].replace('"', "").rstrip("\n")
                    # Title split
                    if rowname == "Title:":
                        title_name = deets[1].rstrip("\n").replace('"', "").split()
                        semester = title_name[0].replace("Sem", "Semester ")
                        week = title_name[1].replace("Wk", "Week ")
                        if semester == "General":
                            semester = "Semester 1"
                            week = "General Meeting"

                        cols.update({"Semester": semester})
                        cols.update({"Week": week})
                    else:
                        value = deets[1].replace('"', "").rstrip("\n")
                        cols.update({rowname: value})


            else:
                deets = line.split('","', 2)
                url = deets[0]
                url = url.replace("https://", "")
                url = url.replace('"', "")
                if len(url.split('.')) > 1:
                    website = url.split('.')[1].capitalize().replace('"', "")
                    total = deets[1].rstrip("\n").capitalize().replace('"', "")
                    unique = deets[2].rstrip("\n").capitalize().replace('"', "")
                    if website == "Facebook" or website == "Instagram" or website == "Google":
                        cols.update({f"{website} Total" : total})
                        cols.update({f"{website} Unique" : unique})
                    
    new_df = pd.DataFrame(cols, index = [0])
    results = pd.concat([results, new_df], ignore_index = True)

results.to_csv("test.csv", index=False)