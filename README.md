# cybersecurity-checker

**Demo Link:** [https://cybersecurity-checker.herokuapp.com/](https://cybersecurity-checker.herokuapp.com/)

**TODOs:**
- [x] connect chatbot to backend, partially re-write
- [x] clear chatbot chat on clear
- [x] fix uri encoding bug so won't randomly crash
- [x] add default values to demo input
- [x] remove app name field (for now...), tweak input directions
- [x] add dismissible instructions alert
- [x] handle entered dependencies that aren't in ontology
- [x] change results format: css, add not_in_onto, add info
- [x] handle non-vulnerable results
- [x] maybe separate overall results from table tab
- [x] gather known context for QA from descriptions + basic data
- [x] try out Dian's QA api + add api call
- [x] gather canary context for QA from tweets + links
- [x] try getting dependency query tweets (name, name+version, hashtags), maybe CVEs
- [x] filter tweets before sending through classifiers
- [x] use most recent CVEs from tweet queries if too many
- [ ] connect charts to backend, maybe add more/different charts
- [ ] add tweet error handling if no tweets are found
- [ ] add links to CVEs in table to NVD CVE database site
- [ ] make CVE codes not split on dashes in table breaks
- [ ] add result descriptions + blurbs
- [ ] error handling on the off-chance that something goes wrong

- [ ] fill out research track application for twitter api (still need funding info)
- [ ] eventually will need modules for classifiers not apis so demo is usable?
- [ ] try making ontology for 2021 or recent instead of 2019 (Prof Aranovich doing)
- [ ] prettify things: maybe add texture, side panels, icons to tabs/buttons

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
