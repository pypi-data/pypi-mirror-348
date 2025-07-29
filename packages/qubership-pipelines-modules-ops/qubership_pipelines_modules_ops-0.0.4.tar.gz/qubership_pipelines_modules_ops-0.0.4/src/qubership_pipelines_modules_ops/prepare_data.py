from __future__ import annotations # if sys.version_info < (3, 10)

import graphlib  # pip install graphlib_backport if sys.version_info < (3, 9)
import os
import re
import shutil
import sys
import typing
from collections import ChainMap
from copy import deepcopy
from pathlib import Path

from .report import get_pipeline_report_operations
from .utils.utils_dictionary import UtilsDictionary, HierarchicalDict
from .utils.utils_file import UtilsFile, UtilsYaml
from .utils.utils_params import StringSubstitution

import logging
logger = logging.getLogger(__name__)

if sys.version_info >= (3, 10):
    PathRepr: typing.TypeAlias = str | bytes | os.PathLike
else:
    PathRepr = typing.Union[str, bytes, os.PathLike]

_merge_dicts_func = dict.__or__ if sys.version_info >= (3, 9) else lambda d1, d2: {**d1, **d2}

_QUBERSHIP_PIPELINES_MODULES_OPS_PREFIXED_VARS_PRIORITY = os.getenv(
        'QUBERSHIP_PIPELINES_MODULES_OPS_PREFIXED_VARS_PRIORITY', 'true')
_QUBERSHIP_PIPELINES_MODULES_OPS_FALSE_CONDITION_EXIT_CODE = os.getenv(
        'QUBERSHIP_PIPELINES_MODULES_OPS_FALSE_CONDITION_EXIT_CODE', '0')


_ENV_VAR_NAME_DELIMITER_PATTERN = re.compile(r'\.|__')
def _split_var_name(n):
    return _ENV_VAR_NAME_DELIMITER_PATTERN.split(n)

def _ensure_dir(path: PathRepr):
    if path:
        os.makedirs(path, exist_ok=True)
    return path

_SKIP_LOG_CONTENT = object()
def _write_to_file_and_log(content, file: PathRepr, content_to_log = None):
    content_str = content if isinstance(content, str) else UtilsYaml.write_yaml(content)
    content_to_log_str = (
            content_str if content_to_log is None
            else None if content_to_log == _SKIP_LOG_CONTENT
            else content_to_log if isinstance(content_to_log, str)
            else UtilsYaml.write_yaml(content_to_log)
    )
    logger.info(f"Writing to {file}" + (':\n'+content_to_log_str if content_to_log_str is not None else ''))
    UtilsFile.write_file(content_str, file)

def _parse_yaml_if_file_exists(f: PathRepr):
    return UtilsYaml.read_yaml(f) if f and os.path.isfile(f) else {}

def _copy_file(src_base_dir: PathRepr, src_file: str, dst_base_dir: PathRepr, dst_file: str|None, file_key: str=None):
    src_filepath = Path(src_base_dir, src_file)
    if src_filepath.is_file():
        valid_dst_file = dst_file or src_file
        dst_filepath = Path(dst_base_dir, valid_dst_file)
        logger.info(f"Copying file {src_filepath} -> {dst_filepath}")
        _ensure_dir(dst_filepath.parent)
        shutil.copyfile(src_filepath, dst_filepath)
        return valid_dst_file
    else:
        logger.warning(f"File does not exist, path: {src_filepath}" + f", key: {file_key}"*bool(file_key))


class Layout:
    _JOB_DATA_DIR = 'job_data'
    _STORED_DATA_DIR = 'stored_data'
    _PIPELINE_OUTPUT_DIR = 'pipeline/output'
    def __init__(self, root_dir: PathRepr):
        self.root_dirpath = Path(root_dir)
        self.job_data_dirpath = self.root_dirpath / Layout._JOB_DATA_DIR
        self.stored_data_dirpath = self.root_dirpath / Layout._STORED_DATA_DIR
        self.pipeline_output_dirpath = self.root_dirpath / Layout._PIPELINE_OUTPUT_DIR


