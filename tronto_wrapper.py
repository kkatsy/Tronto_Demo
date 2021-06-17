from owlready2 import *
import json
import sys
sys.dont_write_bytecode = True

class Tronto(object):

    def __init__(self):
        self.onto = get_ontology('assets/tronto_g.owl').load()
        self.added_apps = {}
        self.base_iri = self.onto.base_iri

        # build data for applications in ontology
        products = {}  # dict of dicts
        for individual in list(self.onto.individuals()):
            product_dict = {}
            iris = str(individual)[9:]

            # replace xml-encoded characters
            clean_iris = iris.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')\
                .replace('&quot;','\"').replace('&apos;', '\'')

            if (';' in clean_iris) and ('CVE' not in clean_iris):
                company, product, version, stage = clean_iris.split(';')
                company = company.replace('_', ' ')
                product = product.replace('_', ' ')

                if version == '*' or version == '-':
                    key = product
                else:
                    key = product + ' ' + version

                product_dict['iris'] = self.base_iri + iris
                product_dict['company'] = company
                product_dict['product'] = product
                product_dict['version'] = version
                product_dict['stage'] = stage

                key = key.replace('\\\\', '').replace('/', ' ')
                products[key] = product_dict

        self.products_in_onto = products

        # save products in ontology for typeahead
        product_names = list(products.keys())
        with open('assets/dependencynames.json', 'w') as f:
            json.dump(product_names, f)

    # get app's vulnerability status
    def is_vulnerable(self, dependencies):

        is_vulnerable = False
        for dep in dependencies:
            if len(dep.has_vulnerability) > 0:
                is_vulnerable = True
                break

        if is_vulnerable:
            return 'vulnerable'
        else:
            return 'not vulnerable'

    # check if app has critical vulnerability
    def is_critical(self, dependencies):

        highest_vuln_level = 0
        for dep in dependencies:
            for vuln in dep.has_vulnerability:
                vuln_level = vuln.has_severity_level[0]
                if vuln_level > highest_vuln_level:
                    highest_vuln_level = vuln_level

        # map to corresponding label
        if highest_vuln_level > 3:
            severity = 'critical'
        elif highest_vuln_level > 2:
            severity = 'high'
        elif highest_vuln_level > 1:
            severity = 'medium'
        elif highest_vuln_level > 0:
            severity = 'low'
        else:
            severity = 'none'

        return severity

    # get list of all vulnerabilities in dependencies
    def get_vulnerabilities(self, app):

        cve_list = []
        dependencies = list(app.depends_on)
        for dependency in dependencies:
            vulnerabilities = dependency.has_vulnerability
            cves = [str(iris).replace('tronto_g.', '') for iris in vulnerabilities]
            cves = [(cve[:3] + '-' + cve[3:7] + '-' + cve[7:]) for cve in cves]
            cve_list.extend(cves)

        cve_list = sorted(list(set(cve_list)))
        return cve_list

    # get dictionary of dependency data
    def get_dependency_dict(self, app):

        dependency_status_list = []
        dependencies = list(app.depends_on)
        for dependency in dependencies:
            vulnerabilities = dependency.has_vulnerability
            vulnerability_str = [str(iris).replace('tronto_g.', '') for iris in vulnerabilities]
            vulnerability_str = [(vuln[:3] + '-' + vuln[3:7] + '-' + vuln[7:]) for vuln in vulnerability_str]
            vulnerability_str = ', '.join(sorted(vulnerability_str))
            is_vulnerable = 'vulnerable' if (len(vulnerabilities) > 0) else 'not vulnerable'

            # get highest severity score for each dependency's dependencies
            severity_score = 0
            if is_vulnerable:
                for vuln in dependency.has_vulnerability:
                    vuln_level = vuln.has_severity_level[0]
                    if vuln_level > severity_score:
                        severity_score = vuln_level

            # map to corresponding label
            if severity_score > 3:
                severity = 'critical'
            elif severity_score > 2:
                severity = 'high'
            elif severity_score > 1:
                severity = 'medium'
            elif severity_score > 0:
                severity = 'low'
            else:
                severity = 'none'

            dep_list = str(dependency).split(';')
            dependency_name = dep_list[1].replace('_', ' ').replace('\\\\', '')
            if dep_list[2] != '*':
                dependency_name = dependency_name + ' ' + dep_list[2]

            dependency_status_dict = {'Name': dependency_name, 'Status': is_vulnerable,
                                      'Vulnerabilities': vulnerability_str, 'Severity': severity}
            dependency_status_list.append(dependency_status_dict)

        return dependency_status_list

    def get_app_data(self, app_dict):
        app_data_dict = {}                              # dict to return to client-side
        app_dependencies = app_dict['dependencies']     # list of all valid dependencies
        depends_on = []                                 # dependency ontology objects
        onto_dependencies = []                          # dependencies in ontology
        not_in_onto = []                                # entered depedencies not in ontology
        for dependency_name in app_dependencies:
            if dependency_name in self.products_in_onto:
                onto_dependencies.append(dependency_name)
                depend_iris = (self.products_in_onto[dependency_name])['iris']
                depend_obj = IRIS[depend_iris]
                depends_on.append(depend_obj)
            else:
                not_in_onto.append(dependency_name)

        # create new ontology application
        new_app = self.onto.Application(app_dict['name'], depends_on=depends_on)

        # get list of dependencies recursively
        app_dependencies = list(new_app.INDIRECT_depends_on)
        app_dependencies.append(new_app)

        # get and store app data
        app_data_dict['name'] = app_dict['name']
        app_data_dict['dependencies'] = onto_dependencies
        app_data_dict['is_vulnerable'] = self.is_vulnerable(app_dependencies)
        app_data_dict['is_critical'] = self.is_critical(app_dependencies)
        app_data_dict['vulnerabilities'] = self.get_vulnerabilities(new_app)
        app_data_dict['dependency_dict'] = self.get_dependency_dict(new_app)
        app_data_dict['not_in_onto'] = not_in_onto

        # for now, to decrease http request size
        if len(app_data_dict['vulnerabilities']) > 0:
            app_data_dict['vulnerabilities'] = ['dummy']

        return app_data_dict

    def get_descriptions(self, dependencies):
        descriptions = []
        for dependency_name in dependencies:
            depend_iris = (self.products_in_onto[dependency_name])['iris']
            dependency = IRIS[depend_iris]
            vulnerabilities = dependency.has_vulnerability
            for vuln in vulnerabilities:
                descriptions.append(vuln.has_description[0])

        return descriptions

    def get_cve_names(self, dependencies):
        cve_list = []
        for dependency_name in dependencies:
            depend_iris = (self.products_in_onto[dependency_name])['iris']
            dependency = IRIS[depend_iris]
            vulnerabilities = dependency.has_vulnerability
            cves = [str(iris).replace('tronto_g.', '') for iris in vulnerabilities]
            cves = [(cve[:3] + '-' + cve[3:7] + '-' + cve[7:]) for cve in cves]
            cve_list.extend(cves)

        cve_list = sorted(list(set(cve_list)))
        return cve_list

    def sync_ontology(self):
        sync_reasoner()

    def save_updated_ontology(self):
        self.onto.save(file='_updated.owl')
