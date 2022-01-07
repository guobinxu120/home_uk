import csv

bedroom_type = "3 Bedrooms"
room_type = "Terraced"
bill_type = "Yes"

wanted = {}
with open('wanted.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        wanted[row['city']]= row['location']

rent = {}
with open('rent.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        rent[row['city']] = row['location']

rooms = {}
with open('average1.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Type'] == bedroom_type:
            rooms[row['Code']] = row

median = {}
with open('median1.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Type'] == room_type:
            median[row['Code']] = row

districts = {}
with open('Postcode_districts.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        districts[row[0]] = row



# taks = {}
# output = 'task1_1.csv'
# csvfile = open(output.replace(' ','_'), 'wb')
# spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
# header = ['Postal Code','Town_Area', 'Region','Room size','Bills included','Average (median)','Avg min','Avg max']
# spamwriter.writerow(header)
# flag = True
# with open('task1_2.csv') as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         tep_row = []
#         for val in row:
#             tep_row.append(val)
#         tep_row.pop(2)
#         tep_row.insert(2,'')
#         if row[0] in districts.keys():
#             region = districts[row[0]][2]
#             if tep_row[1].lower() in districts[row[0]][1].lower():
#                 tep_row[2] = region
#
#         spamwriter.writerow(tep_row)
#         # print(row['Postal Code'])
#         # else:
#         #     tep_row = [row['Postal Code'],  '', row['Neighbourhood']]
#         #     for i, key in enumerate(row.keys()):
#         #         if key == 'Postal Code' or key == 'Neighbourhood' or key == 'Postcode': continue
#         #         tep_row.append(row[key])
#         #     spamwriter.writerow(tep_row)
# csvfile.close()



task1 = []
output = 'output/' + bedroom_type+' ' +room_type + ' ' + bill_type +'.csv'
csvfile = open(output.replace(' ','_'), 'wb')
spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
spamwriter.writerow(['Postal Code','Town_Area','Region','Room size','Bills included','Average (median)',
                     'Avg min','Avg max','_StartTime','_EndTime','StartTime_Room','EndTime_Room','Type_Room','Change_Room',
                     'StartTime','EndTime','Type','Change','Wanted','Rent'])


with open('task1.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile)
    j = 0
    for row1 in spamreader:
        if j==0:
            j+= 1
            continue


        row = []
        for key in row1:
            row.append(key)

        if bill_type != "" and bill_type != row[4]: continue

        if row[0] in rooms.keys():
            for i, val in enumerate(rooms[row[0]].values()):
                if i==0: continue
                row.append(val)
        else:
            row.extend(['','','','','', ''])

        if row[0] in median.keys():
            for i, val in enumerate(median[row[0]].values()):
                if i< 3: continue
                row.append(val)
        else:
            row.extend(['','','',''])

        if row[0] in wanted.keys():
            row.append(wanted[row[0]])
        else:
            row.append('')

        if row[0] in rent.keys():
            row.append(rent[row[0]])
        else:
            row.append('')

        spamwriter.writerow(row)
