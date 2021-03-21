from owlready2 import *
import json


class Tronto(object):

    def __init__(self):
        self.onto = get_ontology('assets/tronto_f.owl').load()
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

                key = key.replace('\\\\', '')
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

        is_critical = 'false'
        for dep in dependencies:
            for vuln in dep.has_vulnerability:
                vuln_level = vuln.has_severity_level[0]
                if vuln_level > 3.0:
                    is_critical = 'true'
                    break

        return is_critical

    # get list of all vulnerabilities in dependencies
    def get_vulnerabilities(self, app):

        cve_list = []
        dependencies = list(app.depends_on)
        for dependency in dependencies:
            vulnerabilities = dependency.has_vulnerability
            cves = [str(iris).replace('tronto_f.', '') for iris in vulnerabilities]
            cve_list.extend(cves)

        cve_list = sorted(list(set(cve_list)))
        return cve_list

    # get dictionary of dependency data
    def get_dependency_dict(self, app):

        dependency_status_list = []
        dependencies = list(app.depends_on)
        for dependency in dependencies:
            vulnerabilities = dependency.has_vulnerability
            vulnerability_str = [str(iris).replace('tronto_f.', '') for iris in vulnerabilities]
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

            dependency_name = (str(dependency).split(';')[1]).replace('_', ' ')

            dependency_status_dict = {'Name': dependency_name, 'Status': is_vulnerable,
                                      'Vulnerabilities': vulnerability_str, 'Severity': severity}
            dependency_status_list.append(dependency_status_dict)

        return dependency_status_list

    def get_app_data(self, app_dict):
        app_data_dict = {}
        app_dependencies = app_dict['dependencies']
        depends_on = []
        for dependency_name in app_dependencies:
            if dependency_name in self.products_in_onto:
                depend_iris = (self.products_in_onto[dependency_name])['iris']
                depend_obj = IRIS[depend_iris]
                depends_on.append(depend_obj)
            else:
                app_dependencies.remove(dependency_name)

        new_app = self.onto.Application(app_dict['name'], depends_on=depends_on)

        dependencies = list(new_app.INDIRECT_depends_on)
        dependencies.append(new_app)

        app_data_dict['name'] = app_dict['name']
        app_data_dict['dependencies'] = app_dependencies

        app_data_dict['is_vulnerable'] = self.is_vulnerable(dependencies)
        app_data_dict['is_critical'] = self.is_critical(dependencies)
        app_data_dict['vulnerabilities'] = self.get_vulnerabilities(new_app)
        app_data_dict['dependency_dict'] = self.get_dependency_dict(new_app)

        return app_data_dict

    def sync_ontology(self):
        sync_reasoner()

    def save_updated_ontology(self):
        self.onto.save(file='tronto_f_updated.owl')
