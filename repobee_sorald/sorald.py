"""Plugin that runs Sorald"""
import json
import os
import pathlib
import subprocess
import sys

import repobee_plug as plug

PLUGIN_NAME = "sorald"
PLUGIN_DESCRIPTION = "Runs Sorald and generates a report of Sonar Java violations"

HANDLED_RULES = [
    "S1068",
    "S1118",
    "S1132",
    "S1155",
    "S1217",
    "S1444",
    "S1481",
    "S1596",
    "S1656",
    "S1854",
    "S1860",
    "S1948",
    "S2057",
    "S2095",
    "S2097",
    "S2111",
    "S2116",
    "S2142",
    "S2164",
    "S2167",
    "S2184",
    "S2204",
    "S2225",
    "S2272",
    "S2755",
    "S3032",
    "S3067",
    "S3984",
    "S4973",
]


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

        os.makedirs(self.sorald_stats_file_directory, exist_ok=True)

        path_to_stats_file = f"{self.sorald_stats_file_directory}/{repo.name}.json"
        command = (
            f"java -jar {self.sorald_jar_path} mine "
            f"--source {repo.path} "
            f"--stats-output-file={path_to_stats_file}"
        )
        process = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )

        if process.returncode != 0:
            message = process.stderr.decode(sys.getdefaultencoding())
            status = plug.Status.ERROR
            return plug.Result(PLUGIN_NAME, status, message)

        number_of_violations = SoraldHooks._parse_stats_file(path_to_stats_file)
        status = plug.Status.SUCCESS
        return plug.Result(PLUGIN_NAME, status, number_of_violations)

    @staticmethod
    def _parse_stats_file(path_to_stats_file: str):
        with open(path_to_stats_file) as stats_file:
            json_object = json.loads(stats_file.read())

            mined_rules = json_object["minedRules"]
            number_of_violation = {}
            for violation in mined_rules:
                number_of_violation[violation["ruleKey"]] = len(violation["warningLocations"])
            return number_of_violation

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
