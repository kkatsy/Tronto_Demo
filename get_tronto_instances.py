import json
import re


def parse_cve(cve):
    # The argument of this function is an entry in a cve dict.
    # It should iterate over the dict, and the output should be added to a new dict.

    cve_id = cve["cve"]["CVE_data_meta"]["ID"]  # Get the ID
    cve_class = cve["cve"]["problemtype"]["problemtype_data"][0]["description"][0]["value"]  # Get the class
    cve_description = cve["cve"]["description"]["description_data"][0]["value"]  # Get the description
    cve_severity = cve["impact"]["baseMetricV3"]["cvssV3"]["baseScore"]  # Get the severity score

    # Flatten the configurations dict into a string
    conf_str = str(cve['configurations'])

    # Compile the regular expression pattern for matching. This may need to be done only once.
    cpe_item = re.compile("(\{'vulnerable': True, 'cpe23Uri': 'cpe:2.3:)(.*?)('\})")

    # Extract the matches
    cpe_list = cpe_item.findall(conf_str)

    # Extract the item of interest and add it to a set of affected configurations
    cpe_set = set(list())
    for item in cpe_list:
        cpe_set.add(item[1])

    return [cve_id, cve_class, cve_description, cve_severity, cpe_set]


# Load the cve feed json file. It loads it as a string
json_file = 'nvdcve-1.1-2021.json'

with open(json_file, 'r') as json_in:
    json_string = json_in.read()

# This is necessary to properly load a json feed as a python dict
json_feed = json.loads(json_string)

# As we iterate over the json feed, extracting the information,
# we format it as a string and write to file directly (no need to store information in a dict).
# The json feed is a dict. The `CVE_Items` key has as its value a **list** of CVEs.

# Since we are going to write to a file, it is a good idea to specify the file where the
# information is going to be stored first:
destination_file = 'tronto_instances.txt'

error_list = []
# Now we start the processing of the information from the json feed
for id_num, it in enumerate(json_feed["CVE_Items"]):  # iterate over the members of the list
    # Keep the iteration short as a trial
    # Each member or item is a CVE entry, that needs to be parsed using the `parse_cve()` function
    try:
        parsed_cve = parse_cve(it)  # parse the item

        # The output of parse_cve is a list: [cve_id, cve_class, cve_description, cve_severity, cpe_set]
        # We use the items in this list to format strings for writing to the OWL document
        # First format a string for the vulnerability. The fields of interest are the
        # CVE ID and the CWE class
        # We are also including a datatype property for the severity score

        vuln = """<%(class)s rdf:about="#%(id)s"> \
        \n\t<rdf:type rdf:resource="http://www.w3.org/2002/07/owl#NamedIndividual"/> \
        \n\t<has_severity_score rdf:datatype="http://www.w3.org/2001/XMLSchema#float"> \
        %(severity).1f</has_severity_score>\n</%(class)s>\n""" \
               % {"class": parsed_cve[1].replace('-', ""), "id": parsed_cve[0].replace('-', ''),
                  "severity": parsed_cve[3]}

        # Once the vulnerability string is formatted using the XML/OWL standard and stored as the
        # value of the vuln variable, we write it to a text file

        with open(destination_file, 'a') as outfile:
            outfile.write(vuln)

        # Next format a string for the configuration(s), including the relation to a vulnerability.
        # The parse_cve function stores all the configurations in a set. We iterate over the
        # members of the set to extract the fields we are interested in.
        comp_class = ''
        comp_vendor = ''
        comp_product = ''
        comp_version = ''
        comp_release = ''
        comp_id = ''
        for comp_uri in list(parsed_cve[4]):
            comp_class = re.match(r'(.:)([^:]*):([^:]*):([^:]*):([^:]*)', comp_uri).group(1)
            comp_vendor = re.match(r'(.:)([^:]*):([^:]*):([^:]*):([^:]*)', comp_uri).group(2)
            comp_product = re.match(r'(.:)([^:]*):([^:]*):([^:]*):([^:]*)', comp_uri).group(3)
            comp_version = re.match(r'(.:)([^:]*):([^:]*):([^:]*):([^:]*)', comp_uri).group(4)
            comp_release = re.match(r'(.:)([^:]*):([^:]*):([^:]*):([^:]*)', comp_uri).group(5)
            comp_id = comp_vendor + ';' + comp_product + ';' + comp_version + ';' + comp_release

        comp = ''
        if comp_class == 'o:':
            comp = """<Operating_system rdf:about="#%(c_id)s">\n\t<rdf:type \
            rdf:resource="http://www.w3.org/2002/07/owl#NamedIndividual"/> \
            \n\t<has_vulnerability rdf:resource="#%(v_id)s"/> \
            \n</Operating_system>\n""" \
                   % {"c_id": comp_id, "v_id": parsed_cve[0].replace('-', "")}

        elif comp_class == 'a:':
            comp = """<Application rdf:about="#%(c_id)s">\n\t<rdf:type \
            rdf:resource="http://www.w3.org/2002/07/owl#NamedIndividual"/> \
            \n\t<has_vulnerability rdf:resource="#%(v_id)s"/> \
            \n</Application>\n""" \
                   % {"c_id": comp_id, "v_id": parsed_cve[0].replace('-', "")}

        elif comp_class == 'h:':
            comp = """<Hardware rdf:about="#%(c_id)s">\n\t<rdf:type rdf:resource=
            "http://www.w3.org/2002/07/owl#NamedIndividual"/> \n\t<has_vulnerability
            rdf:resource="#%(v_id)s"/> \n</Hardware>\n""" \
                   % {"c_id": comp_id, "v_id": parsed_cve[0].replace('-', "")}

        with open(destination_file, 'a') as outfile:
            outfile.write(comp)

    except IndexError:
        error_list.append('IndexError: list index out of range in CVE %d' % (id_num))
        pass
    except KeyError:
        error_list.append("KeyError: 'baseMetricV3' in CVE %d" % (id_num))
        pass
