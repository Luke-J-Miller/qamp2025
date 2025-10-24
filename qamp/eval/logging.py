from typing import Any, Dict

def open_run(output_dir: str) -> Any:
    """Create and return a run handle for JSONL logging. Week 1 stub."""
    raise NotImplementedError("Implement in Week 3+")

def append_record(handle: Any, record: Dict[str, Any]) -> None:
    """Validate and append one JSONL record. Week 1 stub."""
    raise NotImplementedError("Implement in Week 3+")

def close_run(handle: Any) -> None:
    """Close any open resources. Week 1 stub."""
    raise NotImplementedError("Implement in Week 3+")
