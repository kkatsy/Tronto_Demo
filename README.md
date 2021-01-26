# cybersecurity-checker

**Heroku Link:** [https://cybersecurity-checker.herokuapp.com/](https://cybersecurity-checker.herokuapp.com/)

### Repository Organization
**directories**
- static: JS and CSS files
- templates: HTML files
- tronto: code for getting applications data within ontology

**python files**
- app.py: flask routes and functions
- tronto_owl_ontology.py: tronto class
- twitter.py: pulling tweets w/ Twitter API

**data files**
- dependencynames.json: name strings of applications within ontology
- tronto_d.owl: owl files containing ontology 
- product_dict.pickle: dict of dicts containing names + iris data within ontology

### TODOs:
- mess with css + make presentable
- add loading spinner while waiting on sync_reasoner
- embed tweets into page

### Questions
- how to transfer demo to Errol and deploy from there
- should users input dependencies not contained within ontology
- demo behavior while sync_reasoner loads for 4ish mins
- adding tweets + SpaCy NER + twitter classifier functionality
- which tweets and how many tweets to embed
- updating ontology file: to save or not to save after adding new apps
- other tasks + recommended adjustments/changes/additions
