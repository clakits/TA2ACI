# csv2xml.py

# First row of the csv file must be header!
# Christine Lakits
# Date: 05/13/2018
import csv

def main():
    csvFile = 'ERPM-v1-policies.csv'
    xmlFile = 'ERPM-v1-policies_filters.xml'
    tenant = "clakits"
    #rowNum = 0
    fieldNames = ["Source", "Destination", "Protocol", "From_Port", "To_Port", "Service Name"]
    csvData = csv.reader(open(csvFile))
    rowNum = 0
    writeConfig = 0
    for row in csvData:
        if rowNum == 0:
            if row == fieldNames:
                print "Headers are correct - proceed with writing xml file"
                writeConfig = 1

        rowNum += 1

    #print writeConfig


    if writeConfig:
        csvData = csv.reader(open(csvFile))
        rowNum = 0
        xmlData = open(xmlFile, 'w')
        xmlData.write('<?xml version="1.0" encoding="UTF-8"?>' + "\n")
        xmlData.write('<imdata totalCount="1">' + "\n")
        xmlData.write('<fvTenant descr="" dn="uni/tn-clakits" name="clakits" nameAlias="" ownerKey="" ownerTag="">' + "\n")

        for row in csvData:

            if rowNum > 0:
                for i in range(len(fieldNames)):
                    sourceEPG = row[0]
                    destEPG = row[1]
                    proto = row[2]
                    fromPort = row[3]
                    toPort = row[4]
                    filterName = proto + "." + fromPort + "." + toPort + ".allow"
                    vzEntryName = proto + "-" + fromPort + "-" +toPort
                    print filterName
                xmlData.write('    ' + '<vzFilter descr="" name="' + filterName + '" nameAlias="" ownerKey="" ownerTag="">' +"\n")
                xmlData.write('        ' + '<vzEntry applyToFrag="no" arpOpc="unspecified" dFromPort="' + fromPort + '" dToPort="' + toPort + \
                              '" descr="" etherT="ip" icmpv4T="unspecified" icmpv6T="unspecified" matchDscp="unspecified name="' + vzEntryName +' nameAlias="" prot="' + proto + \
                              '" sFromPort="unspecified" sToPort="unspecified" stateful="no" tcpRules=""/>' + "\n")
                xmlData.write('    ' +'</vzFilter>' + "\n")


            rowNum += 1

        xmlData.write('</fvTenant>' + "\n")
        xmlData.write('</imdata>' + "\n")
        xmlData.close()

if __name__ == '__main__':
    main()