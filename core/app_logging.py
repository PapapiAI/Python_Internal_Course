import logging
from colorlog import ColoredFormatter
from core.trace import trace_id_ctx


class TraceIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = trace_id_ctx.get() or "n/a"
        return True

# Gọi 1 lần khi app start để
# tạo formatter có %(trace_id)s
# và gắn TraceIdFilter vào root logger
def setup_logging(sql_echo: bool = False) -> None:
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    trace_filter = TraceIdFilter()

    # Nếu root đã có handler (thường do uvicorn cấu hình), gắn filter vào các handler đó
    if root.handlers:
        for h in root.handlers:
            h.addFilter(trace_filter)
    else:
        # Nếu chưa có handler nào, tự tạo handler console theo format tự cấu hình
        handler = logging.StreamHandler()
        formatter = ColoredFormatter(
            fmt="%(log_color)s %(asctime)s %(levelname)s [trace_id=%(trace_id)s] %(name)s: %(message)s",
            log_colors={
                "DEBUG": "white",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            }
        )
        handler.setFormatter(formatter)
        handler.addFilter(trace_filter)
        root.addHandler(handler)

    # DEV ONLY: bật SQLAlchemy engine log qua hệ logging hiện tại
    sa_logger = logging.getLogger("sqlalchemy.engine")
    sa_logger.setLevel(logging.INFO if sql_echo else logging.WARNING)
    sa_logger.propagate = True
