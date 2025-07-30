import json

from bs4 import BeautifulSoup
import requests

from .._constructors import _Livewire2, SSLAdapterCF, GLOBAL_UA

class Tempdashmail_id(_Livewire2):
    """An API Wrapper around the https://temp-mail.id/ website. From experience very fast."""

    def __init__(self, name: str=None, domain: str=None, exclude: list[str]=None):
        """
            Generate an inbox\n
            Args:\n
            name - name for the email, if None a random one is chosen\n
            domain - the domain to use, domain is prioritized over exclude\n
            exclude - a list of domain to exclude from the random selection\n
        """
        
        super().__init__(
            urls={
                "base": "https://temp-mail.id",
                "mailbox": "https://temp-mail.id/mailbox/",
                "app": "https://temp-mail.id/livewire/message/frontend.app",
                "actions": "https://temp-mail.id/livewire/message/frontend.actions"
            },
            order=0, cf_protx=True, name=name, domain=domain, exclude=exclude
            )


    @staticmethod
    def get_valid_domains() -> list[str] | None:
        """
            Returns a list of a valid domains, None if failure
        """
        s = requests.Session()
        s.mount("https://", SSLAdapterCF)
        r = s.get("https://temp-mail.id/", headers={
            "User-Agent": GLOBAL_UA
        })

        if r.ok:
            soup = BeautifulSoup(r.text, "lxml")
            data = json.loads(soup.find(lambda tag: tag.name == "div" and "in_app: true" in tag.get("x-data", "") and ( "wire:initial-data" in tag.attrs ))["wire:initial-data"])

            return data["serverMemo"]["data"]["domains"]
