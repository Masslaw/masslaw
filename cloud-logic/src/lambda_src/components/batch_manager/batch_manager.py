import secrets
import time
import boto3
from botocore.config import Config

batch = boto3.client('batch', region_name = 'us-east-1',config=Config(signature_version='s3v4'))


class BatchJob:
    name = ''
    queue = ''
    definition = ''
    env_variables = ''
    share_identifier = ''


class BatchManager:

    @staticmethod
    def submit_job(job: BatchJob, depends_on: list = None):
        response = batch.submit_job(
            jobName=f'{job.name}_{secrets.token_hex(8).lower()}_{str(int(time.time()))}',
            jobQueue=job.queue,
            jobDefinition=job.definition,
            # shareIdentifier=job.share_identifier, TODO: we might want to make this dynamic. as of now, where no job with a share identifier is submitted, this will stay commented for simplicity
            containerOverrides={
                'environment': job.env_variables or []
            },
            dependsOn=depends_on or []
        )
        return response['jobId']

    @staticmethod
    def describe_jobs(job_ids):
        response = batch.describe_jobs(jobs=job_ids)
        return response['jobs']

    @staticmethod
    def list_jobs(job_queue=None, job_status=None):
        filters = []
        if job_queue is not None:
            filters.append({'name': 'job-queue', 'values': [job_queue]})
        if job_status is not None:
            filters.append({'name': 'status', 'values': [job_status]})
        response = batch.list_jobs(jobQueue=job_queue, jobStatus=job_status, filters=filters)
        return response['jobSummaryList']

    @staticmethod
    def cancel_job(job_id, reason=None):
        batch.cancel_job(jobId=job_id, reason=reason)

    @staticmethod
    def terminate_job(job_id, reason=None):
        batch.terminate_job(jobId=job_id, reason=reason)

    @staticmethod
    def submit_job_pipeline(jobs: list):
        job_ids = []
        for i, job in enumerate(jobs):
            if i == 0:
                job_id = BatchManager.submit_job(job)
            else:
                prev_job_id = job_ids[i - 1]
                depends_on = [{'jobId': prev_job_id}]
                job_id = BatchManager.submit_job(job, depends_on)
            job_ids.append(job_id)
        return job_ids
