from typing import Optional, Union
from types import ModuleType

import importlib.machinery
import importlib.util

from os import getenv
from os.path import isdir
import re
import sys

import yaml
from decouple import UndefinedValueError, Config, RepositoryEnv
from cron_converter import Cron

from umnet_napalm.abstract_base import AbstractUMnetNapalm

from .mappers import credentials, save_to_db, save_to_file


class AgadorError(Exception):
    pass


class CommandMapError(Exception):
    def __init__(self, cmd: str, error_str: str):
        super().__init__(f"command map error for '{cmd}' - {error_str}")


class CredentialMapError(Exception):
    pass


def get_config_settings(cfg_file: Optional[str]) -> Config:
    """
    Get config settings from file, or if 'None' is provided, look for 'AGADOR_CFG'
    in environment
    """

    cfg_file = cfg_file if cfg_file else getenv("AGADOR_CFG")
    if not cfg_file:
        raise AgadorError("No config file provided, and no AGADOR_CFG env set!")

    try:
        return Config(RepositoryEnv(cfg_file))
    except FileNotFoundError:
        raise AgadorError(f"Cannot locate agador config file {cfg_file}")


def load_inventory_filters(file_name: str) -> ModuleType:
    """
    Loads inventory filters if they're not loaded already
    """

    # Prefer to only load the module once
    if "inventory_filters" not in sys.modules:

        loader = importlib.machinery.SourceFileLoader("inventory_filters", file_name)
        spec = importlib.util.spec_from_loader("inventory_filters", loader)
        inventory_filters = importlib.util.module_from_spec(spec)
        try:
            sys.modules["inventory_filters"] = inventory_filters
            loader.exec_module(inventory_filters)

        except Exception as e:
            raise AgadorError(f"Could not load inventory filters from {file_name}: {e}")

    # returning referece to modules for convenience
    return sys.modules["inventory_filters"]


def parse_command_map(cfg: Config) -> dict:
    """
    Parses and validates command_map file, replacing text references
    to functions to references to the actual functions where applicable.

    Future task: pydantic-based validation
    """

    db_module = save_to_db
    file_module = save_to_file

    inventory_filters = load_inventory_filters(cfg.get("INVENTORY_FILTERS"))

    with open(cfg.get("CMD_MAP"), encoding="utf-8") as fh:
        cmd_map = yaml.safe_load(fh)

    output = {}
    for cmd, data in cmd_map["commands"].items():

        output[cmd] = {}

        # validating frequency, which is required
        if "frequency" not in data:
            raise CommandMapError(cmd, "Must specify frequency")
        try:
            output[cmd]["frequency"] = Cron(data["frequency"])
        except ValueError:
            raise CommandMapError(cmd, "Invalid frequency - must be in crontab format")

        # validating umnet_napalm getter specification
        if "getter" not in data:
            raise CommandMapError(cmd, "Must specify umnet_napalm getter")
        if data["getter"] not in dir(AbstractUMnetNapalm):
            raise CommandMapError(cmd, f"Unknown umnet_napalm getter {data['getter']}")
        output[cmd]["getter"] = data["getter"]

        # validating and retrieving inventory filter fuction
        inv_filter = data.get("inventory_filter", None)
        if inv_filter:
            if inv_filter not in dir(inventory_filters):  # noqa: F821
                raise CommandMapError(cmd, f"Unknown inventory filter {inv_filter}")

            output[cmd]["inventory_filter"] = getattr(
                inventory_filters, inv_filter
            )  # noqa: F821

        # validating and retrieving save_to_file class
        file_data = data.get("save_to_file", None)
        if file_data:
            if "mapper" not in file_data:
                raise CommandMapError(cmd, "Must specify mapper for save_to_file")

            if "destination" not in file_data:
                raise CommandMapError(cmd, "Must specify destination for save_to_file")

            destination = resolve_envs(file_data["destination"], cfg)
            if not isdir(destination):
                raise CommandMapError(
                    cmd, f"Invalid desintation {destination} for save_to_file"
                )

            if file_data["mapper"] not in dir(file_module):
                raise CommandMapError(
                    cmd, f"Unknown save_to_file mapper {file_data['mapper']}"
                )

            output[cmd]["save_to_file"] = {
                "mapper": getattr(file_module, file_data["mapper"])(destination),
            }

        # validating and retrieving save_to_db class
        db_data = data.get("save_to_db", None)
        if db_data:
            if db_data not in dir(db_module):
                raise CommandMapError(cmd, f"Unknown save_to_db mapper {db_data}")

            output[cmd]["save_to_db"] = getattr(db_module, db_data)

        if not db_data and not file_data:
            raise CommandMapError(
                cmd, "Must specifiy either save_to_db or save_to_file"
            )

    return output


