# cybersecurity-checker

**Heroku Link:** [https://cybersecurity-checker.herokuapp.com/](https://cybersecurity-checker.herokuapp.com/)
-> wrapper doesn't run on site b/c of 503 error (fix!) (occurs bc of owlready2 exception, try w python 3.9)

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

### TODOs:
- check vulnerability by dependency: add function to tronto class
- add checkbox: if user checks, add application to ontology via sync_reasoner
- change output: show application vulnerability + which dependencies are vulnerable
- create table from JSON dependency data w/ javascript
- embed tweets (query = depedency name), format ~20 end of page
- make demo more presentable: centered, bigger font, fix colors, css grid stuff and such
- if time, figure out how to run sync_reasoner as background job via stack queue

### Questions
- how to transfer demo to Errol and deploy from there
- should users input dependencies not contained within ontology
- demo behavior while sync_reasoner loads for 4ish mins
- adding tweets + SpaCy NER + twitter classifier functionality
- which tweets and how many tweets to embed
- updating ontology file: to save or not to save after adding new apps
- other tasks + recommended adjustments/changes/additions
