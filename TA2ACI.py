# TA2ACI_0514Healthsouth.py

# First row of the csv file must be header as following:
# Source	Destination	Protocol	From_Port	To_Port
# Christine Lakits
# Version: 0.1
# Date: 05/13/2018
# Based on HS naming convention - tenant, ap, filter, contract, EPG should be changed accordingly

import csv

def main():
    csvFile = 'Non_prod_ADW_default_policies_modified_CL0515.csv'
    xmlFile = 'Non_prod_ADW-policies_contract.xml'
    tenant = "clakits"
    ap = "Non-prod-ADW"
    l3extOut = "default"
    l3extInstP = "l3outDefault"

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
        xmlData.write('<fvTenant descr="" dn="uni/tn-'+ tenant +'" name="' + tenant + '" nameAlias="" ownerKey="" ownerTag="">' + "\n")
        filter_Names =[]


        # write filter config
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
                if filterName not in filter_Names:
                    filter_Names.append(filterName)
                    xmlData.write('    ' + '<vzFilter descr="" name="' + filterName + '" nameAlias="" ownerKey="" ownerTag="">' +"\n")
                    xmlData.write('        ' + '<vzEntry applyToFrag="no" arpOpc="unspecified" dFromPort="' + fromPort + '" dToPort="' + toPort + \
                              '" descr="" etherT="ip" icmpv4T="unspecified" icmpv6T="unspecified" matchDscp="unspecified" name="' + vzEntryName +'" nameAlias="" prot="' + proto + \
                              '" sFromPort="unspecified" sToPort="unspecified" stateful="no" tcpRules=""/>' + "\n")
                    xmlData.write('    ' +'</vzFilter>' + "\n")


            rowNum += 1


#### write contract config
        csvData = csv.reader(open(csvFile))
        rowNum = 0
        src2dst_list = []
        contract_all =[]
        contractInfo = {}
        for row in csvData:

            if rowNum > 0:
                for i in range(len(fieldNames)):
                    contractInfo['srcEPG'] = row[0]
                    contractInfo['dstEPG'] = row[1]
                    contractInfo['proto']= row[2]
                    contractInfo['fromPort'] = row[3]
                    contractInfo['toPort'] = row[4]
                if contractInfo not in contract_all:
                    contract_all.append(contractInfo.copy())
            #print contractInfo['srcEPG'] + ".TO." + contractInfo['dstEPG'] + "Contract"
                src2dst = contractInfo['srcEPG'] + "To" + contractInfo['dstEPG'] + "Contract"
                if src2dst not in src2dst_list:
                    src2dst_list.append(src2dst)
                    #print src2dst_list

            rowNum += 1
        print src2dst_list
        #print "88888888"
        print contract_all
        for i in src2dst_list:
            xmlData.write('    ' + '<vzBrCP descr="" name="' + i + '" nameAlias="" ownerKey="" ownerTag="" prio="unspecified" scope="context" targetDscp="unspecified">' + "\n")
            xmlData.write('         ' + '<vzSubj consMatchT="AtleastOne" descr="" name="subject" nameAlias="" prio="unspecified" provMatchT="AtleastOne" revFltPorts="yes" targetDscp="unspecified">'+ "\n")
            #print "I"
            for j in contract_all:
                f = j['proto'] + "." + j['fromPort'] + "." + j['toPort'] + ".allow"
                j_comp = j['srcEPG'] + "To" + j['dstEPG'] + "Contract"

                if j_comp == i:


                    xmlData.write('        ' + '<vzRsSubjFiltAtt directives="" tnVzFilterName="' + f + '"/>' + "\n")
            xmlData.write('         ' + '</vzSubj>' + "\n")
            xmlData.write('    ' +'</vzBrCP>' + "\n")

        # config provide and consume contract for EPGs
        epg_list = []
        l3instP_s = ""
        l3instP_d = ""
        epg_contract = {}
        epg_inx = 0
        for i in src2dst_list:
            print i
            epg_inx = i.find('To')
            print epg_inx
            epg_s = i[0:epg_inx]
            print epg_s
            epg_d = i[epg_inx+2:-8]
            print epg_d
            if epg_s not in epg_list:
                epg_list.append(epg_s)
            if epg_d not in epg_list:
                epg_list.append(epg_d)
            #if epg_s == "Default" or epg_d == "Default":
            #    l3instP = "Default"

        xmlData.write('<fvAp descr="" name="' + ap + '" nameAlias="" ownerKey="" ownerTag="" prio="unspecified">' + "\n")
        for n in epg_list:
            epg_contract['epg'] = n

            if n != "Default":
                xmlData.write('     '+ '<fvAEPg name="' + n + '" nameAlias="">'  + "\n" )
            for i in src2dst_list:
                epg_inx = i.find('To')
                print epg_inx
                epg_s = i[0:epg_inx]
                epg_d = i[epg_inx+2:-8]
                if n == epg_s and n != "Default":
                    xmlData.write('       ' + '<fvRsCons prio="unspecified" tnVzBrCPName="' + i +'"/>' + "\n")
                if n == epg_d and n != "Default":
                    xmlData.write('       ' + '<fvRsProv prio="unspecified" tnVzBrCPName="' + i +'"/>' + "\n")
            if n != "Default":
                xmlData.write('     '+ '</fvAEPg>'  + "\n")

        xmlData.write('     '+ '</fvAp>'  + "\n")

        # l3outInstP contract

        xmlData.write('<l3extOut descr="" name="' + l3extOut +'">'  + "\n")
        xmlData.write('    ' + '<l3extInstP descr="" name="' + l3extInstP + '">' + "\n")

        for n in epg_list:
            epg_contract['epg'] = n
            for i in src2dst_list:
                epg_inx = i.find('To')
                print epg_inx
                epg_s = i[0:epg_inx]
                epg_d = i[epg_inx+2:-8]
                if n == epg_s and n == "Default":
                    xmlData.write('       ' + '<fvRsCons prio="unspecified" tnVzBrCPName="' + i +'"/>' + "\n")
                if n == epg_d and n == "Default":
                    xmlData.write('       ' + '<fvRsProv prio="unspecified" tnVzBrCPName="' + i +'"/>' + "\n")

        xmlData.write('    ' + '</l3extInstP>' + "\n")
        xmlData.write('</l3extOut>' + "\n")
        xmlData.write('</fvTenant>' + "\n")
        xmlData.write('</imdata>' + "\n")
        xmlData.close()
        # config for l3out instP

if __name__ == '__main__':
    main()
