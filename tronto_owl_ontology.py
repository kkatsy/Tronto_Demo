from owlready2 import *
import pickle
import Cython

class Tronto(object):

    def __init__(self):
        self.onto = get_ontology("tronto_d.owl").load()
        self.added_apps = {}
        self.base_iri = self.onto.base_iri
        self.cur_app = None
        with open('product_dict.pickle', 'rb') as f:
            self.products_in_onto = pickle.load(f)

    def add_to_ontology(self, app_dict):
        depends_on = []
        for dependency_name in app_dict['dependencies']:
            depend_iris = (self.products_in_onto[dependency_name])['iris']
            depend_obj = IRIS[depend_iris]
            depends_on.append(depend_obj)

        new_app = self.onto.Application(app_dict['name'], depends_on=depends_on)

        self.added_apps[app_dict['name']] = new_app
        self.cur_app = new_app

    def sync_ontology(self):
        sync_reasoner()

    def is_app_vulnerable(self):
        if (self.onto.Vulnerable_configuration in self.cur_app.is_a) == True:
            return 'vulnerable'
        return 'not vulnerable, afaik'

    def save_updated_ontology(self):
        self.onto.save(file='tronto_d_updated.owl')
