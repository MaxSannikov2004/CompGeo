import os
import re
import types
import importlib.util
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

REQUIRED_FUNCS = (
    "orient",
    "dist_point_line",
    "on_segment",
    "segments_intersect",
    "polygon_area",
    "point_in_polygon",
)

def _load_from_notebook(repo_root: Path, nb_name: str = "Лабораторная_работа_1.ipynb"):
    nb_path = repo_root / nb_name
    if not nb_path.exists():
        raise FileNotFoundError(f"Не найден ноутбук: {nb_name}")

    import nbformat

    nb = nbformat.read(str(nb_path), as_version=4)

    ns = {"__name__": "student_nb"}
    wanted = set(REQUIRED_FUNCS)

    def has_wanted_def(src: str) -> bool:
        return any(re.search(rf"^\s*def\s+{name}\s*\(", src, re.M) for name in wanted)

    for cell in nb.cells:
        if cell.get("cell_type") != "code":
            continue
        src = cell.get("source", "")
        if not src.strip():
            continue
        if re.match(r"^\s*(import|from)\s+", src):
            exec(src, ns)
            continue
        if has_wanted_def(src):
            exec(src, ns)

    mod = types.SimpleNamespace(**ns)
    return mod

def _import_lab1_py(repo_root: Path):
    path = repo_root / "lab1.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location("lab1", str(path))
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def _is_stubbed(mod) -> bool:
    # Пытаемся аккуратно вызвать функции на "безопасных" входах.
    # Если где-то вылетает NotImplementedError — считаем, что это заглушка.
    try:
        mod.orient((0,0),(1,0),(0,1))
        mod.dist_point_line((0,0), 1, 0, 0)
        mod.on_segment((0,0),(1,0),(0.5,0))
        mod.segments_intersect((0,0),(1,0),(0.5,-1),(0.5,1))
        mod.polygon_area([(0,0),(1,0),(0,1)])
        mod.point_in_polygon((0.1,0.1), [(0,0),(1,0),(1,1),(0,1)])
        return False
    except NotImplementedError:
        return True

def load_student_module():
    repo_root = Path(__file__).resolve().parents[1]

    # 1) Основной источник — ноутбук.
    mod_nb = _load_from_notebook(repo_root)
    if not _is_stubbed(mod_nb):
        mod = mod_nb
    else:
        # 2) Если в ноутбуке остались заглушки, пробуем lab1.py
        mod_py = _import_lab1_py(repo_root)
        if mod_py is None:
            mod = mod_nb  # упадём ниже с понятной ошибкой
        else:
            mod = mod_py

    for name in REQUIRED_FUNCS:
        if not hasattr(mod, name):
            raise AttributeError(f"Не найдена функция `{name}` (проверьте, что она реализована).")
    return mod

import pytest

@pytest.fixture(scope="session")
def student():
    return load_student_module()
