import requests

from .._constructors import _WaitForMail, _generate_user_data

class Inboxkitten_com(_WaitForMail):
    """An API Wrapper around the https://inboxkitten.com/ website"""

    _BASE_URL = "https://inboxkitten.com"

    def __init__(self, name: str=None, domain:str=None, exclude: list[str]=None):
        """
        Generate an inbox\n
        Args:\n
        name - name for the email, if None a random one is chosen\n
        domain - the domain to use, domain is prioritized over exclude\n
        exclude - a list of domain to exclude from the random selection\n
        """
        super().__init__(0)

        self._session = requests.Session()
        
        self.name, self.domain, self.email, self.valid_domains = _generate_user_data(name, domain, exclude, self.get_valid_domains())

    @staticmethod
    def get_valid_domains() -> list[str]:
        """
        Returns a list of valid domains of the service (format: abc.xyz) as a list. This website only has 1 domain.
        """
        return ["inboxkitten.com"]


    def get_mail_content(self, mail_id: str) -> str:
        """
        Returns the content of a given mail_id as a html string\n
        Args:\n
        mail_id - the id of the mail you want the content of
        """

        region, mail_id = mail_id.split(",", 1)
        r = self._session.get(f"{self._BASE_URL}/api/v1/mail/getHtml?region={region}&key={mail_id}")
        if r.ok:
            return r.text.rsplit("<script>", 1)[0]


    def get_inbox(self) -> list[dict]:
        """
        Returns the inbox of the email as a list with mails as dicts list[dict, dict, ...]
        """

        r = self._session.get(f"{self._BASE_URL}/api/v1/mail/list?recipient={self.name}")
        if r.ok:
            return [{
                "id": f"{email['storage']['region']},{email['storage']['key']}",
                "from": email["message"]["headers"]["from"],
                "time": email["timestamp"],
                "subject": email["message"]["headers"]["subject"]
            } for email in r.json()]