# dxlog - a DNAnexus log reader

[![PyPI - Version](https://img.shields.io/pypi/v/dxlog.svg)](https://pypi.org/project/dxlog)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/dxlog/0.0.1)](https://pypi.org/project/dxlog/)

This app allows for the displaying of latest DNAnexus jobs in a convenient UI.

![Job page preview](https://github.com/gloriabenoit/dxlog/blob/main/data/job_page.png?raw=true)

## Installation

To install the package, you can run the following command.

```console
pip install dxlog
```

However, please be aware, you need to enter your DNAnexus credentials before using the app (in order to access to your projects remotely).

```console
dx login
```

> By default, your information expires in 30 days, but this can be changed using the `--timeout` option.

## Usage (from command line)

The most basic way to use the app is the following:

```bash
dxlog
```

However, the app has 4 options:

* `-p [str]` specifies the project for which you wish to say the jobs (default Current)
* `-u [str]` specifies the user of which you wish to see the jobs (default All)
* `-n [int]` specifies the number of jobs to display when you first open the app (default 100)
* `-s [int]` specifies the incrementation of the number of jobs displayed (default 100)

Opening *dxlog* will display the last 100 jobs run on the current project by default.
Clicking on a job will open a new page displaying the log of the job chosen.

![Log page preview](https://github.com/gloriabenoit/dxlog/blob/main/data/log_page.png?raw=true)

## Features

### On the job page

* Update the job list
* Show only `done`, `running` or `failed` jobs
* Show more or less jobs
* Search for string in job name, user name or date

### On the log page

* Update the log
* Download the output (if it exists)
* Open the job's monitor page (or display link if not possible)

## License

`dxlog` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
