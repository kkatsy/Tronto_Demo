from owlready2 import *
import pickle


class Tronto(object):

    def __init__(self):
        self.onto = get_ontology("tronto_d.owl").load()
        self.added_apps = {}
        self.base_iri = self.onto.base_iri
        self.cur_app = None
        self.cur_dependencies = None
        with open('product_dict.pickle', 'rb') as f:
            self.products_in_onto = pickle.load(f)

    # create new ontology application
    def create_onto_application(self, app_dict):
        depends_on = []
        for dependency_name in app_dict['dependencies']:
            depend_iris = (self.products_in_onto[dependency_name])['iris']
            depend_obj = IRIS[depend_iris]
            depends_on.append(depend_obj)

        new_app = self.onto.Application(app_dict['name'], depends_on=depends_on)

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

        vuln = 0
        for d in dependencies:
            if len(d.has_vulnerability) > 0:
                vuln = 1
                break

        if vuln == 1:
            return 'vulnerable'
        return 'not vulnerable'

    # get dict of dependencies and their vulnerability statuses
    def get_dependency_statuses(self):
        dependency_status_list = []
        for dependency_name in self.cur_dependencies:
            depend_iris = (self.products_in_onto[dependency_name])['iris']
            dependency = IRIS[depend_iris]
            vulnerabilities = dependency.has_vulnerability
            vulnerabilities = [str(iris).replace('tronto_d.', '') for iris in vulnerabilities]
            vulnerabilities = ', '.join(vulnerabilities)
            is_vulnerable = 'vulnerable' if (len(vulnerabilities) > 0) else 'not vulnerable'
            dependency_status_dict = {'Name': dependency_name, 'Status': is_vulnerable, 'Vulnerabilities': vulnerabilities}
            dependency_status_list.append(dependency_status_dict)
        return dependency_status_list

    # get application status after it's been embedded in ontology
    def is_app_in_onto_vulnerable(self):
        if (self.onto.Vulnerable_configuration in self.cur_app.is_a) == True:
            return 'vulnerable'
        return 'not vulnerable'

    # save updated ontology
    def save_updated_ontology(self):
        self.onto.save(file='tronto_d_updated.owl')
