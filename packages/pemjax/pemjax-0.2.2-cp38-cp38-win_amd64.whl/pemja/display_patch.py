import importlib.util
import importlib.metadata
from typing import Tuple, Union
import sys

# TODO: This doesn't work for all packages (`bs4`, `faiss`, etc.)
def _is_package_available(pkg_name: str, return_version: bool = False) -> Union[Tuple[bool, str], bool]:
    # Check if the package spec exists and grab its version to avoid importing a local directory
    package_exists = importlib.util.find_spec(pkg_name) is not None
    package_version = "N/A"
    if package_exists:
        try:
            # Primary method to get the package version
            package_version = importlib.metadata.version(pkg_name)
        except importlib.metadata.PackageNotFoundError:
            # Fallback method: Only for "torch" and versions containing "dev"
            if pkg_name == "torch":
                try:
                    package = importlib.import_module(pkg_name)
                    temp_version = getattr(package, "__version__", "N/A")
                    # Check if the version contains "dev"
                    if "dev" in temp_version:
                        package_version = temp_version
                        package_exists = True
                    else:
                        package_exists = False
                except ImportError:
                    # If the package can't be imported, it's not available
                    package_exists = False
            else:
                # For packages other than "torch", don't attempt the fallback and set as not available
                package_exists = False
        # logger.debug(f"Detected {pkg_name} version: {package_version}")
    if return_version:
        return package_exists, package_version
    else:
        return package_exists

if _is_package_available("tqdm"):
    """tqdm patch"""
    import tqdm
    import time
    class CustomTqdm(tqdm.tqdm):
        def update(self, n=1):
            if time.time() - self.last_print_t > self.mininterval:
                print(file=self.fp, flush=True)
            super().update(n)

    # replace
    sys.modules["tqdm"].tqdm = CustomTqdm
    try:
        import tqdm.auto
        tqdm.auto.tqdm = CustomTqdm  # replace tqdm.auto.tqdm
    except ImportError:
        pass  # tqdm.auto not available

if _is_package_available("rich"):
    """rich.progress patch"""
    import rich.progress
    from rich.console import Console
    from collections.abc import Iterable

    OriginalProgress = rich.progress.Progress

    class CustomProgress(OriginalProgress):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._custom_console = Console()
            self.tasks_info = {}

        def add_task(self, description, total=None, completed=0, **kwargs):
            """save task info"""
            task_id = super().add_task(description, total=total, completed=completed, **kwargs)

            self.tasks_info[task_id] = {
                "description": description,
                "total": total, # may be None, will be updated in track()
                "completed": completed,
                "last_updated":time.time()
            }

            self._custom_console.print(f"Task [{task_id}] {description} created with total count: {total}")
            return task_id

        def update(self, task_id, advance=0, **kwargs):
            """update progress information of the task"""
            if task_id in self.tasks_info:
                if "total" in kwargs and kwargs["total"] is not None:
                    self.tasks_info[task_id]["total"] = kwargs["total"]

                task = self._tasks[task_id]
                new_completed = task.completed

                if advance:
                    new_completed += advance
                elif "completed" in kwargs:
                    new_completed = kwargs["completed"]

                self.tasks_info[task_id]["completed"] = new_completed
                total = self.tasks_info[task_id]["total"]

                if total is None:
                    total = task.total
                    self.tasks_info[task_id]["total"] = total

                if total is None or total == 0:
                    percentage = 0
                else:
                    percentage = (new_completed / total) * 100

                if time.time() - self.tasks_info[task_id]["last_updated"] >= 1: # 每秒更新一次
                    des = self.tasks_info[task_id]["description"]
                    self._custom_console.print(
                        f"Task [{task_id}] {des} updated: {new_completed}/{total} ({percentage:.1f}%)"
                    )
                    self.tasks_info[task_id]["last_updated"] = time.time()
            return super().update(task_id, advance=advance, **kwargs)

        def track(self, sequence, description="Working...", total=None, **kwargs):
            """rewrite track to catch all updates"""
            self._custom_console.print(f"Tracing task: {description}")

            task_id = self.add_task(description, total=total)
            sequence = iter(sequence) if not isinstance(sequence, Iterable) else sequence

            # total not defined initially, check for update
            if total is None:
                try:
                    total = len(sequence)
                    self.update(task_id, total=total)
                    self.tasks_info[task_id]["total"] = total
                    self._custom_console.print(f"Task [{task_id}] updated total count: {total}")
                except (TypeError, AttributeError):
                    pass

            # just make sure additional operations are executed
            super().track(sequence, total=total, task_id=task_id, description=description, **kwargs)
            index = 0
            try:
                for index, value in enumerate(sequence):
                    yield value
                    self.update(task_id, advance=1)
            finally:
                if task_id in self._tasks:
                    final_total = self._tasks[task_id].total
                    if final_total is not None:
                        self.update(task_id, completed=final_total)
                    else:
                        self.update(task_id, completed=index + 1)

    # replace rich.progress.Progress
    sys.modules["rich.progress"].Progress = CustomProgress
    rich.progress.Progress = CustomProgress

