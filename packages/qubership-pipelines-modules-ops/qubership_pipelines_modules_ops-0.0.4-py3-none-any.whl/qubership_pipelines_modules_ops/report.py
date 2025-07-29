import os
import logging

from datetime import datetime, timezone
from .utils.utils_file import UtilsYaml
from .utils.utils_github import UtilsGithub

logger = logging.getLogger(__name__)


class PipelineReportBuilder:
    def __init__(self, report_cfg):
        self.report_cfg = report_cfg
        # self.version = report_cfg.get('version', 'v1')

    def add_job(self, *, stats_file, module_report_file):
        raise NotImplementedError()

    def build(self):
        raise NotImplementedError()

    @staticmethod
    def _parse_datetime(dt):
        try:
            return datetime.fromisoformat(dt)
        except (TypeError, ValueError):
            logger.error('Incorrect date/time format: %s', dt)
            return None

    @staticmethod
    def _parse_src_file(src):
        return UtilsYaml.read_yaml(src) if src and os.path.isfile(src) else None


class PipelineReportOperations:
    def get_pipeline_report_builder(self, report_cfg):
        return PipelineReportBuilder(report_cfg)

    def get_job_stats(self, job_data_registry):
        raise NotImplementedError()


class GitLabPipelineReportOperations(PipelineReportOperations):
    GITLAB_STATUS_FAILED = 'failed'
    GITLAB_STATUS_SKIPPED = 'skipped'
    GITLAB_STATUS_SUCCESS = 'success'

    class GitLabPipelineReportBuilder(PipelineReportBuilder):
        SUCCESS_ERROR_CODE = 'DEVOPS-GITLAB-EXEC-0000'
        FAILED_ERROR_CODE = 'DEVOPS-GITLAB-EXEC-1500'

        def __init__(self, report_cfg):
            super().__init__(report_cfg)
            self.current_datetime = datetime.now(timezone.utc).replace(microsecond=0)
            self._job_reports = []

        def add_job(self, *, stats_file, module_report_file):
            if stats := self._parse_src_file(stats_file):
                job_started_at = stats.get('CI_JOB_STARTED_AT')
                job_finished_at = stats.get('_CI_JOB_FINISHED_AT')
                job_duration = None
                if ( (job_finished_at_dt := self._parse_datetime(job_finished_at))
                        and (job_started_at_dt := self._parse_datetime(job_started_at)) ):
                    job_duration = str(job_finished_at_dt - job_started_at_dt)
                job_report = {
                    'kind': 'AtlasStageReport',
                    'apiVersion': 'v1',
                    'execution': {
                        'name': stats.get('CI_JOB_NAME'),
                        'result': stats.get('CI_JOB_STATUS'),
                        'startedAt': job_started_at,
                        'time': job_duration,
                        'url': stats.get('CI_JOB_URL'),
                        'id': stats.get('CI_JOB_ID'),
                    }
                }
                if module_report := self._parse_src_file(module_report_file):
                    job_report['moduleReport'] = module_report
                self._job_reports.append(job_report)
            return self

        def build(self):
            job_reports = sorted(self._job_reports, key=lambda el: el.get('execution', {}).get('startedAt'))

            pipeline_started_at = job_reports[0].get('execution', {}).get('startedAt', '') if job_reports else None
            pipeline_duration = None
            if pipeline_started_at_dt := self._parse_datetime(pipeline_started_at):
                pipeline_duration = str(self.current_datetime - pipeline_started_at_dt)

            ok_statuses = (
                    GitLabPipelineReportOperations.GITLAB_STATUS_SUCCESS,
                    GitLabPipelineReportOperations.GITLAB_STATUS_SKIPPED,
            )
            if any(jr.get('execution', {}).get('result') not in ok_statuses for jr in job_reports):
                pipeline_status = GitLabPipelineReportOperations.GITLAB_STATUS_FAILED
                pipeline_error_code = self.FAILED_ERROR_CODE
            else:
                pipeline_status = GitLabPipelineReportOperations.GITLAB_STATUS_SUCCESS
                pipeline_error_code = self.SUCCESS_ERROR_CODE

            return {
                    'kind': 'AtlasPipelineReport',
                    'apiVersion': 'v1',
                    'execution': {
                        'result': pipeline_status,
                        'code': pipeline_error_code,
                        'startedAt': pipeline_started_at,
                        'time': pipeline_duration,
                        'user': os.getenv('GITLAB_USER_NAME'),
                        'email': os.getenv('GITLAB_USER_EMAIL'),
                        'url': os.getenv('CI_PIPELINE_URL'),
                    },
                    'config': self.report_cfg.get('config', []),
                    'stages': job_reports,
            }

    def get_pipeline_report_builder(self, report_cfg):
        return self.GitLabPipelineReportBuilder(report_cfg)

    def get_job_stats(self, job_data_registry):
        current_datetime = datetime.now(timezone.utc).replace(microsecond=0)
        stats = { k: v for k, v in os.environ.items() if k.startswith('CI_JOB_') }
        stats['_CI_JOB_FINISHED_AT'] = current_datetime.isoformat().replace("+00:00", "Z")  # non-standard field
        if (job_data_registry.logs_dirpath / '.when_condition_false').is_file():
            # change CI_JOB_STATUS based on when.condition evaluation
            stats['CI_JOB_STATUS'] = GitLabPipelineReportOperations.GITLAB_STATUS_SKIPPED
        return stats


