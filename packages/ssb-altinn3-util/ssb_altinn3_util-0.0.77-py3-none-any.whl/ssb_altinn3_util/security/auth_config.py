import os
import configparser
import logging

from ssb_altinn3_util.security.helpers.token_validators import (
    ValidatorConfig,
    BaseTokenValidator,
    AuthSSBValidator,
    LabIdValidator,
)

logger = logging.getLogger()

auth_parser = configparser.ConfigParser()

CONFIG_FILE_PATH = os.path.join(os.getcwd(), "app/auth.config")

if not os.path.exists(CONFIG_FILE_PATH):
    logger.warning("NO auth.config EXISTS!")

auth_parser.read(CONFIG_FILE_PATH)
SUV_ENVIRONMENT = os.getenv("NAIS_APP_NAME").split("-")[0]

if not SUV_ENVIRONMENT:
    logger.warning("Unable to determine runtime SUV environment!")


providers = auth_parser["providers"]["keys"].split(",")
envs = auth_parser["providers"]["envs"].split(",")

environment = SUV_ENVIRONMENT if SUV_ENVIRONMENT in envs else None

validators: dict[str, BaseTokenValidator] = {}

if environment:
    for p in providers:
        prv = auth_parser[f"provider_{p}_{environment}"]
        config = ValidatorConfig(
            authority=prv["authority"],
            issuer=prv["trusted_issuer"],
            audiences=prv["audiences"],
        )

        if p == "labId":
            validators[config.issuer] = LabIdValidator(config=config)
        elif p == "authSSB":
            validators[config.issuer] = AuthSSBValidator(config=config)
        else:
            logger.error(
                "Unsupported auth provider.  Unable to configure authentication"
            )


class AuthConfig:
    enforce_token_validation: bool
    auth_authority_url: str
    trusted_issuer: str
    allowed_audiences: list[str]

    def __init__(self):
        self.auth_authority_url = os.getenv("AUTH_AUTHORITY_URL")
        self.allowed_audiences = os.getenv("VALID_AUDIENCES", "").split(",")
        self.trusted_issuer = os.getenv("TRUSTED_ISSUER")
        self.enforce_token_validation = bool(os.getenv("VALIDATE_TOKEN", None))
