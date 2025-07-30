from .plugin import   CrudToolsModule
##
# from fastpluggy.fastpluggy import FastPluggy
# from .config import CrudConfig
# from .router import crud_router as module_router
# from .template_tools import url_for_crud
#
# __module_settings__ = CrudConfig
#
# def on_load(fast_pluggy: FastPluggy):
#     # Register our helper. We assume that `url_for` is already available in the environment.
#     fast_pluggy.templates.env.globals["url_for_crud"] = url_for_crud
#
#     crud_routes = [
#         route
#         for route in fast_pluggy.app.routes
#         if isinstance(route, APIRoute) and route.tags and "crud_tools" in route.tags
#     ]
#
#     # Optionally, create a mapping of route aname to URL path
#     crud_routes_map = {route.name: route.path for route in crud_routes}
#     FastPluggy.register_global('crud_routes', crud_routes_map)
#
#     from .crud_admin_registry import CrudAdminRegistry
#
#     admin_registry = CrudAdminRegistry()
#     FastPluggy.register_global("crud_admin_registry", admin_registry)
#
#     return True
