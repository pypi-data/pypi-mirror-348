from typing import Optional
from decouple import Config

from nornir import InitNornir
from nornir.core import Nornir

from .logging import configure_nornir_logging
from .connection_options import configure_connection_options
from .device_credentials import update_nornir_credentials

from ..loaders import parse_nb_roles, parse_credential_map


def nornir_setup(
    cfg: Config,
    log_level: str = "DEBUG",
    log_globally: Optional[bool] = False,
    log_to_console: Optional[bool] = False,
    device_filter: Optional[str] = None,
    role_filter: Optional[str] = None,
) -> Nornir:
    """
    Initializes Nornir to point at netbox, and to only care about active
    devices tied to a specific subset of device roles.
    Sets up logging. Populates default and custom passwords from cyberark. Returns
    customized Nornir instance
    """

    logfile = cfg.get("LOG_DIR") + "/agador.log"

    configure_nornir_logging(log_level, log_globally, logfile, log_to_console)

    nb_url = cfg.get("NB_URL")

    filter_params = {"status": "active", "has_primary_ip": "True"}

    # Restrict what the netbox inventory plugin pulls if it was indicated
    # on the CLI
    if device_filter:
        filter_params["name"] = device_filter
    elif role_filter:
        filter_params["role"] = [role_filter]

    # if it wasn't indicated on the CLI, pull list of roles from command map
    else:
        nb_roles = parse_nb_roles(cfg)
        if nb_roles:
            filter_params["role"] = nb_roles

    # Nornir initialization
    nr = InitNornir(
        runner={
            "plugin": "multiprocess",
            "options": {
                "num_workers": int(cfg.get("NUM_WORKERS")),
            },
        },
        inventory={
            "plugin": "NetBoxInventory2",
            "options": {
                "nb_url": nb_url,
                "nb_token": cfg.get("NB_TOKEN"),
                "filter_parameters": filter_params,
                "ssl_verify": False,
            },
        },
        logging={
            "enabled": False,
        },
    )

    update_nornir_credentials(nr, parse_credential_map(cfg))
    configure_connection_options(nr)

    return nr
