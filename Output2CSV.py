
import xml.etree.ElementTree as ET
import unicodecsv as csv

### Writing the file into csv format


name_file = "Output.xml"
tree = ET.parse(name_file)
root = tree.getroot()


OSM_nodes = open('OSM_nodes.csv', 'w')

csvwriter = csv.writer(OSM_nodes)
osm_nodes_header = []

for i in tree.getiterator('node'):
    attribute_nodes = i.keys()
for i in attribute_nodes:
    osm_nodes_header.append(i)

csvwriter.writerow(osm_nodes_header)
count = 0
for row in root.findall("node"):
    osm_row = []
    lat = row.get("lat")
    lon = row.get("lon")
    id = row.get('id')
    osm_row = [lat, lon, id]
    csvwriter.writerow(osm_row)
    count = count+1

print "Total rows in nodes file:"
print count
print ""

OSM_nodes_tags = open('OSM_nodes_tags.csv', 'w')
csvwriter2 = csv.writer(OSM_nodes_tags)
osm_nodes_tags_header = ["id", "v_type"]

for i in tree.getiterator('tag'):
    attribute_nodes = i.keys()
for i in attribute_nodes:
    osm_nodes_tags_header.append(i)

csvwriter2.writerow(osm_nodes_tags_header)
count2 = 0
for row in root.findall("node"):
    id = row.get('id')
    for line in row.findall("tag"):
        osm_row = []
        k = line.get("k")
        v = line.get("v")

        v_type = type(v)
        id1 = id
        osm_row = [id1,v_type, k,v]
        csvwriter2.writerow(osm_row)
        count2 = count2+1

print "Total rows in tags file"
print count2

print count+count2

