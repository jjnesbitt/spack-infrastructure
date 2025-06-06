import json

import djclick as click
from django.db import connections
from tqdm import tqdm

from analytics.core.models.facts import JobFact

CHUNK_SIZE = 5000


@click.command()
def migrate_gitlab_section_timers():
    with connections["backup"].cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM core_jobdatadimension WHERE gitlab_section_timers != '{}'
        """)
        total = cursor.fetchall()[0][0]

        after = 0
        with tqdm(total=total) as pbar:
            while True:
                cursor.execute(
                    """
                    SELECT
                        job_id,
                        gitlab_section_timers
                    FROM
                        core_jobdatadimension
                    WHERE
                            gitlab_section_timers != '{}'
                        AND job_id > %(after)s
                    ORDER BY
                        job_id
                    LIMIT %(chunk_size)s;
                """,
                    {
                        "after": after,
                        "chunk_size": CHUNK_SIZE,
                    },
                )

                records = [
                    (id, json.loads(jsonstr)) for id, jsonstr in cursor.fetchall()
                ]
                if not records:
                    break

                # Set new after value
                after = records[-1][0]

                job_ids = [job_id for job_id, _ in records]
                job_facts = list(
                    JobFact.objects.filter(job_id__in=job_ids).order_by("job_id")
                )
                assert len(job_ids) == len(job_facts)

                for i, fact in enumerate(job_facts):
                    _, jsondata = records[i]
                    fact.gitlab_clear_worktree = jsondata.get("clear_worktree", 0)
                    fact.gitlab_after_script = jsondata.get("after_script", 0)
                    fact.gitlab_cleanup_file_variables = jsondata.get(
                        "cleanup_file_variables", 0
                    )
                    fact.gitlab_clear_worktree = jsondata.get('clear_worktree', 0)
                    fact.gitlab_download_artifacts = jsondata.get(
                        "download_artifacts", 0
                    )
                    fact.gitlab_get_sources = jsondata.get("get_sources", 0)
                    fact.gitlab_prepare_executor = jsondata.get("prepare_executor", 0)
                    fact.gitlab_prepare_script = jsondata.get("prepare_script", 0)
                    fact.gitlab_resolve_secrets = jsondata.get("resolve_secrets", 0)
                    fact.gitlab_step_script = jsondata.get("step_script", 0)
                    fact.gitlab_upload_artifacts_on_failure = jsondata.get(
                        "upload_artifacts_on_failure", 0
                    )
                    fact.gitlab_upload_artifacts_on_success = jsondata.get(
                        "upload_artifacts_on_success", 0
                    )

                    fact.save()
                    pbar.update(1)
