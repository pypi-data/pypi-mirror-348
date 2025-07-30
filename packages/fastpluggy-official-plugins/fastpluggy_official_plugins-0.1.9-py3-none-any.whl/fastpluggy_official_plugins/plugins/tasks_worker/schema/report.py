import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import List, Optional, Dict

from .status import TaskStatus


@dataclass
class TaskReport:
    task_id: str
    function: str
    args: List[str] = field(default_factory=list)
    kwargs: Dict[str, str] = field(default_factory=dict)
    result: Optional[str] = None
    logs: str = ""
    #duration: float = 0.0
    error: Optional[str] = None
    tracebacks: List[str] = field(default_factory=list)
    attempts: int = 0
    success: bool = False
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None  # Optional at init
    status: TaskStatus = TaskStatus.CREATED
    heartbeat: Optional[datetime] = None

    thread_native_id:str = None
    thread_ident:str = None

    finished: bool = False
    finished_at: Optional[datetime] = None


    @property
    def duration(self)->float:
        if self.end_time:
            return (self.end_time  - self.start_time).total_seconds()
        return float(0)

    # def to_db_model(self) -> 'TaskReportDB':
    #     return TaskReportDB(
    #         task_id=self.task_id,
    #         status=self.status,
    #         result=self.result,
    #         logs=self.logs,
    #         error=self.error,
    #         tracebacks=json.dumps(self.tracebacks),
    #         duration=self.duration,
    #         attempts=self.attempts,
    #         success=self.success,
    #         start_time=self.start_time,
    #         end_time=self.end_time,
    #         thread_native_id=self.thread_native_id,
    #         thread_ident=self.thread_ident,
    #         finished=self.finished,
    #         finished_at=self.finished_at,
    #     )
    #
    # def update_db_fields(self, db: Session, **fields_to_update):
    #     report = db.query(TaskReportDB).filter(TaskReportDB.task_id == self.task_id).first()
    #     if not report:
    #         return False
    #
    #     for key, value in fields_to_update.items():
    #         if hasattr(report, key):
    #             setattr(report, key, value)
    #         if hasattr(self, key):
    #             setattr(self, key, value)
    #
    #     db.commit()
    #     return True

    def print(self):
        status = "SUCCESS" if self.success else "FAILED"
        print(f"\n--- Task {self.task_id} - {self.function}({self.args}, {self.kwargs}) ---")
        print(f"Start: {self.start_time} | End: {self.end_time}")
        print(f"Duration: {self.duration:.2f}s | Attempts: {self.attempts} | Status: {status}")
        print(f"Result: {self.result}")
        if self.tracebacks:
            print(f"\nError Traceback ({len(self.tracebacks)} attempt(s)):")
            for i, err in enumerate(self.tracebacks, 1):
                print(f"\n--- Attempt {i} ---")
                print(err)
        print("Logs:")
        print(self.logs)

    def to_dict(self):
        return asdict(self)

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)
