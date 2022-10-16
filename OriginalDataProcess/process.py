import csv
from math import log
import matplotlib.pyplot as plt

Tier1 = {}
Tier2 = {}
Tier3 = {}

Tier1_file = open('Tier1.csv')
Tier1_reader = csv.reader(Tier1_file)
Tier2_file = open('Tier2.csv')
Tier2_reader = csv.reader(Tier2_file)
Tier3_file = open('Tier3.csv')
Tier3_reader = csv.reader(Tier3_file)

Tier1_data = []
Tier2_data = []
Tier3_data = []
for row in Tier1_reader:
    Tier1_data.append(row)
for row in Tier2_reader:
    Tier2_data.append(row)
for row in Tier3_reader:
    Tier3_data.append(row)
    
for data in Tier1_data:
    key_paper = data[0]
    institution = data[1][1:-1]
    if key_paper not in Tier1:
        Tier1[key_paper] = {institution}
    else:
        Tier1[key_paper].add(institution)
        
for data in Tier2_data:
    key_paper = data[0]
    institution = data[1][1:-1]
    if key_paper not in Tier2:
        Tier2[key_paper] = {institution}
    else:
        Tier2[key_paper].add(institution)
        
for data in Tier3_data:
    key_paper = data[0]
    institution = data[1][1:-1]
    if key_paper not in Tier3:
        Tier3[key_paper] = {institution}
    else:
        Tier3[key_paper].add(institution)

Id = 1
Tier1_cleaned = {}
Tier2_cleaned = {}
Tier3_cleaned = {}
for key in Tier1:
    temp_set = set()
    original_set = Tier1[key]
    for institute in original_set:
        full = institute.split(',')
        first = full[0].strip()
        last = full[-1].strip()
        temp_set.add(first + ',' + last)
    Tier1_cleaned[Id] = temp_set
    Id += 1
Id = 1
for key in Tier2:
    temp_set = set()
    original_set = Tier2[key]
    for institute in original_set:
        full = institute.split(',')
        first = full[0].strip()
        last = full[-1].strip()
        temp_set.add(first + ',' + last)
    Tier2_cleaned[Id] = temp_set
    Id += 1
Id = 1
for key in Tier3:
    temp_set = set()
    original_set = Tier3[key]
    for institute in original_set:
        full = institute.split(',')
        first = full[0].strip()
        last = full[-1].strip()
        temp_set.add(first + ',' + last)
    Tier3_cleaned[Id] = temp_set
    Id += 1
    
Tier1_file.close()
Tier2_file.close()
Tier3_file.close()

countries2institution = {}

for key in Tier1_cleaned:
    value = Tier1_cleaned[key]
    for each in value:
        school = each.split(',')[0]
        country = each.split(',')[1]
        if country not in countries2institution:
            countries2institution[country] = set()
            countries2institution[country].add(school)
        else:
            countries2institution[country].add(school)
for key in Tier2_cleaned:
    value = Tier2_cleaned[key]
    for each in value:
        school = each.split(',')[0]
        country = each.split(',')[1]
        if country not in countries2institution:
            countries2institution[country] = set()
            countries2institution[country].add(school)
        else:
            countries2institution[country].add(school)
for key in Tier3_cleaned:
    value = Tier3_cleaned[key]
    for each in value:
        school = each.split(',')[0]
        country = each.split(',')[1]
        if country not in countries2institution:
            countries2institution[country] = set()
            countries2institution[country].add(school)
        else:
            countries2institution[country].add(school)

def read(file):
    new = {}
    fout = file
    fo = open(fout, "r")

    for row in fo:
        if len(row.strip()) == 0:
            continue
        r = row.split('>>>')
        key = r[0].strip()
        try:
            value = r[1].strip()[1:-1].split(', ')
            value = set([x[1:-1] for x in value])
        except:
            print(row[0])
        if key not in new:
            new[key] = value
        else:
            new[key] = new[key].union(value)
    fo.close()
    return new
def read_grade(file):
    new = {}
    fout = file
    fo = open(fout, "r")

    for row in fo:
        if len(row.strip()) == 0:
            continue
        r = row.split('>>>')
        key = r[0].strip()
        value = r[1].strip()
        new[key] = float(value)
    fo.close()
    return new
    
c2i = read('countries2institution.txt')
i2c = read('institution2countries.txt')
for each in Tier1_cleaned:
    try:
        new_value = set()
        value = Tier1_cleaned[each]
        for ic in value:
            i = ic.split(',')[0].strip()
            c = i2c[i]
            new_value = new_value.union(c)
        Tier1_cleaned[each] = new_value
    except:
        print(each)

del Tier1_cleaned[3689]
del Tier1_cleaned[5069]

for each in Tier2_cleaned:
    try:
        new_value = set()
        value = Tier2_cleaned[each]
        for ic in value:
            i = ic.split(',')[0].strip()
            c = i2c[i]
            new_value = new_value.union(c)
        Tier2_cleaned[each] = new_value
    except:
        print(each)
del Tier2_cleaned[3699]
del Tier2_cleaned[4725]
del Tier2_cleaned[4766]
del Tier2_cleaned[4798]
del Tier2_cleaned[5476]

for each in Tier3_cleaned:
    try:
        new_value = set()
        value = Tier3_cleaned[each]
        for ic in value:
            i = ic.split(',')[0].strip()
            c = i2c[i]
            new_value = new_value.union(c)
        Tier3_cleaned[each] = new_value
    except:
        print(each)

Tier1_grade = 1.5
Tier2_grade = 1.25
Tier3_grade = 1
countries_grade = {}
for key in c2i:
    countries_grade[key] = 0.11
for each in Tier1_cleaned:
    for c in Tier1_cleaned[each]:
        countries_grade[c] = Tier1_grade + countries_grade[c]
for each in Tier2_cleaned:
    for c in Tier2_cleaned[each]:
        countries_grade[c] = Tier2_grade + countries_grade[c]
for each in Tier3_cleaned:
    for c in Tier3_cleaned[each]:
        countries_grade[c] = Tier3_grade + countries_grade[c]
        
def write_grade(grade, name):
    fo = open(name, "w")
    for k, v in grade.items():
        fo.write(str(k) + ' >>> '+ str(v) + '\n\n')
    fo.close()

def myplot(c_grade):
    y = []
    for each in c_grade:
        y.append(c_grade[each])
    y.sort()
    plt.plot(y)
c2rgdp = read_grade("country2ResearchGDP.txt")
countries_rgdp = {}
for country in countries_grade:
    if country in c2rgdp and countries_grade[country] > 14:
        countries_rgdp[country] = countries_grade[country] / c2rgdp[country] + 1
del countries_grade['none']
countries_population = read_grade("country2Population.txt")

print(countries_rgdp)
print(countries_grade)
print(countries_population)