class StoredDataRegistry:
    _STAGE_DESCRIPTOR_FILENAME = 'stage.yaml'

    def __init__(self, stored_data_dir: PathRepr):
        self.stored_data_dirpath = Path(_ensure_dir(stored_data_dir))

    _UNSAFE_FILENAME_CHARS_PATTERN = re.compile(r'[^\w\- .]')
    @staticmethod
    def _get_safe_filename(s: str):
        return re.sub(StoredDataRegistry._UNSAFE_FILENAME_CHARS_PATTERN, '_', s)

    def get_stored_stage_dirpath(self, stage):
        return self.stored_data_dirpath / StoredDataRegistry._get_safe_filename(stage)

    def get_stored_job_dirpath(self, stage, job):
        return self.get_stored_stage_dirpath(stage) / StoredDataRegistry._get_safe_filename(job)

    def register_current_stage(self, stage: str) -> None:
        stage_dirpath = self.get_stored_stage_dirpath(stage)
        stage_dirname = stage_dirpath.name
        stage_descriptor_filepath = stage_dirpath / StoredDataRegistry._STAGE_DESCRIPTOR_FILENAME
        if not stage_descriptor_filepath.is_file():
            prev_stages = [ sd.get('name')
                            for subdir_path in self.stored_data_dirpath.iterdir()
                            if subdir_path.name!=stage_dirname
                                and (sd_filepath:=subdir_path/StoredDataRegistry._STAGE_DESCRIPTOR_FILENAME).is_file()
                                and (sd:=UtilsYaml.read_yaml(sd_filepath)) ]
            UtilsYaml.write_yaml({'name': stage, 'previous': prev_stages}, stage_descriptor_filepath)

    def get_registered_stages(self) -> list[str]:
        prev_stages_graph = { sd.get('name'): sd.get('previous')
                              for subdir_path in self.stored_data_dirpath.iterdir()
                              if (sd_filepath:=subdir_path/StoredDataRegistry._STAGE_DESCRIPTOR_FILENAME).is_file()
                                  and (sd:=UtilsYaml.read_yaml(sd_filepath)) }
        logger.info(f"Previous stages graph: {prev_stages_graph}")
        stages = list(graphlib.TopologicalSorter(prev_stages_graph).static_order())
        logger.info(f"Stages (ordered): {stages}")
        return stages


    class StoredJobDataRegistry:
        _FILES_DIRNAME = 'files'
        _LOGS_DIRNAME = 'logs'
        _FILES_FILENAME = 'files.yaml'
        _PARAMS_FILENAME = 'params.yaml'
        _STATS_FILENAME = 'stats.yaml'

        def __init__(self, stored_job_data_dir: PathRepr):
            self.stored_job_data_dirpath = Path(stored_job_data_dir)

        @property
        def files_dirpath(self): return self.stored_job_data_dirpath / self._FILES_DIRNAME
        @property
        def logs_dirpath(self): return self.stored_job_data_dirpath / self._LOGS_DIRNAME
        @property
        def files_filepath(self): return self.stored_job_data_dirpath / self._FILES_FILENAME
        @property
        def params_filepath(self): return self.stored_job_data_dirpath / self._PARAMS_FILENAME
        @property
        def stats_filepath(self): return self.stored_job_data_dirpath / self._STATS_FILENAME

    def _get_stored_job_data_registry(self, stored_job_data_dir: PathRepr):
        return self.StoredJobDataRegistry(stored_job_data_dir)

    def get_stored_job_data_registry(self, stage: str, job: str):
        return self._get_stored_job_data_registry(self.get_stored_job_dirpath(stage, job))

    def get_stored_job_data_registries(self):
        for stage in self.get_registered_stages():
            for child_path in self.get_stored_stage_dirpath(stage).iterdir():
                if child_path.is_dir():
                    yield self._get_stored_job_data_registry(child_path)


    class StoredDataCollector:
        def __init__(self, stored_data_registry: StoredDataRegistry):
            self.stored_data_registry = stored_data_registry
            self.params = {}
            self.files_info = {}

        def collect(self):
            for stored_job_data_registry in self.stored_data_registry.get_stored_job_data_registries():
                logger.debug(f"Collecting stored params from {stored_job_data_registry.stored_job_data_dirpath}")
                stored_job_params = _parse_yaml_if_file_exists(stored_job_data_registry.params_filepath)
                stored_job_files = _parse_yaml_if_file_exists(stored_job_data_registry.files_filepath)

                self.params = _merge_dicts_func(self.params, stored_job_params)

                stored_job_files_dir = str(stored_job_data_registry.files_dirpath)
                stored_job_files_info = { file_key: { 'basedir': stored_job_files_dir, 'path': file_path }
                                        for file_key, file_path in stored_job_files.items() }
                self.files_info = _merge_dicts_func(self.files_info, stored_job_files_info)
            return self

        def get_files_info(self):
            logger.debug(f"Collected stored files info:\n%s", UtilsYaml.write_yaml(self.files_info))
            return self.files_info

        def get_params(self):
            logger.debug(f"Collected stored params:\n%s", UtilsYaml.write_yaml(self.params))
            return self.params

        def copy_files(self, dst_dir: PathRepr, dst_file_paths: dict[str,str|None]=None) -> dict[str, str]:
            if dst_file_paths is None:
                dst_file_paths = dict.fromkeys(self.files_info.keys())  # copy all files, without renaming
            copied_files = {}
            for file_key, file_path in dst_file_paths.items():
                if file_path and len(file_path_and_content := file_path.split(':', 1)) == 2:  # for tests
                    file_content = file_path_and_content[1]
                    if file_content.startswith('\n'):
                        file_content = file_content[1:]
                    _write_to_file_and_log(file_content, Path(dst_dir, file_path_and_content[0]))
                    copied_files[file_key] = file_path_and_content[0]
                elif file_info := self.files_info.get(file_key):
                    real_dst_path = _copy_file(src_base_dir=file_info.get('basedir'), src_file=file_info.get('path'),
                                               dst_base_dir=dst_dir, dst_file=file_path, file_key=file_key)
                    copied_files[file_key] = real_dst_path
                else:
                    logger.warning(f"File key {file_key} is not found in stored files")
            return copied_files

    def get_stored_data_collector(self):
        return self.StoredDataCollector(self)


