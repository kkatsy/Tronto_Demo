from owlready2 import *
import pickle
import Cython

class Tronto(object):

    def __init__(self):
        # load ontology from owl file
        self.onto = get_ontology("tronto_d.owl").load()

        # get product dict of dicts from pickle
        with open('product_dict.pickle', 'rb') as f:
            self.products_in_onto = pickle.load(f)

        self.added_apps = {}                # new apps added in session
        self.base_iri = self.onto.base_iri  # base iri of ontology
        self.cur_app = None                 # cur app being evaluated

    def add_to_ontology(self, app_dict):
        # get list of iris for entered dependencies
        depends_on = []
        for dependency_name in app_dict['dependencies']:
            depend_iris = (self.products_in_onto[dependency_name])['iris']
            depend_obj = IRIS[depend_iris]
            depends_on.append(depend_obj)

        # create ontology application object
        new_app = self.onto.Application(app_dict['name'], depends_on=depends_on)

        # update newly added status
        self.added_apps[app_dict['name']] = new_app
        self.cur_app = new_app

    def sync_ontology(self):
        # embed new app in ontology
        # takes about 4 min to run
        sync_reasoner()

    def is_app_vulnerable(self):
        # check if cur app is in vulnerable configuration
        if (self.onto.Vulnerable_configuration in self.cur_app.is_a) == True:
            return 'vulnerable'
        return 'not vulnerable, afaik'

    def save_updated_ontology(self):
        # save new ontology to file
        self.onto.save(file='tronto_d_updated.owl')
