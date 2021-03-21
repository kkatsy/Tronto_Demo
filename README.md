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

TODOs:
- make tweet functionality usable for now
- error message if failure due to twitter api
- think about how to integrate QA and descriptions
- prettify margins/spacing and table
- handle non-vulnerable results