class JobDataRegistry:
    _PARAMS_TEMPLATE = {'kind': 'AtlasModuleParamsInsecure', 'apiVersion': 'v1',}
    _PARAMS_SECURE_TEMPLATE = {'kind': 'AtlasModuleParamsSecure', 'apiVersion': 'v1',}
    _CONTEXT_DESCRIPTOR_TEMPLATE = {'kind': 'AtlasModuleContextDescriptor', 'apiVersion': 'v1',}
    _DEFAULT_CONTEXT_PATHS = {
        'paths.input.params':         'input_params.yaml',
        'paths.input.params_secure':  'input_params_secure.yaml',
        'paths.input.files':          'input_files',
        'paths.output.params':        'output_params.yaml',
        'paths.output.params_secure': 'output_params_secure.yaml',
        'paths.output.files':         'output_files',
        # 'paths.logs':                 'logs',
        # 'paths.temp':                 'temp',
    }

    @staticmethod
    def _create_context_descriptor(context_paths_root: PathRepr|None=None) -> dict:
        context_descriptor_wrap = HierarchicalDict()
        for k, v in JobDataRegistry._DEFAULT_CONTEXT_PATHS.items():
            context_descriptor_wrap[k] = os.path.join(context_paths_root, v) if context_paths_root else v
        return context_descriptor_wrap.data

    def __init__(self, base: PathRepr, relative_to_context: bool=False):
        if os.path.isfile(base):  # `base` is an existing context file
            self.context_descriptor_filepath = Path(base)
            self.context_descriptor = UtilsYaml.read_yaml(self.context_descriptor_filepath)
        else:  # `base` is a directory, might not exist: applying default qubership_pipelines_modules_ops layout
            _ensure_dir(base)
            self.context_descriptor_filepath = Path(base, 'context.yaml')
            self.context_descriptor = JobDataRegistry._create_context_descriptor(None if relative_to_context else base)

        context_dirpath = self.context_descriptor_filepath.parent

        context_descriptor_wrap = HierarchicalDict.wrap(self.context_descriptor)
        def _path(param) -> Path:
            if param_value := context_descriptor_wrap.get(param):
                return Path(context_dirpath, param_value) if relative_to_context else Path(param_value)
            return None

        self.input_params_filepath          = _path('paths.input.params')
        self.input_params_secure_filepath   = _path('paths.input.params_secure')
        self.input_files_dirpath: Path      = _ensure_dir(_path('paths.input.files'))
        self.output_params_filepath         = _path('paths.output.params')
        self.output_params_secure_filepath  = _path('paths.output.params_secure')
        self.output_files_dirpath: Path     = _ensure_dir(_path('paths.output.files'))
        self.logs_dirpath                   = _path('path.logs') or (context_dirpath / 'logs')

    def write_context_descriptor(self):
        _write_to_file_and_log(
                _merge_dicts_func(JobDataRegistry._CONTEXT_DESCRIPTOR_TEMPLATE, self.context_descriptor),
                self.context_descriptor_filepath
        )

    @staticmethod
    def _write_params_to_file(params, file: PathRepr):
        _write_to_file_and_log(_merge_dicts_func(JobDataRegistry._PARAMS_TEMPLATE, params), file)

    def write_input_params(self, params):
        JobDataRegistry._write_params_to_file(params, self.input_params_filepath)

    def write_output_params(self, params):
        JobDataRegistry._write_params_to_file(params, self.output_params_filepath)

    @staticmethod
    def _write_params_secure_to_file(params_secure, file: PathRepr):
        _write_to_file_and_log(
                _merge_dicts_func(JobDataRegistry._PARAMS_SECURE_TEMPLATE, params_secure), file, _SKIP_LOG_CONTENT)

    def write_input_params_secure(self, params_secure):
        JobDataRegistry._write_params_secure_to_file(params_secure, self.input_params_secure_filepath)

    def write_output_params_secure(self, params_secure):
        JobDataRegistry._write_params_secure_to_file(params_secure, self.output_params_secure_filepath)

    @staticmethod
    def read_descriptor_from_file(file: PathRepr):
        descriptor = _parse_yaml_if_file_exists(file)
        for k in ('kind', 'apiVersion',):
            descriptor.pop(k, None)
        return descriptor

