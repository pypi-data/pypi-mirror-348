import importlib.resources
import logging
import os.path
import shutil
from pathlib import Path



def init_plugins_if_needed(plugins_dir: str, enabled_plugins: list):
    plugins_dir = Path(plugins_dir)

    from fastpluggy_official_plugins import plugins as official_plugins
    plugins_embedded = importlib.resources.files(official_plugins)
    logging.debug(f"Plugins embedded: {plugins_embedded}")

    for plugin_name in enabled_plugins:
        src = plugins_embedded / plugin_name
        dest = Path(os.path.join(plugins_dir, plugin_name))

        logging.debug(f"Copying {src} -> {dest}")
        logging.debug(f"src: {src.exists()}, dest: {dest.exists()}")

        if not dest.exists() and src.is_dir():
            shutil.copytree(src, dest)
            logging.debug(f"Copied {src} -> {dest}")

        # Try installing requirements
        from fastpluggy.core.tools.install import install_requirements
        req_file = dest / "requirements.txt"
        logging.debug(f"Installing requirements from {req_file}")
        install_requirements(str(req_file))