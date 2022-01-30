# repobee-sorald
Plugin for executing Sorald on Java source files

## Setup

### Prerequisites

Editable build of [`repobee`](https://github.com/repobee/repobee).

> I have not tested this script with the pip package of repobee.

### Steps

1. Clone this repository anywhere on your system.
2. Change directory to `repobee` and install `repobee-sorald` by running:
    ```shell
    $ pip install /path/to/repobee-sorald 
    ```
3. Run `repobee-sorald` as a command extension of clone command. Example,
    ```shell
    $ python repobee.py -p sorald repos clone \
      --students-file students_file.txt \
      -a task-14 \
      -sj ~/sorald/target/sorald-0.3.1-SNAPSHOT-jar-with-dependencies.jar
    ```
   The extension, as of now, takes only two arguments:
   1. `--sorald-jar/-sj`: path to Sorald Jar.
   2. `--directory/-d` (optional): directory where all stats file are
      collected.
   > NOTE: Be careful about running the clone command. It will clone student
   > repositories in the current working directory!

The console output shows the Sonar rule key and the frequency of violations.
Currently, the script reports violations of the
[handled rules](https://github.com/SpoonLabs/sorald/blob/master/docs/HANDLED_RULES.md)
to make the analysis easier. It can, of course, be tweaked to incorporate all
Sonar rules. Anyway, JSON files inside stats directory, passed using
`--directory/-d`, have reported violations of all Sonar rules.

# License
See [LICENSE](LICENSE) for details.
