from contextvars import ContextVar
from functools import wraps
from typing import Any, Dict, Callable
from contextlib import contextmanager


class AuditContext:
    def __init__(self):
        self._data: ContextVar[Dict[str, Any]] = ContextVar("audit_ctx_data", default={})
        self._reason_stack: ContextVar[list[str]] = ContextVar("audit_ctx_reason", default=[])

    def set(self, key: str, value: Any):
        ctx = self._data.get().copy()
        ctx[key] = value
        self._data.set(ctx)

    def get(self, key: str) -> Any:
        return self._data.get().get(key)

    def push_change_reason(self, reason: str):
        stack = self._reason_stack.get().copy()
        stack.append(reason)
        self._reason_stack.set(stack)

    def get_change_reason(self) -> str:
        return " -> ".join(self._reason_stack.get())

    def build_sql(self) -> str:
        ctx = self._data.get()
        reason = self.get_change_reason()
        if reason:
            ctx["change_reason"] = reason

        lines = []
        for k, v in ctx.items():
            key = f"session.myapp_{k}"
            val = str(v).replace("'", "''")
            lines.append(f"SET LOCAL {key} = '{val}';")
        return "\n".join(lines)

    @contextmanager
    def use(self, **kwargs):
        original_data = self._data.get().copy()
        ctx = original_data.copy()
        ctx.update(kwargs)
        self._data.set(ctx)
        try:
            yield
        finally:
            self._data.set(original_data)

    @contextmanager
    def use_change_reason(self, reason: str):
        original_stack = self._reason_stack.get().copy()
        stack = original_stack.copy()
        stack.append(reason)
        self._reason_stack.set(stack)
        try:
            yield
        finally:
            self._reason_stack.set(original_stack)


audit_context = AuditContext()


def with_context(**kwargs):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **fkwargs):
            with audit_context.use(**kwargs):
                return func(*args, **fkwargs)
        return wrapper
    return decorator


def with_change_reason(reason: str):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with audit_context.use_change_reason(reason):
                return func(*args, **kwargs)
        return wrapper
    return decorator
