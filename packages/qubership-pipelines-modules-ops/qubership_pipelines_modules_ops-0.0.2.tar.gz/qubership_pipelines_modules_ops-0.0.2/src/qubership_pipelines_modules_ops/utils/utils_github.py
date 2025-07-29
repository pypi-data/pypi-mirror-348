import os
import json

from urllib.request import urlopen, Request


class UtilsGithub:
    @staticmethod
    def get_api_data(url):
        httprequest = Request(url, headers={"Authorization": f"Bearer {os.getenv('GH_TOKEN')}"})
        with urlopen(httprequest) as response:
            return json.loads(response.read().decode())

    @staticmethod
    def get_run_data():
        url = f"{os.getenv('GITHUB_API_URL')}/repos/{os.getenv('GITHUB_REPOSITORY')}/actions/runs/{os.getenv('GITHUB_RUN_ID')}"
        return UtilsGithub.get_api_data(url)

    @staticmethod
    def get_all_jobs_data():
        # todo: pagination in >100 jobs case?
        url = f"{os.getenv('GITHUB_API_URL')}/repos/{os.getenv('GITHUB_REPOSITORY')}/actions/runs/{os.getenv('GITHUB_RUN_ID')}/jobs"
        return UtilsGithub.get_api_data(url)

    @staticmethod
    def get_job_data(job_id):
        url = f"{os.getenv('GITHUB_API_URL')}/repos/{os.getenv('GITHUB_REPOSITORY')}/actions/jobs/{job_id}"
        return UtilsGithub.get_api_data(url)