class JobVariablesCollector:
    _PREFIXED_VARS_PRIORITY = _QUBERSHIP_PIPELINES_MODULES_OPS_PREFIXED_VARS_PRIORITY == 'true'

    def __init__(self, *, declared_vars: dict = None, context_vars: dict = None):
        self.declared_vars = declared_vars if declared_vars is not None else os.environ
        self.context_vars = context_vars if context_vars is not None else {}
        self._string_substitution = StringSubstitution(ChainMap(self.context_vars, self.declared_vars))
                                                        # context vars have priority over declared vars
        self._vars_configs = []
        self._prefixed_vars_config = {}

    @staticmethod
    def _normalize_key(k: str|list[str]) -> list[str]:
        return [key_item_chunk
                    for key_item in ([k] if isinstance(k, str) else k)
                        for key_item_chunk in _split_var_name(key_item)]

    def add_source_var(self, var_name):
        logger.info(f"Collecting variable '{var_name}'")
        if var_value := self.declared_vars.get(var_name):
            # var_config = UtilsYaml.read_yaml(string=self._string_substitution.calculate_expression(var_value))
            var_config = UtilsYaml.read_yaml(string=var_value)  # do not substitute variables before parsing yaml,
                                                                # as multiline var substitution produced incorrect yaml
            var_config_calculated = {}
            for path, value in UtilsDictionary.traverse(var_config, traverse_nested_lists=True):
                value_calculated = self._string_substitution.calculate_expression(value)
                UtilsDictionary.setitem_by_path(var_config_calculated, path, value_calculated)
            self._vars_configs.append({var_name: var_config_calculated})
        return self

    def add_prefixed_source_vars(self, root_var: str, replace_root: str|list[str]=None):
        logger.info(f"Collecting variables with prefix '{root_var}'" + f" -> '{replace_root}'"*bool(replace_root))
        root_key_list = JobVariablesCollector._normalize_key(replace_root) if replace_root is not None else [root_var]
        _ACCEPTED_ENV_VAR_NAMES_PATTERN = re.compile(re.escape(root_var)+r'(?:\.|__)(.+)')
        for k, v in self.declared_vars.items():  # k:str
            if m := re.match(_ACCEPTED_ENV_VAR_NAMES_PATTERN, k):
                key_list = root_key_list + JobVariablesCollector._normalize_key(m[1])
                value = self._string_substitution.calculate_expression(v)
                UtilsDictionary.setitem_by_path(self._prefixed_vars_config, key_list, value)
        return self

    def result(self):
        # note: we cannot substitute variables in this method, as we do not traverse lists here
        if not self._vars_configs:
            _result = deepcopy(self._prefixed_vars_config)  # no need to flatten and reassemble the structure
        elif len(self._vars_configs) == 1 and not self._prefixed_vars_config:
            _result = deepcopy(self._vars_configs[0])  # no need to flatten and reassemble the structure
        else:
            # flatten and reassemble to correctly merge hierarchical structures, such as:
            # 1. input:
            #      systems:
            #        cmdb.url: some_url
            # 2. input__systems__cmdb__url: another_url
            _result = {}
            params_to_merge = ([*self._vars_configs, self._prefixed_vars_config]
                                if JobVariablesCollector._PREFIXED_VARS_PRIORITY
                                else [self._prefixed_vars_config, *self._vars_configs])
            for params in params_to_merge:
                for path, value in UtilsDictionary.traverse(params, traverse_nested_lists=False):
                    UtilsDictionary.setitem_by_path(_result, path, value)

        logger.debug(f"Collected parameters:\n%s", UtilsYaml.write_yaml(_result))
        return _result


