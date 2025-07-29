"""An app to read the logs of DNAnexus jobs.

Author: Gloria Benoit
Version: 0.1.0
Date: 16/05/25
"""

import argparse
import asyncio
import datetime
import re
import sys

from subprocess import Popen, PIPE

import dxpy

from textual import on
from textual.app import App
from textual.binding import Binding
from textual.containers import Center, HorizontalGroup, VerticalGroup
from textual.reactive import reactive
from textual.widgets import Button, Footer, Input, Link, Log, ProgressBar, Static

class SearchBar(Input):
    """A search bar."""
    BINDINGS = [
        Binding("escape", "blur"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.can_focus = False

    def action_blur(self) -> None:
        """Unfocus search bar."""
        # Focus on first job available
        jobs = self.parent.query(Job)
        for job in jobs:
            if job.focusable:
                job.focus()
                break

    def action_submit(self):
        """When a search is submitted."""
        self.action_blur()

        # Search for matches
        job_page = self.parent.query_one(JobPage)
        job_page.search = str(self.value)
        job_page.show_all_jobs()

class Job(Button):
    """A job."""

    def __init__(self,
                 jid: str,
                 jobname: str,
                 outputs: list,
                 runtime: str,
                 state: str,
                 user: str,
                 date: str,
                 **kwargs):
        self.jid = jid
        self.jobname = jobname
        self.outputs = outputs
        self.runtime = runtime
        self.state = state
        self.user = user
        self.date = date
        label = f"{jobname:^30s} | {date} | {runtime:^8} | {state:^10s} | {user:^15s}"
        super().__init__(label, **kwargs)

class JobPage(Static):
    """The page with all jobs."""

    n_jobs_shown = reactive(0)
    n_jobs_total = reactive(0)
    n_jobs_max = 0

    show_done = False
    show_running = False
    show_failed = False

    search = reactive("")

    @on(Button.Pressed, "#more")
    def add_jobs(self):
        """Increase the number of jobs displayed."""
        if self.n_jobs_shown + self.step > self.n_jobs_total:
            self.n_jobs_total *= 2
        self.n_jobs_shown += self.step

        # Update utilities
        self.check_utilities()

    @on(Button.Pressed, "#less")
    def remove_jobs(self):
        """Decrease the number of jobs displayed."""
        if self.n_jobs_shown > self.step:
            if (self.n_jobs_max != 0) and (self.n_jobs_max < self.n_jobs_shown):
                self.n_jobs_shown = self.n_jobs_max - self.step
            else:
                self.n_jobs_shown -= self.step

        # Update utilities
        self.check_utilities()

    def __init__(self, *args, project: str, user: str, n_lines: int, step: int, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project
        self.user = user
        self.n_lines = n_lines
        self.step = step

    def compose(self):
        """Composition of the job page."""
        yield VerticalGroup(id="job_view")
        with HorizontalGroup(classes="change_line"):
            yield Button("More", id="more")
            yield Button("Less", id="less")

    def on_mount(self):
        """First read of jobs."""
        self.n_jobs_total = self.n_lines
        self.n_jobs_shown = self.n_lines
        self.check_utilities()

    def read_job_log(self):
        """Create jobs from job log."""
        # Remove existing jobs
        jobs = self.query(Job)
        if jobs: # If there's anything
            jobs.remove()

        # Get latest jobs
        command = ["dx", "find", "jobs", "-n", f"{self.n_jobs_total}", "--show-outputs"]
        if self.project:
            command += ["--project", f"{self.project}"]
        if self.user:
            command += ["--user", f"{self.user}"]
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        output, _ = process.communicate()

        if output:
            job_view = self.query_one("#job_view")

            job_list = output.decode('utf-8').split("* ")[1:]
            if (job_list[-1]).startswith("More"):
                job_list = job_list[:-1]

            # For every job found
            for job in job_list:
                sep = job.split()
                cached = False

                # Get positions
                parenthesis_info = [sep.index(info) for info in sep if info.startswith('(')]
                exec_id = parenthesis_info[0]

                # Get info
                jobname = " ".join(sep[:exec_id])
                # If the job is cached
                if jobname.startswith('['):
                    jobname = jobname.strip('[]')
                    cached = True
                state = sep[parenthesis_info[1]].strip("()")
                jid = sep[parenthesis_info[1] + 1]
                user = sep[parenthesis_info[1] + 2]
                date = sep[parenthesis_info[1] + 3]
                date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%y')
                runtime = "-"
                outputs = ""

                if state == "done":
                    runtime = sep[parenthesis_info[2] + 1].strip("()")
                    if cached:
                        runtime = sep[parenthesis_info[2] + 2].strip("()")
                    if sep[sep.index('Output:')+1] != '-':
                        output_start = sep.index('[')
                        output_end = sep.index(']')
                        for i in range(output_start + 1, output_end):
                            outputs += sep[i]
                        outputs = outputs.split(',')

                if state == "running":
                    runtime = sep[parenthesis_info[2] + 2].strip("()")

                # Color and activity
                disabled = False
                button_variant = "default"
                if state == "done":
                    button_variant = "success"
                elif state == "failed":
                    button_variant = "error"
                elif state == "running":
                    button_variant = "primary"
                elif state == "runnable":
                    disabled = True

                # Add the job
                job_button = Job(jid=jid,
                                 jobname=jobname,
                                 outputs=outputs,
                                 runtime=runtime,
                                 state=state,
                                 user=user,
                                 date=date,
                                 disabled=disabled,
                                 variant=button_variant,
                                 classes="hidden")
                job_view.mount(job_button)

            # If the max number of jobs is reached
            if len(job_list) < self.n_jobs_total:
                self.n_jobs_max = len(job_list)
        else:
            sys.exit("ERROR: Invalid user.\nPlease enter a valid user name.")

    def show_jobs(self):
        """View jobs."""
        jobs = self.query(Job)
        if self.n_jobs_max != 0:
            max_value = min(self.n_jobs_total, self.n_jobs_max)
        else:
            max_value = self.n_jobs_total

        gap = len(jobs) - max_value
        for i, job in enumerate(jobs):
            if i < self.n_jobs_shown + gap:
                if self.show_done is True:
                    if job.state == "done":
                        job.remove_class("hidden")
                elif self.show_running is True:
                    if job.state == "running":
                        job.remove_class("hidden")
                elif self.show_failed is True:
                    if job.state == "failed":
                        job.remove_class("hidden")
                else:
                    job.remove_class("hidden")
            else:
                job.add_class("hidden")

            if self.search:
                if not "hidden" in job.classes:
                    if not (re.search(self.search.lower(), job.jobname.lower()) or
                        re.search(self.search.lower(), job.user.lower()) or
                        re.search(self.search.lower(), job.date.lower())):
                        job.add_class("hidden")

    def check_utilities(self):
        """Check if utilities need to be disabled."""
        # More jobs
        button_more = self.query_one("#more")
        if (self.n_jobs_max != 0) and (self.n_jobs_max < self.n_jobs_shown):
            button_more.disabled = True
        else:
            button_more.disabled = False

        # Less jobs
        button_less = self.query_one("#less")
        if self.n_jobs_shown <= self.step:
            button_less.disabled = True
        else:
            button_less.disabled = False

    def hide_all_jobs(self):
        """Hide all jobs shown."""
        jobs = self.query(Job)
        for job in jobs:
            job.add_class("hidden")

    def show_all_jobs(self):
        """Show all jobs."""
        self.show_done = False
        self.show_running = False
        self.show_failed = False
        self.show_jobs()

    def watch_n_jobs_total(self):
        """When n_jobs_total changes."""
        self.read_job_log()

    def watch_n_jobs_shown(self):
        """When n_jobs_shown changes."""
        self.show_jobs()

    def watch_search(self):
        """When you search something."""
        self.show_jobs()

class LogDNAnexus(Log):
    """A DNAnexus log."""

    def __init__(self,
                 jid: str,
                 **kwargs):
        self.jid = jid
        super().__init__(**kwargs)

    def on_mount(self):
        """Get log."""
        self.get_current()

    def get_current(self):
        """Read current log."""
        command = ["dx", "watch", f"{self.jid}", "--no-wait"]
        process = Popen(command, stdout=PIPE, stderr=PIPE, bufsize=1, text=True)
        output, _ = process.communicate()
        self.write_line(output)

class LogPage(Static):
    """The page with the log."""

    jid = reactive("")

    @on(Button.Pressed, "#download")
    async def download_output(self):
        """Download the job output."""
        progress_bar = self.query_one(ProgressBar)
        progress_bar.update(total=len(self.outputs),
                            progress=0)
        progress_bar.remove_class("hidden")

        for output in self.outputs:
            command = ["dx", "download", f"{output}", "--overwrite"]
            process = Popen(command, stdout=PIPE, stderr=PIPE)
            await asyncio.to_thread(process.communicate)
            progress_bar.advance(1)

    @on(Button.Pressed, "#page")
    def open_page(self):
        """Open the monitor page of the job."""
        page_link = self.query_one(Link)
        page = page_link.url
        openned = self.parent.parent.parent.open_url(page, new_tab=True)

        # If you cannot open the page
        if not openned:
            page_link.remove_class("hidden")

    def watch_jid(self):
        """Update page."""
        job_id = self.jid.split('-')[-1]
        project_id = dxpy.PROJECT_CONTEXT_ID.split('-')[-1]
        page = f"https://ukbiobank.dnanexus.com/panx/projects/{project_id}/monitor/job/{job_id}"

        self.query_one(Link).url = page
        self.query_one(Link).text = page

    def compose(self):
        """Log page components."""
        with Center():
            yield Link("placeholder",
                       id="page_link",
                       classes="hidden")
        with Center():
            yield ProgressBar(total=10,
                              show_percentage=True,
                              show_eta=False,
                              classes="hidden")
        with HorizontalGroup(id="log_buttons"):
            yield Button("Download output", id="download")
            yield Button("Open page", id="page")

class Joblog(App):
    """A log reader for DNAnexus."""

    # Hide palette keybind
    ENABLE_COMMAND_PALETTE = False

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("u", "update", "Update"),
        ("h", "home", "Home"),
        ("a", "show_all", "All"),
        ("d", "show_done", "Done"),
        ("r", "show_running", "Running"),
        ("f", "show_failed", "Failed"),
        ("m", "add_jobs", "More"),
        ("l", "remove_jobs", "Less"),
        ("s", "search_jobs", "Search"),
        ]

    CSS_PATH = "log_reader.css"

    @on(Button.Pressed, "Job")
    def see_log(self, press):
        """Switch to the log page."""
        # Remove search bar
        search_bar = self.query_one(SearchBar)
        search_bar.add_class("hidden")

        # Hide other pages
        job_container = self.query_one("#job_container")
        job_container.add_class("hidden")
        log_container = self.query_one("#log_container").remove_class("hidden")
        log_page = log_container.query_one(LogPage)
        log_page.jid = press.button.jid
        log_page.outputs = press.button.outputs
        log_page.state = press.button.state

        # Hide download button if necessary
        log_page.outputs = press.button.outputs
        download_button = log_page.query_one("#download")
        page_button = log_page.query_one("#page")
        if log_page.outputs:
            download_button.remove_class("hidden")
            page_button.remove_class("page-full-width")
        else:
            download_button.add_class("hidden")
            page_button.add_class("page-full-width")

        # Show job log
        jid = press.button.jid
        log = LogDNAnexus(jid=jid)
        log_page.mount(log)

    def __init__(self, *args, project: str, user: str, n_lines: int, step: int, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project
        self.user = user
        self.n_lines = n_lines
        self.step = step

    def compose(self):
        """Create child widgets for the app."""
        yield SearchBar(placeholder="Press Enter to submit query.",
                        classes="hidden")
        with VerticalGroup(id="job_container"):
            yield JobPage(project=self.project,
                          user=self.user,
                          n_lines=self.n_lines,
                          step=self.step
                          )
        with VerticalGroup(id="log_container", classes="hidden"):
            yield LogPage()
        yield Footer()

    def action_quit(self):
        """An action to quit the app."""
        sys.exit()

    def action_update(self):
        """Refresh page."""
        job_container = self.query_one("#job_container")
        log_container = self.query_one("#log_container")

        # Si on est sur la page de jobs
        if not "hidden" in job_container.classes:
            job_page = job_container.query_one(JobPage)
            job_page.read_job_log()
            job_page.show_jobs()

        # Si on est sur la page des logs
        if not "hidden" in log_container.classes:
            log_page = log_container.query_one(LogPage)
            current = log_page.query_one(LogDNAnexus)
            current.clear()
            current.get_current()

        self.notify("Page updated")

    def action_home(self):
        """An action to return to the main page."""
        # Empty and hide the log page
        log_container = self.query_one("#log_container")
        log_container.add_class("hidden")
        log_page = log_container.query_one(LogPage)
        log_page.query_one(ProgressBar).add_class("hidden")
        log_page.query_one(Link).add_class("hidden")
        log_page.query_one(Log).remove()

         # Show job page
        self.query_one("#job_container").remove_class("hidden")
        self.refresh_bindings()

        # Show search bar if existent
        search_bar = self.query_one(SearchBar)
        if search_bar.value:
            search_bar.remove_class("hidden")

    def action_show_all(self):
        """Show only done jobs."""
        job_page = self.query_one(JobPage)

        # Remove search
        job_page.search = ""
        search_bar = self.query_one(SearchBar)
        search_bar.value = ""
        search_bar.add_class("hidden")

        # Update page
        job_page.show_all_jobs()

    def action_show_done(self):
        """Show only done jobs."""
        job_page = self.query_one(JobPage)

        # Filters
        job_page.show_done = True
        job_page.show_running = False
        job_page.show_failed = False

        # Update page
        job_page.hide_all_jobs()
        job_page.show_jobs()

        self.check_jobs(job_type="done")

    def action_show_running(self):
        """Show only running/waiting jobs."""
        job_page = self.query_one(JobPage)

        # Filters
        job_page.show_done = False
        job_page.show_running = True
        job_page.show_failed = False

        # Update page
        job_page.hide_all_jobs()
        job_page.show_jobs()

        self.check_jobs(job_type="running")

    def action_show_failed(self):
        """Show only failed jobs."""
        job_page = self.query_one(JobPage)

        # Filters
        job_page.show_done = False
        job_page.show_running = False
        job_page.show_failed = True

        # Update page
        job_page.hide_all_jobs()
        job_page.show_jobs()

        self.check_jobs(job_type="failed")

    def action_add_jobs(self):
        """Increase the number of jobs displayed."""
        self.query_one(JobPage).add_jobs()

    def action_remove_jobs(self):
        """Decrease the number of jobs displayed."""
        self.query_one(JobPage).remove_jobs()

    def action_search_jobs(self):
        """Open/close the search bar."""
        search_bar = self.query_one(SearchBar)
        search_bar.remove_class("hidden")
        if "hidden" not in search_bar.classes:
            search_bar.can_focus = True
            search_bar.focus(scroll_visible=True)

    def check_action(self, action: str, parameters: tuple[object, ...]):
        """Check if an action may run.

        Helps with hiding keybinds from specific pages.
        """
        no_job_binds = ["show_all", "show_done", "show_running",
                        "show_failed", "add_jobs", "remove_jobs",
                        "search_jobs"]
        no_log_binds = ["home"]

        if (action in no_log_binds and
            "hidden" not in self.query_one("#job_container").classes):
            return False
        if (action in no_job_binds and
            "hidden" not in self.query_one("#log_container").classes):
            return False
        return True

    def check_jobs(self, job_type=""):
        """Check if jobs are displayed."""
        visible_jobs = [
            job for job in self.query(Job)
            if not job.has_class("hidden")
        ]
        if not visible_jobs:
            self.notify(f"No {job_type} jobs found.", severity="warning")

def run():
    """Run the log reader application."""
    parser = argparse.ArgumentParser(
        prog="DNAnexus Log Reader",
        description="Read DNAnexus job logs directly from the command line."
    )
    parser.add_argument('-p',
                        dest="project",
                        default="",
                        type=str,
                        help="show jobs from said project (default: current)"
                        )
    parser.add_argument('-u',
                        dest="user",
                        default="",
                        type=str,
                        help="show only jobs from said user (default: all)"
                        )
    parser.add_argument('-n',
                        dest="n_lines",
                        default=100,
                        type=int,
                        help="show n jobs (default: 100)"
                        )
    parser.add_argument('-s',
                        dest="step",
                        default=100,
                        type=int,
                        help="add/remove s jobs (default: 100)"
                        )

    # Arguments
    nargs = parser.parse_args()
    project, user, n_lines, step = nargs.project, nargs.user, nargs.n_lines, nargs.step

    app = Joblog(project=project, user=user, n_lines=n_lines, step=step)
    app.run()

if __name__ == "__main__":
    run()
