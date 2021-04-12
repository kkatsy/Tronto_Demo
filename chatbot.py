import requests


class ChatBot:
    def __init__(self):
        self.known_context = None
        self.canary_context = None
        self.combined_context = None

    @staticmethod
    def get_known_context(description_list, dependency_list, cve_list):
        descriptions = ' '.join(description_list)
        dependency_info = 'Your application has the dependencies ' + ', '.join(dependency_list) + '.'
        cve_info = 'Your application has the vulnerabilities: ' + ', '.join(cve_list) + '.'

        known_context = descriptions + ' ' + dependency_info + '. ' + cve_info
        return known_context

    @staticmethod
    def get_canary_context(tweet_list):
        tweet_text = ' '.join(tweet_list)
        return tweet_text

    def answer_to_question(self, question):
        # question = "Is there a link to CVE?"
        # print(self.combined_context)
        url = "http://0.0.0.0:9801/qa/pred"
        query = {"question": question, "context": self.combined_context}
        pred = requests.post(url=url, json=query)
        return pred.json()

    def update_data(self, description_list, dependency_list, cve_list, tweet_list):
        self.known_context = self.get_known_context(description_list, dependency_list, cve_list)
        self.canary_context = self.get_canary_context(tweet_list)
        self.combined_context = self.known_context + ' ' + self.canary_context
