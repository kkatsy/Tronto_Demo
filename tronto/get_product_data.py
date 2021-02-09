from tronto_owl import Tronto
import json
import pickle

ontology = Tronto()

individuals_list = list(ontology.onto.individuals())
individuals_list = [str(thing) for thing in individuals_list]

products = {} # dict of dicts
for individual in list(ontology.onto.individuals()):
    product_dict = {}
    iris = str(individual)[9:]

    if (';' in iris) and ('CVE' not in iris):
        company, product, version, stage = iris.split(';')
        company = company.replace('_', ' ')
        product = product.replace('_', ' ')

        if version == '*' or version == '-':
            key = product
        else:
            key = product + ' ' + version

        product_dict['iris'] = ontology.base_iri + iris
        product_dict['company'] = company
        product_dict['product'] = product
        product_dict['version'] = version
        product_dict['stage'] = stage

        products[key] = product_dict

product_names = list(products.keys())

print(products)
print(product_names)

with open('product_dict.pickle', 'wb') as f:
    pickle.dump(products, f)

with open('products.json', 'w') as f:
    json.dump(product_names, f)
