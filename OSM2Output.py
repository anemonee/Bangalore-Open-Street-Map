
import xml.etree.ElementTree as ET
import re

name_file = "blore_select"
tree = ET.parse(name_file)
root = tree.getroot()
rows_initial= 0
rows_final= 0

for i in root.iter():
    rows_initial = rows_initial + 1
print ("Total number of initial rows", rows_initial)
print ""

### Checking and Fixing postal codes

def postalcode_update(v1):
    x = v1.replace(" ","")
    x = x.replace(",","")
    x = x.replace("-","")
    x = x.replace('"',"")
    return x

initial_wrong_codes = []
codes_wrong_after_correction = []
count = 0
regex = re.compile('^(5)(6)\d{4}$')
for node in root.findall('node'):
    for tag in node.iter('tag'):
        k1 = tag.get("k")
        if k1 == "addr:postcode":
            v1 = tag.get("v")
            m1 = regex.match(v1)
            if not m1:
                initial_wrong_codes.append(v1)
                if len(v1) <> 6:
                    v2 = postalcode_update(v1)
                    tag.set("v",v2)
                    m2 = regex.match(v2)
                if not m2:
                    codes_wrong_after_correction.append(v2)
                    node.remove(tag)
                    count = count +1
                elif len(v1) == 6:
                    node.remove(tag)
                    count = count +1
                    codes_wrong_after_correction.append(v2)


print ("wrong postal codes list:", initial_wrong_codes)
print (" postal codes that cant be corrected", codes_wrong_after_correction)
print ""
print ("number of postal codes dropped", count)
print ""


### Checking and correcting for phone numbers:

# Three conditions: one for landline numbers starting with digit 8 (080 is code for blore)
## Other for mobile number starting with 91, i.e. code for India, and last for the rest:


regex1 = re.compile('(8)|(08)')
countm1 = 0
m1list = []

regex2 = re.compile('(9)|(09)')
countm2 = 0
m2list = []

regex3 = re.compile('(7)|(07)|(1800)|(3)|(4)')
countm3 = 0
m3list = []

# printing phone numbers gives a sense that a lot of them are in different formats.Standardising
## formats and then applying regex conditions.

def phonenumber_update(v2):
    x = v2.replace(" ","")
    x = x.replace("  ","")
    x = x.replace("-","")
    x = x.replace('+',"")
    x = x.replace("(91)", "91")
    x = x.replace("0091", "91")
    x = x.replace("O", "0")
    x = x.replace('"', "")
    x = x.replace('01800', "1800")
    x = x.replace('0099', "99")
    x = x.replace('9180', "80")
    x = x.replace('91080', "80")
    return x


def regex_m1(number):
    if len(number)<= 9:
        return True
    elif len(number)>= 12:
        return False
    else:
        pass


def regex_m2(number):
    if number[:2] == "91" and len(number) <> 12:
        if number[:6] <> "911800":
            if len(number) <> 25 or len(number) <> 38 or len(number) <> 51:
                return True

def regex_m3(number):
    if len(number) == 8:
        return True


for node in root.findall('node'):
    for tag in node.iter('tag'):
        k1 = tag.get("k")
        if k1 == "phone":
            v2 = tag.get("v")
            v1 = phonenumber_update(v2)
            tag.set("v",v1)

## Now applying regex:

            m1 = regex1.match(v1)
            m2 = regex2.match(v1)
            m3 = regex3.match(v1)

            if m1:
                if regex_m1(v1) is True:
                    countm1 = countm1 + 1
                    m1list.append(v1)
                    node.remove(tag)
                elif regex_m1(v1) is False:
                    if v1.find(',') == -1:
                        v2 = v1[:11]+", "+v1[11:]
                        if len(v2) < 20:
                            countm1 = countm1 + 1
                            m1list.append(v1)
                            node.remove(tag)
            elif m2:
                if regex_m2(v1) is True:
                    v2 = v1[:12] + "," + v1[12:]
                    if v2[13:15] == '91':
                        if len(v2[13:]) == 12:
                            v1 = v1.replace(v1,v2)
                            tag.set("v",v1)
                        else:
                            countm2 = countm2 + 1
                            m2list.append(v1)
                            node.remove(tag)
                    elif v2[13:15] == '97':
                        if len(v2[13:]) == 10:
                            v1 = v1.replace(v1,v2)
                            tag.set("v",v1)
                        else:
                            countm2 = countm2 + 1
                            m2list.append(v1)
                            node.remove(tag)
                    elif v2[13:16] == '080' or v2[13:15] == '80' or  v2[13:17] == ',080':
                        v1 = v1.replace(v1,v2)
                        tag.set("v",v1)
                    else:
                        countm2 = countm2 + 1
                        m2list.append(v1)
                        node.remove(tag)
            elif m3:
                if regex_m3(v1) is True:
                    v2 = '80'+ v1
                    v1 = v1.replace(v1,v2)
                    tag.set("v",v1)
            else:
                countm3 = countm3 + 1
                m3list.append(v1)
                node.remove(tag)

print "Phone numbers with starting digit 8,9, and others that can't be corrected, hence dropped"
print ("starting with 8", countm1, m1list)
print ("starting with 9", countm2, m2list)
print ("other", countm3, m3list)
print ""
print ("Total phone numbers dropped = ", countm1+countm2+countm3)


### Correcting for amenity names:

for node in root.findall('node'):
    for tag in node.iter('tag'):
        k1 = tag.get("k")
        if k1 == "amenity":
            v1 = tag.get("v")
            if v1 == 'ice cream':
                v1 = v1.replace(v1, "ice_cream")
                tag.set("v",v1)
            elif v1 == "bar" or v1 == "pub":
                v1 = v1.replace(v1, "bar;pub;restaurant")
                v1 = v1.replace(v1, "bar;pub;restaurant")
                tag.set("v",v1)


for i in root.iter():
    rows_final = rows_final + 1
print ("Total number of final rows", rows_final)

tree.write('Output.xml')



