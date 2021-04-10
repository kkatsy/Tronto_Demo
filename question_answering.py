import requests

def answer_to_question(question):
    question = "Is there a link to CVE?"
    context = """Apple has patched the critical vulnerability affecting the Sudo application on macOS devices. Although an update had already been released for the other affected operating systems, the macOS version of the security bug remained exploitable until now.
    The sudo app is used by administrators to grant root access to other users. However, earlier this month, it was discovered that it was vulnerable to a privilege escalation attack that would allow a low-privilege user to gain root-level access either by injecting malware or carrying out a brute force attack.
    Initially, it was believed that this sudo vulnerability only affected Linux and BSD operating systems but researcher Matthew Hickey then discovered that the bug, tracked as CVE-2021-3156, could be exploited on mac devices as well with just a few minor tweaks.
    We've built a list of the best endpoint protection software around Check out our roundup of the best malware removal tools Also, these are the best ransomware protection services on the market Priority patches However, it hasn’t taken long for Apple to patch the Sudo macOS application. A security update for macOS Big Sur 11.2, macOS Catalina 10.15.7, and macOS Mojave 10.14.6 is now available and should be applied as a priority.
    RECOMMENDED VIDEOS FOR YOU...Individuals with devices running the sudo app that want to check whether they are at risk from the CVE-2021-3156 vulnerability, whether they are running Linux, macOS, or BSD operating systems, can run the command “sudoedit -s /”. If the system remains vulnerable, it will respond with an error message starting with “sudoedit:” while a patched system will respond with an error that starts with “usage:”.
    In addition to patching the sudo vulnerability, fans of Apple antivirus news will be pleased to hear that the new security update also fixes two arbitrary code execution flaws affecting Intel graphics drivers.
    """

    url = "http://0.0.0.0:9801/qa/pred"
    query = {"question": question, "context": context}
    pred = requests.post(url=url, json=query)
    return pred.json()['answer']
