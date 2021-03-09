from owlready2 import *
import json


class Tronto(object):

    def __init__(self):
        self.onto = get_ontology('assets/tronto_f.owl').load()
        self.added_apps = {}
        self.base_iri = self.onto.base_iri
        self.cur_app = None
        self.cur_dependencies = None
        self.cur_vulnerability = None

        # build data for applications currently in onto
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

        product_names = list(products.keys())
        with open('assets/dependencynames.json', 'w') as f:
            json.dump(product_names, f)

    # create new ontology application
    def create_onto_application(self, app_dict):
        depends_on = []
        for dependency_name in app_dict['dependencies']:
            depend_iris = (self.products_in_onto[dependency_name])['iris']
            depend_obj = IRIS[depend_iris]
            depends_on.append(depend_obj)

        new_app = self.onto.Application(app_dict['name'], depends_on=depends_on)

        # update current information
        self.added_apps[app_dict['name']] = new_app
        self.cur_app = new_app
        self.cur_dependencies = app_dict['dependencies']

    # embed application into ontology
    def sync_ontology(self):
        sync_reasoner()

    # check if app vulnerable based on dependencies
    def is_app_vulnerable(self):
        dependencies = list(self.cur_app.INDIRECT_depends_on)
        dependencies.append(self.cur_app)

        is_vulnerable = False
        for dep in dependencies:
            if len(dep.has_vulnerability) > 0:
                is_vulnerable = True
                break

        if is_vulnerable:
            self.cur_vulnerability = True
            return 'vulnerable'
        else:
            self.cur_vulnerability = False
            return 'not vulnerable'

    def is_app_critical(self):
        dependencies = list(self.cur_app.INDIRECT_depends_on)
        dependencies.append(self.cur_app)

        is_critical = False
        if self.cur_vulnerability:
            for dep in dependencies:
                for vuln in dep.has_vulnerability:
                    vuln_level = vuln.has_severity_level[0]
                    if vuln_level > 3.0:
                        is_critical = True
                        break

        return is_critical

    # get dict of dependencies and their vulnerability statuses
    def get_dependency_statuses(self):
        dependency_status_list = []
        for dependency_name in self.cur_dependencies:
            depend_iris = (self.products_in_onto[dependency_name])['iris']
            dependency = IRIS[depend_iris]
            vulnerabilities = dependency.has_vulnerability
            vulnerability_str = [str(iris).replace('tronto_f.', '') for iris in vulnerabilities]
            vulnerability_str = ', '.join(vulnerability_str)
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

            dependency_status_dict = {'Name': dependency_name, 'Status': is_vulnerable,
                                      'Vulnerabilities': vulnerability_str, 'Severity': severity}
            dependency_status_list.append(dependency_status_dict)

        return dependency_status_list

    # get application status after it's been embedded in ontology
    def is_app_in_onto_vulnerable(self):
        if (self.onto.Vulnerable_configuration in self.cur_app.is_a) == True:
            return 'vulnerable'
        return 'not vulnerable'

    # save updated ontology
    def save_updated_ontology(self):
        self.onto.save(file='tronto_updated.owl')