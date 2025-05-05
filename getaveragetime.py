import os
from datetime import datetime
import time
dic = {}
for filename in os.listdir("logs"):
# if True:
#     filename = "RandomvsRandom.txt"
    file_path = os.path.join("logs", filename)
    filename = filename.split(".")[0]
    if os.path.isfile(file_path):
        av = []
        dic[filename] = {}
        with open(file_path) as file:
            for line in file:
                ar = line[:-1].split("took ")
                if len(ar) == 2:
                    # print(ar)
                    hms = ar[1].split(":")
                    seconds = int(hms[1]) * 60 + float(hms[2])

                    av.append(seconds)
                    # print(seconds)
                elif ": " in line:
                    ar = line[:-1].split(": ")
                    ar2 = ar[0].split(" ")
                    if len(ar2) == 2:
                        key = ar2[0].lower() + ar2[1].capitalize()
                    else:
                        key = ar2[0].lower()
                    dic[filename][key] = int(ar[1])      

        average = sum(av)/len(av)
        # print(f"Each game in {filename} took {average} seconds on average")
        dic[filename]["avgTime"] = average
        dic[filename]["minTime"] = min(av)
        dic[filename]["maxTime"] = max(av)

# for str in ["min", "max", "avg"]:
#     sort = str + "Time"
#     sorted_dict = dict(sorted(dic.items(), key=lambda item: item[1][sort]))
#     for key in sorted_dict:
#         print(f"Each game in {key} took {sorted_dict[key][sort]} seconds on {sort}")
sorted_dict = dict(sorted(dic.items(), key=lambda item: item[1]["avgTime"]))
for key in sorted_dict:
    print(f"Each game in {key} took {sorted_dict[key]["avgTime"]} seconds on average")

for str in ["White Wins", "Black Wins", "Ties"]:
    ar = str.split(" ")
    if len(ar) == 2:
        sort = ar[0].lower() + ar[1]
    else:
        sort = ar[0].lower()
    sorted_dict = dict(sorted(dic.items(), key=lambda item: item[1][sort]))
    for key in sorted_dict:
        print(f"Games {key} had {sorted_dict[key][sort]} {str}")

print(dic)

