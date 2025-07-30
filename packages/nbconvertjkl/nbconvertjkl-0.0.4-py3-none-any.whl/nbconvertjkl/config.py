"""Global configuration handling."""

import logging
import os
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)

CONFIG_FILENAMES = ['nbconvertjkl.yml', '.nbconvertjkl.yml']

DEFAULT_CONFIG = {
    "nbs": "notebooks/*.ipynb",
    "nb_read_path": "notebooks",
    "nb_write_path": "docs/_notebooks",
    "asset_write_path": "docs/assets",
    "asset_subdirs": ['figures', 'data', 'images', 'imgs', 'img'],
    "nb_nav_top": True,
    "nb_nav_bottom": True,
    "overwrite_existing": True,
}

def get_config():
    """Load config from file if present, fallback to default config."""
    for fname in CONFIG_FILENAMES:
        config_path = Path.cwd() / fname
        if config_path.exists():
            logger.debug(f"Loading config from {config_path}")
            with open(config_path) as f:
                user_config = yaml.safe_load(f) or {}
                return resolve_paths({**DEFAULT_CONFIG, **user_config})

    resolved_default = resolve_paths(DEFAULT_CONFIG.copy())
    logger.debug("No user config found. Using default config:")
    for k, v in resolved_default.items():
        logger.debug(f"  {k}: {v}")
    return resolved_default

def resolve_paths(config):
    """Ensure all paths are absolute and glob-safe."""
    root = Path.cwd()

    def normalize(p):
        return os.path.normpath(str(root.joinpath(p)))

    for key in ['nbs', 'nb_read_path', 'nb_write_path', 'asset_write_path']:
        if key in config and config[key]:
            config[key] = normalize(config[key])

    return config

def get_user_config(config_file=None, default_config=False):
    """Return the user config as a dict"""
    #TODO
    pass