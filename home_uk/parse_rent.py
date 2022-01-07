import csv

bedroom_type = "Three bedrooms"
median_type = ""
average_type = "2 Bedrooms"

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
with open('average4.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Type'] == bedroom_type:
            rooms[row['Code']] = row

districts = {}
with open('Postcode_districts.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        districts[row[0]] = row




if median_type != '':

    task1 = []
    output = 'output/' + bedroom_type + '_{}_rent'.format(median_type) + '.csv'
    csvfile = open(output.replace(' ', '_'), 'wb')
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(
        ['Postal Code', 'Town/Area', 'Region', '_StartTime', '_EndTime', 'StartTime', 'EndTime', 'Type', 'Change'
            , 'Average ToM', 'Median rent', 'Average rent', 'Type', 'properties', 'Wanted', 'Rent'])

    with open('median1.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        j = 0
        for row1 in spamreader:
            if j==0:
                j+= 1
                continue
            row = []
            if row1[5] != median_type: continue

            if row1[0] in districts.keys():
                row.extend(districts[row1[0]])
            else:
                row.extend([row1[1], '', ''])

            for i, key in enumerate(row1):
                if i == 0: continue
                row.append(key)

            if row[0] in rooms.keys():
                for i, val in enumerate(rooms[row[0]].values()):
                    if i == 1: continue
                    row.append(val)
            else:
                row.extend(['','','','',''])

            if row[0] in wanted.keys():
                row.append(wanted[row[0]])
            else:
                row.append('')

            if row[0] in rent.keys():
                row.append(rent[row[0]])
            else:
                row.append('')

            spamwriter.writerow(row)

elif average_type != "":
    task1 = []
    output = 'output/' + bedroom_type + '_{}_rent'.format(average_type) + '.csv'
    csvfile = open(output.replace(' ', '_'), 'wb')
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(
        ['Postal Code', 'Town/Area', 'Region', '_StartTime', '_EndTime', 'StartTime', 'EndTime', 'Type', 'Change'
            , 'Average ToM', 'Median rent', 'Average rent', 'Type', 'properties', 'Wanted', 'Rent'])

    with open('average1.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        j = 0
        for row1 in spamreader:
            if j == 0:
                j += 1
                continue
            row = []
            if row1[5] != average_type: continue

            if row1[0] in districts.keys():
                row.extend(districts[row1[0]])
            else:
                row.extend([row1[1], '', ''])

            for i, key in enumerate(row1):
                if i == 0: continue
                row.append(key)

            if row[0] in rooms.keys():
                for i, val in enumerate(rooms[row[0]].values()):
                    if i == 1: continue
                    row.append(val)
            else:
                row.extend(['', '', '', '', ''])

            if row[0] in wanted.keys():
                row.append(wanted[row[0]])
            else:
                row.append('')

            if row[0] in rent.keys():
                row.append(rent[row[0]])
            else:
                row.append('')

            spamwriter.writerow(row)