def parse_credential_map(cfg: Config) -> dict:
    """
    Parses and validates the credential map file, replacing references
    to filters and mappers with actual functions

    Future task: pydantic-based validation
    """
    required_default_fields = ["username", "password", "mapper", "enable"]
    required_custom_fields = ["mapper", "inventory_filter"]

    inventory_filters = load_inventory_filters(cfg.get("INVENTORY_FILTERS"))

    with open(cfg.get("CRED_MAP"), encoding="utf-8") as fh:
        cred_map = yaml.safe_load(fh)

    output = {}

    ##### default credential validation
    if "defaults" not in cred_map:
        raise CredentialMapError("Default credentials must be specified!")

    for reqd in required_default_fields:
        if reqd not in cred_map["defaults"]:
            raise CredentialMapError(f"default {reqd} is required")

    output["defaults"] = {}
    for k, v in cred_map["defaults"].items():
        if k == "mapper":
            if v not in dir(credentials):
                raise CredentialMapError(f"Invalid credential mapper {v}")
            output["defaults"]["mapper"] = getattr(credentials, v)
        else:
            output["defaults"][k] = v

    ##### custom credentials parsing
    output["custom"] = []
    seen_filters = []
    for cred in cred_map["custom"]:

        for reqd in required_custom_fields:
            if reqd not in cred:
                raise CredentialMapError(
                    f"Required custom credential {reqd} is missing"
                )

        if cred["inventory_filter"] not in dir(inventory_filters):
            raise CredentialMapError(
                f"Invalid inventory filter {cred['inventory_filter']}"
            )

        if cred["inventory_filter"] in seen_filters:
            raise CredentialMapError("Inventory filter values must be unique!")

        new_cred = {
            "inventory_filter": getattr(inventory_filters, cred["inventory_filter"]),
            "username": cred.get("username", output["defaults"]["username"]),
            "password": cred.get("password", output["defaults"]["password"]),
            "mapper": getattr(credentials, cred["mapper"]),
        }

        if "enable" in cred:
            new_cred["enable"] = cred["enable"]

        output["custom"].append(new_cred)

    return resolve_credentials(output, cfg)


def parse_nb_roles(cfg: Config) -> Union[list, None]:
    """
    Parses the list of netbox roles out of the command map
    """
    with open(cfg.get("CMD_MAP"), encoding="utf-8") as fh:
        cmd_map = yaml.safe_load(fh)

    if "netbox_roles" not in cmd_map:
        return None

    return cmd_map["netbox_roles"]


def resolve_envs(input_str: str, cfg: Config) -> str:
    """
    Takes an input string and searches for all instances of '${ENV_VAR}', replacing
    ENV_VAR with the value in the .env file. Raises an exception
    if the ENV_VAR is not found
    """
    for m in re.finditer(r"\${(\w+)}", input_str):
        var = m.group(1)
        try:
            input_str = re.sub(r"\${" + var + "}", cfg.get(var), input_str)
        except UndefinedValueError:
            raise ValueError(f"Invalid env var {m.group(1)} in {input_str}")

    return input_str


def resolve_credentials(cred_map, cfg):
    """
    Resolving all credentials in the cred map based on their
    mapper functions
    """

    # first we need to resolve all the credentials in the map
    _resolve_cred(cred_map["defaults"], cfg)
    for custom_cred in cred_map["custom"]:
        _resolve_cred(custom_cred, cfg)

    return cred_map

def _resolve_cred(cred, cfg):
    """
    Resolves enable and password fields in the credential map using the specified mapper
    """
    pw_keys = ["password", "enable"]
    for key in pw_keys:
        if key in cred:
            cred[key] = cred["mapper"](cred[key], cfg)