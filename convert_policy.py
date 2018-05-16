import ujson
import csv
import socket


def get_service_name(port, protocol_num):
    if port == 5640:
        return "tetration-data"
    elif port == 5660:
        return "tetration-enforcement"
    elif protocol_num == 6:
        protocol = "tcp"
        try:
            return socket.getservbyport(port, protocol)
        except:
            return "n/a"
    elif protocol_num == 17:
        protocol = "udp"
        try:
            return socket.getservbyport(port, protocol)
        except:
            return "n/a"
    elif protocol_num == 1:
        return "icmp"
    else:
        return "n/a"


def get_cluster(file):
    # fieldname = "EPG", "IP", "Hostname"
    print "EPG", "IP", "Hostname"

    fieldnames = ["EPG", "IP", "Hostname"]

    with open("/Users/clakits/Documents/ADM/policyOutput/cluster.csv", "wb") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for items in file.get("clusters"):
            if items["name"]:
                epg = items["name"].replace(" ", "-")
                for item in items["nodes"]:
                    ip = item["ip"]
                    hostname = item['name']
                    print epg, ip, hostname

                    writer.writerow({"EPG": epg, "IP": ip, "Hostname": hostname})

    csvfile.close()


def write_csv(filename, fieldnames, output):
    file_name = filename + ".csv"


def get_policy(file, policy_name):
    print "source", "destination", "protocol", "from_port", "to_port", "service name"

    fieldnames = ["Source", "Destination", "Protocol", "From_Port", "To_Port", "Service Name"]

    with open("/Users/clakits/Documents/ADM/policyOutput/" + policy_name + ".csv", "wb") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for items in file.get(policy_name):
            if items["action"] == 'ALLOW':
                consumer_epg = items['consumer_filter_name'].replace(" ", "-")
                provider_epg = items['provider_filter_name'].replace(" ", "-")

                # ignore uSeg components
                # remove this statement if you want to include them
                if consumer_epg == provider_epg:
                    continue
                else:
                    for item in items["l4_params"]:
                        proto = item["proto"]
                        from_port = item["port"][0]
                        to_port = item["port"][1]
                        service_name = get_service_name(from_port, proto)
                        print consumer_epg, provider_epg, proto, from_port, to_port, service_name
                        writer.writerow({"Source": consumer_epg, "Destination": provider_epg, "Protocol": proto, "From_Port": from_port, "To_Port": to_port, "Service Name": service_name})

    csvfile.close()


def main():
    with open('/Users/clakits/Documents/ADM/policyInput/ADW non-prod-test-v37-policies.json') as fi:
        policy = ujson.load(fi)

    ap_name = policy["name"].replace(" ", "-")
    print "Application profile is", ap_name

    if policy.get("clusters"):
        print "+++++++++ Cluster Info +++++++++"
        get_cluster(policy)

    if policy.get("absolute_policies"):
        print "+++++++++ Absolute policy +++++++++"
        get_policy(policy, "absolute_policies")

    if policy.get("default_policies"):
        print "+++++++++ Default policy +++++++++"
        get_policy(policy, "default_policies")


if __name__ == '__main__':
    main()
