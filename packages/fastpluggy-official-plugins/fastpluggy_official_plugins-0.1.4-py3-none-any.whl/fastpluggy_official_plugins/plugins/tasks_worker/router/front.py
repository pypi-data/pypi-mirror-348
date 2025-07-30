import logging

from fastapi import Request, Depends, APIRouter
from fastapi.responses import HTMLResponse
from fastpluggy.core.database import get_db
from fastpluggy.core.dependency import get_view_builder
from fastpluggy.core.view_builer.components.button import AutoLinkView
from fastpluggy.core.view_builer.components.custom import CustomTemplateView
from fastpluggy.core.view_builer.components.debug import DebugView
from fastpluggy.core.view_builer.components.list import ListButtonView
from fastpluggy.core.view_builer.components.table import TableView
from fastpluggy.fastpluggy import FastPluggy

from .api_tasks import get_task_context_reports_and_format
from .tools.task_form import TaskFormView
from ..models.context import TaskContextDB
from ..models.report import TaskReportDB

front_task_router = APIRouter(
    tags=["task_router"],
)


@front_task_router.get("/", response_class=HTMLResponse, name="dashboard_tasks_worker")
async def dashboard(request: Request, view_builder=Depends(get_view_builder), ):
    return view_builder.generate(
        request,
        title="List of tasks",
        items=[
            ListButtonView(buttons=[
                AutoLinkView(label="Run a Task", route_name="run_task_form"),
                AutoLinkView(label="See Lock Tasks", route_name="view_task_locks"),
                AutoLinkView(label="See Running Tasks", route_name="list_running_tasks"),
                AutoLinkView(label="See notifier", route_name="view_notifier"),
                AutoLinkView(label="Debug", route_name="list_threads"),
            ]),
            CustomTemplateView(
                template_name="tasks_worker/dashboard.html.j2",
                context={
                    "request": request,
                    "url_submit_task": request.url_for("submit_task"),
                    "url_list_tasks": request.url_for("list_tasks"),
                    "url_detail_task": request.url_for("task_details", task_id="TASK_ID_REPLACE"),
                    "url_get_task": request.url_for("get_task", task_id="TASK_ID_REPLACE"),
                    #"ws_logs_url": f"ws://{request.client.host}:{request.url.port or 80}" + request.url_for(
                    #    "stream_logs", task_id="TASK_ID_REPLACE").path

                }
            ),
        ]
    )
    # TODO : add a retry button


@front_task_router.get("/task/{task_id}/details", name="task_details")
def task_details(
        request: Request,
        task_id: str,
        view_builder=Depends(get_view_builder),
        db=Depends(lambda: next(get_db())),
):
    task_info = get_task_context_reports_and_format(db, task_id=task_id)
    if not task_info:
        return view_builder.generate(request, title="Task not found", items=[
            ListButtonView(buttons=[
                AutoLinkView(label="Return to list", route_name="dashboard_tasks_worker"),
            ])
        ])

    task = task_info[0]
    task_context = db.query(TaskContextDB).filter(TaskContextDB.task_id == task_id).first()
    task_report = db.query(TaskReportDB).filter(TaskReportDB.task_id == task_id).first()
    items = [
        CustomTemplateView(
            template_name='tasks_worker/task_details.html.j2',
            context={
                "request": request,
                "task_context": task_context,
                "task_report": task_report,
                "url_retry_task": request.url_for("retry_task", task_id=task_id),

            }
        ),

        ListButtonView(buttons=[
            AutoLinkView(label="Return to task list", route_name="dashboard_tasks_worker"),
        ])
    ]

    return view_builder.generate(
        request,
        title=f"Task {task_id} overview",
        items=items
    )


@front_task_router.get("/run_task", name="run_task_form")
def run_task_form(request: Request, view_builder=Depends(get_view_builder), ):
    return view_builder.generate(
        request,
        title="Run a Task",
        items=[
            TaskFormView(
                title="Run a Task",
                submit_url=str(request.url_for("submit_task")),
                mode="create_task",
            )
        ]
    )


@front_task_router.get("/running_tasks", name="list_running_tasks")
def list_running_tasks(request: Request, view_builder=Depends(get_view_builder)):
    from ..runner import TaskRunner
    runner: TaskRunner = FastPluggy.get_global("tasks_worker")

    task_data = [
        {
            "task_id": task_id,
            "status": status,
        }
        for task_id, status in runner.get_all_active_tasks()
    ]
    logging.info(f"task_data: {task_data}")
    return view_builder.generate(
        request,
        title="Running Tasks",
        items=[
            TableView(
                data=task_data,
                title="Currently Running Tasks",
                field_callbacks={
                    #   "task_id": lambda res: f'<a href"{str(request.url_for("task_details", task_id=res))}">{res}</a>' if res else res,
                },
                links=[
                    AutoLinkView(
                        label="Details",
                        route_name="task_details",
                        #param_mapping={"task_id": "task_id"}
                    ),
                    AutoLinkView(
                        label="Cancel",
                        route_name="cancel_task",
                        #param_mapping={"task_id": "task_id"},
                        css_class="btn btn-danger"
                    )
                ],
            ),
            DebugView(data=task_data, collapsed=True)
        ]
    )
