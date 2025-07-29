from ..credentials.cyberark import Cyberark
from decouple import Config


def plaintext(cred: str, cfg: Config) -> str:
    """
    Plain text mapper returns cred as is
    """
    return cred


def cyberark_umnet(cred: str, cfg: Config) -> str:
    """
    Looks up a credential in the cyberark UMnet environment
    """
    c = Cyberark(env_file=cfg.get("CYBERARK_ENV_FILE"), environment="UMNET")
    return c.query_cyberark(cred)


def cyberark_nso(cred: str, cfg: Config) -> str:
    """
    Looks up a credential in the cyberark NSO environment
    """
    c = Cyberark(env_file=cfg.get("CYBERARK_ENV_FILE"), environment="NSO")
    return c.query_cyberark(cred)

