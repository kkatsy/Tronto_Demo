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

**Done and Todo:**
- [x] add urls when initially loading
- [x] make get_url_content exception proof
- [x] run qa_server locally
- [x] remove tweet_pipeline (for now)
- [x] update urls only when new queries
- [x] figure out why tweets aren't showing up
- [x] filter tweets better
- [x] add new tronto file
- [x] update is_vulnerable function
- [x] add home page -> button click -> demo flow
- [x] add home page -> button click -> about page
- [x] add methodology info to about page
- [x] add spinner while tweets + info loads
- [x] init gcloud app engine
- [x] tweak chatbot
- [x] don't allow QA before tweet + url info loads
- [x] fix filtering so include queries
- [x] figure out where ner/debug_bertoverflow
- [x] get tweet_pipeline to work locally
- [ ] clean up code + print statements + comments
- [ ] move entire demo to errol
- [ ] get tweet_pipeline to work on errol
- [ ] move entire demo to gcloud: compute engine for main and gateway for APIs


ssh -N -f -L localhost:9801:localhost:9801 kkatsy@errol.ucdavis.edu
scp -r kkatsy@errol.ucdavis.edu:/mnt/dian/tronto/exist /Users/kk/Desktop/