def prepare_data(root_dir: PathRepr, stage: str):
    layout = Layout(root_dir)

    job_data_registry = JobDataRegistry(layout.job_data_dirpath)
    job_data_registry.write_context_descriptor()

    stored_data_registry = StoredDataRegistry(layout.stored_data_dirpath)
    stored_data_registry.register_current_stage(stage)

    stored_data_collector = stored_data_registry.get_stored_data_collector()
    stored_data_collector.collect()
    stored_data_params = stored_data_collector.get_params()

    job_vars_collector = JobVariablesCollector(declared_vars=os.environ, context_vars=stored_data_params)
    job_vars_collector.add_source_var('input')
    job_vars_collector.add_prefixed_source_vars('input')
    job_vars_collector.add_prefixed_source_vars('params', 'input.params.params')
    job_vars_collector.add_prefixed_source_vars('systems', 'input.params.systems')
    job_vars_collector.add_source_var('report')
    job_vars_collector.add_prefixed_source_vars('report')
    job_vars_collector.add_source_var('when')
    job_vars_collector.add_prefixed_source_vars('when')
    collected_vars = job_vars_collector.result()

    if condition := collected_vars.get('when', {}).get('condition'):
        logger.info(f"Evaluating condition: {condition}")
        result = eval(condition, {},  ChainMap(stored_data_params, os.environ))
        logger.info(f"Evaluation result: {result if isinstance(result, bool) else result+' -> '+bool(result)}")
        if not result:
            UtilsFile.write_file('', job_data_registry.logs_dirpath / '.when_condition_false')
            exit(int(_QUBERSHIP_PIPELINES_MODULES_OPS_FALSE_CONDITION_EXIT_CODE))

    input = collected_vars.get('input', {})
    job_data_registry.write_input_params(input.get('params', {}))
    job_data_registry.write_input_params_secure(input.get('params_secure', {}))
    stored_data_collector.copy_files(job_data_registry.input_files_dirpath, input.get('files', {}))

    if (report_cfg := collected_vars.get('report')) is not None:
        pipeline_report_builder = get_pipeline_report_operations().get_pipeline_report_builder(report_cfg)
        for stored_job_data_registry in stored_data_registry.get_stored_job_data_registries():
            pipeline_report_builder.add_job(
                    stats_file=stored_job_data_registry.stats_filepath,
                    module_report_file=stored_job_data_registry.logs_dirpath / 'execution_report.yaml',
            )
        _write_to_file_and_log(
                pipeline_report_builder.build(), job_data_registry.input_files_dirpath / 'execution_report.yaml')


