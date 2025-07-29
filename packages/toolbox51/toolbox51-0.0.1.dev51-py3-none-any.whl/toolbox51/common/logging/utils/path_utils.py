

from pathlib import Path

def normalize_path(p: Path) -> Path:
    if p.drive:  # 只有 Windows 上才有 drive
        return Path(p.drive.lower() + str(p)[len(p.drive):])
    return p  # 非 Windows 系统，原样返回