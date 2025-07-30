import logging
import os
from fastpluggy_official_plugins.bootstrap import init_plugins_if_needed
from tests.tools import get_list_plugins_json

logging.basicConfig(level=logging.DEBUG)


enabled_plugins= get_list_plugins_json()
print(f"Installing plugins: {', '.join(enabled_plugins)}")

# Define config
plugins_dir = os.getenv('FASTPLUGGY_PLUGIN_PATH', None)


# Run plugin init
init_plugins_if_needed(plugins_dir=plugins_dir, enabled_plugins=enabled_plugins)

# Assertions
for plugin_name in enabled_plugins:
    plugin_path = os.path.join(plugins_dir, plugin_name)
    assert os.path.isdir(plugin_path), f"{plugin_name} not copied"

print("✅ All plugins installed and copied successfully.")
