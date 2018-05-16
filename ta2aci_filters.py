# csv2xml.py

# First row of the csv file must be header!

# example CSV file: myData.csv
# id,code name,value
# 36,abc,7.6
# 40,def,3.6
# 9,ghi,6.3
# 76,def,99

'''
<vzFilter descr="" name="tet-app--tet-db01" nameAlias="" ownerKey="" ownerTag="">
			<vzEntry applyToFrag="no" arpOpc="unspecified" dFromPort="3306" dToPort="3306" descr="" etherT="ip" icmpv4T="unspecified" icmpv6T="unspecified" matchDscp="unspecified" name="tcp-3306-3306" nameAlias="" prot="tcp" sFromPort="unspecified" sToPort="unspecified" stateful="no" tcpRules=""/>
		</vzFilter>


'''

import csv

csvFile = 'ERPM-v1-policies.csv'
xmlFile = 'ERPM-v1-policies.xml'
tenant = "clakits"

csvData = csv.reader(open(csvFile))
xmlData = open(xmlFile, 'w')
xmlData.write('<?xml version="1.0" encoding="UTF-8"?>' + "\n")
# there must be only one top-level tag
xmlData.write('<imdata totalCount="1">' + "\n")
xmlData.write('<fvTenant descr="" dn="uni/tn-clakits" name="clakits" nameAlias="" ownerKey="" ownerTag="">' + "\n")
rowNum = 0
for row in csvData:
    if rowNum == 0:
        tags = row
        # replace spaces w/ underscores in tag names
        for i in range(len(tags)):
            tags[i] = tags[i].replace(' ', '_')
    else:
        xmlData.write('<row>' + "\n")
        for i in range(len(tags)):
            xmlData.write('    ' + '<' + tags[i] + '>' \
                          + row[i] + '</' + tags[i] + '>' + "\n")
        xmlData.write('</row>' + "\n")

    rowNum +=1

xmlData.write('</fvTenant>' + "\n")
xmlData.write('</imdata>' + "\n")
xmlData.close()