# cybersecurity-checker

**Heroku Link:** [https://cybersecurity-checker.herokuapp.com/](https://cybersecuritychecker.herokuapp.com/)
- wrapper doesn't run on site b/c of 503 error (fix!) (occurs bc of owlready2 exception, try w python 3.9)

### Repository Organization
**directories**
- static: JS and CSS files
- templates: HTML files
- tronto: tronto python notebook code

**python files**
- app.py: flask routes and functions
- tronto_owl_ontology.py: tronto wrapper class
- twitter.py: pulling tweets w/ Twitter API

**data files**
- dependencynames.json: name of applications within ontology (used as keys for typeahead)
- tronto_d.owl: owl file containing ontology (loaded in in tronto_owl_ontology.py)
- product_dict.pickle: dictionary that maps application names to their IRIS data

**heroku files**
- Procfile
- requirements.txt
- runtime.txt
