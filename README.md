# cybersecurity-checker

**Heroku Link:** [https://cybersecurity-checker.herokuapp.com/](https://cybersecurity-checker.herokuapp.com/)

### Files Specs
- app.py: contains flask framework
- tronto.py: contains Tronto functions wrapper
- twitter.py: contains twitter code to pull tweets

### UI Adds:
-[ ] Add header
-[ ] Bootstrap tags input
-[ ] Progress Bar
-[ ] Prettier Results

### Tronto_from_OWL Notes
- load ontology as OWL document(XML doc with specifications)
- models relations between configurations and vulnerabilities
- domains modeled based on NVD and NIST's CPE, w CVEs being individual instances
- basic document has property *has_vulnerability*: configuration is domain and vulnerability is range
- other properties: *is_vulnerability_of*, *has_severity_score*, *depends_on*
- JSON is dict, with CVE_Items keys has value of list of CVEs; each CVE itself is dict; item in dict contains CVE info/metadata
-
