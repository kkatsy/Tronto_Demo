# cybersecurity-checker


### Repository Organization
**directories**
- assets: ontology-related data
- static: JS and CSS files
- pipeline_qa_server: API classifier
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

**TODOs:**
- [ ] add links to CVEs in table to NVD CVE database site
- [ ] make CVE codes not split on dashes in table breaks
- [ ] add result descriptions + blurbs
- [ ] add separate spinner for tweets
- [ ] filter out duplicate tweets better
- [ ] filter out tweets that don't contain dependency/CVE names
- [ ] fix tweet query bug -> missing last dependency
- [ ] fill out research track application for twitter api (still need funding info)
- [ ] prettify things: maybe add texture, side panels, icons to tabs/buttons
- [x] add url scraper for QA

# ssh -N -f -L localhost:9801:localhost:9801 kkatsy@errol.ucdavis.edu
# ssh -N -f -L localhost:9802:localhost:9802 kkatsy@errol.ucdavis.edu
