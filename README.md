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
- [ ] filter tweets better
- [x] add new tronto file
- [x] update is_vulnerable function
- [x] add home page -> button click -> demo flow
- [x] add home page -> button click -> about page
- [ ] add methodology info to about page
- [x] add spinner while tweets + info loads
- [x] init gcloud app engine
- [x] tweak chatbot
- [ ] figure out where ner/debug_bertoverflow


# ssh -N -f -L localhost:9801:localhost:9801 kkatsy@errol.ucdavis.edu
# ssh -N -f -L localhost:9802:localhost:9802 kkatsy@errol.ucdavis.edu
# scp kkatsy@errol.ucdavis.edu:/home/raranovi/tronto_f.owl /Users/kk/Desktop/tronto_g.owl
