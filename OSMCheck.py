
import xml.etree.ElementTree as ET
import re

name_file = "blore_select"
tree = ET.parse(name_file)
root = tree.getroot()

#### Observation1:Printing names and counts of tags

tags_list = []
for child in root:
     if child.tag not in tags_list:
         tags_list.append(child.tag)

print tags_list

count_tag = 0
for i in tree.getiterator('tag'):
   count_tag = count_tag + 1
count_node= 0

for i in tree.getiterator('node'):
   count_node = count_node + 1
print count_tag
print count_node

# ###Observation2:There is no 'user' or 'uid' information in the nodes tags

for i in tree.getiterator('node'):
    c1 = i.get('uid')
    if c1:
        print c1

for i in tree.getiterator('node'):
    c1 = i.get('user')
    if c1:
        print c1

## Observation3: The tag element only contain ['k','v'] attributes.
attribs = []
for i in tree.getiterator('tag'):
    if i.keys() not in attribs:
        attribs.append(i.keys())
print attribs

typedict_k = []
for i in tree.getiterator('tag'):
    c1 = i.get('k')
    type_i = type(c1)
    if type_i not in typedict_k:
        typedict_k.append(type_i)

typedict_v = []
for i in tree.getiterator('tag'):
    c2 = i.get('v')
    type_i = type(c2)
    if type_i not in typedict_v:
        typedict_v.append(type_i)

print typedict_k
print typedict_v