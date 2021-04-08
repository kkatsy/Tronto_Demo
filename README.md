# cybersecurity-checker

**Demo Link:** [https://cybersecurity-checker.herokuapp.com/](https://cybersecurity-checker.herokuapp.com/)

**todos:**
- [x] connect chatbot to backend, partially re-write
- [x] fix uri encoding bug
- [x] add default values to demo input
- [x] remove app name field (for now...), tweak input directions
- [x] add dismissible instructions alert
- [x] handle entered dependencies that aren't in ontology
- [ ] change results format: css, add not_in_onto, add info
- [ ] gather context for QA from description + tweets + links
- [ ] try out Dian's QA api
- [ ] connect charts to backend, maybe add more/different charts
- [ ] try getting dependency query tweets (name, name+version, hashtags)
- [ ] add links to CVEs in table to NVD CVE database site
- [ ] make CVE codes not split on dashes in table breaks
- [ ] try making ontology for 2021 or recent instead of 2019
- [ ] add result field descriptions
- [ ] handle non-vulnerable results
- [ ] error handling on the off-chance that something goes wrong
- [ ] fill out research track application for twitter api
- [ ] think: maybe separate overall results from table tab
- [ ] think: could dependencies be visualized as a tree... it'd be neat

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
