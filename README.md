# cybersecurity-checker

**Heroku Link:** [https://cybersecurity-checker.herokuapp.com/](https://cybersecurity-checker.herokuapp.com/)

**todos:**
- [ ] connect chatbot to backend, maybe re-write
- [ ] gather context for QA from description + tweets + links
- [ ] try out Dian's QA api
- [ ] connect charts to backend, maybe add more/different charts
- [ ] try getting dependency query tweets (name, name+version, hashtags)
- [ ] add links to CVEs in table to NVD CVE database site
- [ ] make CVE codes not split on dashes in table breaks
- [ ] try making ontology for 2021 or recent instead of 2019
- [ ] add info about entered dependencies that aren't in ontology
- [ ] add default values to demo input
- [ ] remove app name field (for now...), tweak input directions
- [ ] add result field descriptions
- [ ] handle non-vulnerable results
- [ ] add dismissible instructions alert
- [ ] error handling on the off-chance that something goes wrong
- [ ] fill out research track application for twitter api
- [ ] think: could dependencies be visualized as a tree... it'd be cute

### Repository Organization
**directories**
- assets: files containing data
- static: JS and CSS files
- templates: HTML files
- tronto: tronto-related python code

**python files**
- app.py: flask endpoints and functions
- tronto_wrapper.py: tronto wrapper class
- twitter.py: pulling tweet ids w/ Twitter API
- question_answering.py

**heroku files**
- Procfile: specify deployment config
- requirements.txt: libraries to install