class GitHubPipelineReportOperations(PipelineReportOperations):

    class GitHubPipelineReportBuilder(PipelineReportBuilder):
        CONCLUSION_SUCCESS = 'success'
        CONCLUSION_FAILURE = 'failure'
        CONCLUSION_SKIPPED = 'skipped'
        SUCCESS_ERROR_CODE = 'DEVOPS-GITHUB-EXEC-0000'
        FAILED_ERROR_CODE = 'DEVOPS-GITHUB-EXEC-1500'

        def __init__(self, report_cfg):
            super().__init__(report_cfg)
            self.current_datetime = datetime.now(timezone.utc).replace(microsecond=0)
            self._job_reports = []

        def add_job(self, *, stats_file, module_report_file):
            if stats := self._parse_src_file(stats_file):
                job_id = stats.get('JOB_ID')
                job_data = UtilsGithub.get_job_data(job_id)
                job_duration = None
                if ((job_completed_at_dt := self._parse_datetime(job_data.get('completed_at')))
                        and (job_started_at_dt := self._parse_datetime(job_data.get('started_at')))):
                    job_duration = str(job_completed_at_dt - job_started_at_dt)
                job_report = {
                    'kind': 'AtlasStageReport',
                    'apiVersion': 'v1',
                    'execution': {
                        'name': job_data.get('name'),
                        'result': self.CONCLUSION_SKIPPED if stats.get('IS_JOB_SKIPPED') else job_data.get('conclusion'),
                        'startedAt': job_data.get('started_at'),
                        'time': job_duration,
                        'url': job_data.get('html_url'),
                        'id': job_id,
                    }
                }
                if module_report := self._parse_src_file(module_report_file):
                    job_report['moduleReport'] = module_report
                self._job_reports.append(job_report)
            return self

        def build(self):
            run_data = UtilsGithub.get_run_data()
            job_reports = sorted(self._job_reports, key=lambda el: el.get('execution', {}).get('startedAt'))

            pipeline_started_at = job_reports[0].get('execution', {}).get('startedAt', '') if job_reports else None
            pipeline_duration = None
            if pipeline_started_at_dt := self._parse_datetime(pipeline_started_at):
                pipeline_duration = str(self.current_datetime - pipeline_started_at_dt)

            ok_statuses = (
                    self.CONCLUSION_SUCCESS,
                    self.CONCLUSION_SKIPPED,
            )
            if any(jr.get('execution', {}).get('result') not in ok_statuses for jr in job_reports):
                pipeline_status = self.CONCLUSION_FAILURE
                pipeline_error_code = self.FAILED_ERROR_CODE
            else:
                pipeline_status = self.CONCLUSION_SUCCESS
                pipeline_error_code = self.SUCCESS_ERROR_CODE

            return {
                    'kind': 'AtlasPipelineReport',
                    'apiVersion': 'v1',
                    'execution': {
                        'result': pipeline_status,
                        'code': pipeline_error_code,
                        'startedAt': pipeline_started_at,
                        'time': pipeline_duration,
                        'user': run_data.get('actor', {}).get('login'),
                        'email': None, # N/A for GH
                        'url': run_data.get('html_url'),
                    },
                    'config': self.report_cfg.get('config', []),
                    'stages': job_reports,
            }

    def get_pipeline_report_builder(self, report_cfg):
        return self.GitHubPipelineReportBuilder(report_cfg)

    def get_job_stats(self, job_data_registry):
        stats = {}
        jobs = UtilsGithub.get_all_jobs_data()
        current_job = [job for job in jobs["jobs"] if job["name"] == os.getenv('CURRENT_JOB_NAME')]
        if not current_job:
            raise Exception(f"Could not find current job data in GitHub response!")
        stats['JOB_ID'] = current_job[0]['id']
        stats['IS_JOB_SKIPPED'] = (job_data_registry.logs_dirpath / '.when_condition_false').is_file()
        return stats


def get_pipeline_report_operations():
    if os.getenv('GITLAB_CI') == 'true':
        return GitLabPipelineReportOperations()
    if os.getenv('GITHUB_ACTIONS') == 'true':
        return GitHubPipelineReportOperations()
    raise PipelineReportOperations()
