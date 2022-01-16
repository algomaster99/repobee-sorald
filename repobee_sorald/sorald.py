"""Plugin that runs Sorald"""
import os
import pathlib
import subprocess
import sys

import repobee_plug as plug

PLUGIN_NAME = "sorald"
PLUGIN_DESCRIPTION = "Runs Sorald and generates a report of Sonar Java violations"


class SoraldHooks(plug.Plugin, plug.cli.CommandExtension):
    __settings__ = plug.cli.command_extension_settings(
        actions=[plug.cli.CoreCommand.repos.clone]
    )

    sorald_jar_path = plug.cli.option(
        short_name="-sj",
        long_name="--sorald-jar",
        help="absolute path to Sorald jar",
        required=True,
        converter=pathlib.Path,
    )

    sorald_stats_file_directory = plug.cli.option(
        short_name="-d",
        long_name="--directory",
        help="directory where all stats file would be saved",
        default=f"{os.path.abspath(os.getcwd())}/stats",
    )

    def post_clone(self, repo: plug.StudentRepo, api: plug.PlatformAPI):
        """
        Mine Sonar Java violations.
        """

        if not SoraldHooks._has_student_committed(repo):
            message = "Student has done not the assignment. Skipping ..."
            return plug.Result(PLUGIN_NAME, plug.Status.WARNING, message)
        command = (
            f"java -jar {self.sorald_jar_path} mine "
            f"--source {repo.path} "
            f"--stats-output-file={self.sorald_stats_file_directory}/{repo.name}.json"
        )
        process = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        if process.returncode != 0:
            message = process.stderr.decode(sys.getdefaultencoding())
            status = plug.Status.ERROR
        else:
            message = f"Violations mined for {repo.name}."
            status = plug.Status.SUCCESS
        return plug.Result(PLUGIN_NAME, status, message)

    @staticmethod
    def _has_student_committed(repo: plug.StudentRepo) -> bool:
        repo_name = repo.name
        student_username = repo_name.split("-")[0]
        command = f"git log --author={student_username}"

        process = subprocess.run(
            command,
            cwd=repo.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        if process.returncode == 0:
            return len(process.stdout) > 0
        else:
            raise plug.UnexpectedException(
                process.stderr.decode(sys.getdefaultencoding())
            )
