from pathlib import Path
from typing import IO, Any, Callable

from loguru import logger
from omegaconf import DictConfig, OmegaConf

from mlbnb.file import ensure_exists, ensure_parent_exists
from mlbnb.namegen import gen_run_name


class ExperimentPath:
    root: Path
    name: str

    def __init__(self, root: Path | str, name: str):
        self.root = Path(root) / name
        self.name = name
        ensure_exists(root)

    @staticmethod
    def from_config(cfg: Any, root: Path) -> "ExperimentPath":
        """
        Find an existing experiment path that matches the given config, or create a new
        one.

        :param cfg: The DictConfig object to convert to a path.
        :param root: The root directory to start from.
        """
        path = get_config_path(cfg, root)
        config_path = path.at("cfg.yaml")
        OmegaConf.save(cfg, config_path)
        return path

    @staticmethod
    def from_path(path: Path) -> "ExperimentPath":
        """
        Create an ExperimentPath from an existing path.

        :param path: The path to the experiment directory.
        """
        return ExperimentPath(path.parent, path.name)

    def at(self, relative_path: str | Path) -> Path:
        """
        Return a path relative to the root, creating required directories.
        """
        path = self.root / relative_path
        ensure_parent_exists(path)
        return path

    def open(self, relative_path: str | Path, mode: str = "r") -> IO[Any]:
        """
        Open a file relative to the root, creating required directories.
        """
        path = self.at(relative_path)
        return path.open(mode)

    def get_config(self) -> DictConfig:
        """
        Load the config file associated with this experiment path.
        """
        config_path = self.at("cfg.yaml")
        config = OmegaConf.load(config_path)
        return config  # type: ignore

    def __str__(self) -> str:
        return str(self.root)

    def __repr__(self) -> str:
        return f"ExperimentPath({self.root})"


PredicateType = Callable[[Any], bool]


def get_experiment_paths(
    root: Path, predicates: PredicateType | list[PredicateType] = lambda _: True
) -> list[ExperimentPath]:
    """
    Get all experiment paths in a directory matching a filter.

    :param root: The root directory to recursively search in.
    :param predicates: A filter (or list of filters) that takes a config
        object and returns whether or not the path should be included.
    """
    if not isinstance(predicates, list):
        predicates = [predicates]

    paths = root.rglob("*/cfg.yaml")
    paths = [ExperimentPath.from_path(path.parent) for path in paths]
    paths = [
        path for path in paths if _matches_predicates(path.get_config(), predicates)
    ]
    logger.info("Found {} matching experiment path(s)", len(paths))
    return paths


def _matches_predicates(cfg: Any, predicates: list[PredicateType]) -> bool:
    return all(predicate(cfg) for predicate in predicates)


def get_config_path(query_cfg: Any, root: Path) -> ExperimentPath:
    query_yaml = OmegaConf.to_yaml(query_cfg)

    def matches_entire_cfg(cfg: Any) -> bool:
        cfg_yaml = OmegaConf.to_yaml(cfg)
        return cfg_yaml == query_yaml

    matching_paths = get_experiment_paths(root, matches_entire_cfg)

    if len(matching_paths) == 0:
        new_path = root / gen_run_name()
        logger.info("Creating new experiment path: {}", new_path)
        return ExperimentPath(root, gen_run_name())

    if len(matching_paths) > 1:
        logger.warning(
            "Multiple experiment paths found for config: {}, selecting latest",
            matching_paths,
        )
        return matching_paths[-1]
    return matching_paths[0]