OUTPUT_MAPPING_ENV_VAR_NAMES = ('BUILD_STATUS', 'BUILD_URL', 'BUILD_DATE',)
def store_data(root_dir: PathRepr, stage: str, job: str):
    layout = Layout(root_dir)
    job_data_registry = JobDataRegistry(layout.job_data_dirpath)
    stored_data_registry = StoredDataRegistry(layout.stored_data_dirpath)

    stored_job_data_registry = stored_data_registry.get_stored_job_data_registry(stage, job)
    stored_job_files_dirpath = stored_job_data_registry.files_dirpath

    output_cfg_collector = JobVariablesCollector(declared_vars=os.environ)
    output_cfg_collector.add_source_var('output')
    output_cfg_collector.add_prefixed_source_vars('output')
    output_cfg = output_cfg_collector.result().get('output', {})

    output_params = JobDataRegistry.read_descriptor_from_file(job_data_registry.output_params_filepath)
    output_params_wrap = HierarchicalDict.wrap(output_params)
    output_params_secure = JobDataRegistry.read_descriptor_from_file(job_data_registry.output_params_secure_filepath)
    output_params_secure_wrap = HierarchicalDict.wrap(output_params_secure)
    output_params_env = { var_name: os.getenv(var_name) for var_name in OUTPUT_MAPPING_ENV_VAR_NAMES }

    output_params_declared = ChainMap(output_params_wrap, output_params_secure_wrap)
    output_params_public = ChainMap(output_params_env, output_params_wrap)

    # collect data
    params = {}
    params_secure = {}
    for var_name, var_path in output_cfg.get('params', {}).items():
        if var_path == '*':
            if val_map := output_params_wrap.get(_split_var_name(var_name)):
                params.update(val_map)
            if val_map_secure := output_params_secure_wrap.get(_split_var_name(var_name)):
                params_secure.update(val_map_secure)
        elif isinstance(var_path, str):
            if (val := output_params_public.get(var_path)) is not None:
                params[var_name] = val
            if (val_secure := output_params_secure_wrap.get(var_path)) is not None:
                params_secure[var_name] = val_secure
        else:
            logger.error(f"Unsupported mapping for output params: {var_name} -> {var_path}")

    files = {}
    for file_key, file_path in output_cfg.get('files', {}).items():
        if file_path == '*':
            if val_map := output_params_declared.get(_split_var_name(file_key)):
                files.update(val_map)
                for k, p in val_map.items():
                    _copy_file(src_base_dir=job_data_registry.output_files_dirpath, src_file=p,
                               dst_base_dir=stored_job_files_dirpath, dst_file=p, file_key=k)
        elif isinstance(file_path, str):
            files[file_key] = file_path
            _copy_file(src_base_dir=job_data_registry.output_files_dirpath, src_file=file_path,
                       dst_base_dir=stored_job_files_dirpath, dst_file=file_path, file_key=file_key)
        else:
            logger.error(f"Unsupported mapping for output files: {file_key} -> {file_path}")

    # store data
    if params or params_secure:
        params_all = _merge_dicts_func(params, params_secure)
        log_params_all = _merge_dicts_func(params, {k: '[MASKED]' for k in params_secure})
        _write_to_file_and_log(params_all, stored_job_data_registry.params_filepath, log_params_all)
    if files:
        _write_to_file_and_log(files, stored_job_data_registry.files_filepath)
    if job_data_registry.logs_dirpath.is_dir():
        shutil.copytree(job_data_registry.logs_dirpath, stored_job_data_registry.logs_dirpath, dirs_exist_ok=True)

    # store pipeline output
    if output_cfg.get('pipeline_output'):
        pipeline_output_registry = JobDataRegistry(layout.pipeline_output_dirpath, relative_to_context=True)
        pipeline_output_registry.write_output_params(output_params)
        pipeline_output_registry.write_output_params_secure(output_params_secure)
        if stored_job_data_registry.files_dirpath.is_dir():
            shutil.copytree(stored_job_data_registry.files_dirpath,
                            pipeline_output_registry.output_files_dirpath,
                            dirs_exist_ok=True)
        pipeline_output_registry.write_context_descriptor()

    # store execution statistics
    _write_to_file_and_log(
            get_pipeline_report_operations().get_job_stats(job_data_registry),
            stored_job_data_registry.stats_filepath
    )
