# cybersecurity-checker

**Heroku Link:** [https://cybersecurity-checker.herokuapp.com/](https://cybersecurity-checker.herokuapp.com/)


### Repository Organization
**directories**
- assets: files containing metadata
- static: JS and CSS files
- templates: HTML files
- tronto: tronto-related python code

**python files**
- app.py: flask endpoints and functions
- tronto_wrapper.py: tronto wrapper class
- twitter.py: pulling tweet ids w/ Twitter API

**heroku files**
- Procfile: specify deployment config
- requirements.txt: libraries to install
- runtime.txt: specify code lang versions

TODO:
- handle/ignore entered tags that are not in ontology list
- add warning label tag if critical severity
- maybe change showing up order
