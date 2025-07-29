# plugin.py
import logging
from typing import Annotated, Any

from fastpluggy.core.database import session_scope, create_table_if_not_exist
from fastpluggy.core.menu.schema import MenuItem
from fastpluggy.core.module_base import FastPluggyBaseModule
from fastpluggy.core.tools.inspect_tools import InjectDependency
from fastpluggy.core.tools.install import is_installed

from .config import RedisToolsSettings
from .router import redis_router


class RedisToolsPlugin(FastPluggyBaseModule):
    module_name: str = "redis_tools"
    module_version: str = "0.0.1"

    module_menu_name: str = "Redis Tools"
    module_menu_icon:str = "fa-solid fa-database"
    module_menu_type: str = "main"

    module_settings: Any = RedisToolsSettings
    module_router: Any = redis_router

    depends_on: dict = {}

    optional_dependencies: dict = {
        "tasks_worker": ">=0.1.0",
    }

    def on_load_complete(self, fast_pluggy: Annotated["FastPluggy", InjectDependency]) -> None:
        settings: RedisToolsSettings = RedisToolsSettings()

        # Add UI menu entries
        fast_pluggy.menu_manager.add_parent_item(
            menu_type='main',
            item=MenuItem(label="Redis Tools", icon="fa-solid fa-database", parent_name=self.module_name)
        )

        fast_pluggy.menu_manager.add_menu_item(
            menu_type='main',
            item=MenuItem(
                url=fast_pluggy.app.url_path_for('redis_browser'),
                label="Redis Browser",
                icon='fa-solid fa-table-list',
                parent_name=self.module_name
            )
        )

        # Register task for cleaning expired keys if tasks_worker is available
        if settings.enable_clean_expired_keys and is_installed("tasks_worker"):
            try:
                from tasks_worker.repository.scheduled import ensure_scheduled_task_exists
                
                # Import the task function
                from .redis_connector import RedisConnection

                def clean_redis_keys():
                    """Clean up Redis keys that are about to expire"""
                    conn = RedisConnection()
                    if not conn.test_connection():
                        logging.error("Cannot connect to Redis server")
                        return {"error": "Cannot connect to Redis server"}
                    
                    keys = conn.get_keys()
                    deleted = 0
                    for key_info in keys:
                        if key_info.ttl == 0:  # About to expire
                            conn.delete_key(key_info.key)
                            deleted += 1
                    return {"deleted_keys": deleted}
                
                # Register the task with the scheduler
                with session_scope() as db:
                    ensure_scheduled_task_exists(
                        db=db,
                        function=clean_redis_keys,
                        task_name="clean_redis_keys",
                        interval=settings.clean_expired_keys_interval,
                    )
            except ImportError:
                logging.warning("tasks_worker module is not available for scheduling tasks")