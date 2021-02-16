import argparse
import logging
import pprint
import requests

from cmd import Cmd
from ibm_watson_machine_learning.wml_client_error import ApiRequestFailure

from dowmlclient import DOWMLClient, InvalidCredentials


class CommandNeedsJobID(Exception):
    pass


class DOWMLInteractive(Cmd):
    prompt = 'dowml> '
    intro = ('''
Decision Optimization in WML Interactive.
Submit and manage Decision Optimization models interactively.

Type ? for a list of commands.

Most commands need an argument that can be either a job id, or the number
of the job, as displayed by the 'jobs' command.  If a command requires a
job id, but none is specified, the last one is used.
''')

    def __init__(self, wml_cred_file):
        super().__init__()
        self.client = DOWMLClient(wml_cred_file)
        self.jobs = []
        self.last_job_id = None

    def emptyline(self) -> bool:
        # Just hitting enter should _not_ repeat a command
        return False

    def _number_to_id(self, number):
        if not number:
            # If nothing specified, use the last job id
            number = self.last_job_id
        if not number:
            raise CommandNeedsJobID
        if number in self.jobs:
            # Easy: we simply have an existing job id
            return number
        if str.isdigit(number):
            num = int(number)
            if 0 < num <= len(self.jobs):
                return self.jobs[num - 1]
        # It may be a job we don't know yet...
        return number

    @staticmethod
    def do_exit(_):
        """Exit this program."""
        return True

    def do_type(self, model_type):
        """type [type-of-model]
Prints current model type (if no argument), or sets the model type."""
        known_types = ', '.join(self.client.MODEL_TYPES)
        if not model_type:
            print(f'Current model type: {self.client.model_type}. Known types: {known_types}')
            # Let's make sure we don't set the model_type to None, but
            # return immediately
            return
        if model_type not in self.client.MODEL_TYPES:
            print(f'Warning: unknown model type \'{model_type}\'. Known types: {known_types}')
        # We set the type nevertheless: this code may not be up-to-date
        self.client.model_type = model_type

    def do_size(self, tshirt_size):
        """size [size-of-deployment]
Prints current deployment size (if no argument), or sets the deployment size."""
        sizes = self.client.TSHIRT_SIZES
        known_sizes = ', '.join(sizes)
        if not tshirt_size:
            print(f'Current size: {self.client.tshirt_size}. Known sizes: {known_sizes}')
            # Let's make sure we don't set the tshirt_size to None, but
            # return immediately
            return
        if tshirt_size not in sizes:
            print(f'Warning: unknown tee-shirt size \'{tshirt_size}\'. Known sizes: {known_sizes}')
        # We set the size nevertheless: this code may not be up-to-date
        self.client.tshirt_size = tshirt_size

    def do_solve(self, paths):
        """solve file1 [file2 ... [filen]]
Starts a job to solve a CPLEX model. At least one file of the correct type must be specified as argument."""
        if not paths:
            print('This command requires at least one file name as argument.')
            return
        job_id = None
        try:
            job_id = self.client.solve(paths)
        except FileNotFoundError as exception:
            print(exception)
        else:
            print(f'Job id: {job_id}')
        self.last_job_id = job_id

    def do_wait(self, job_id):
        """wait [job]
Waits until the job is finished, printing activity. Hit Ctrl-C to interrupt.
job is either a job number or a job id. Uses current job if not specified."""
        job_id = self._number_to_id(job_id)
        try:
            self.client.wait_for_job_end(job_id, True)
        except KeyboardInterrupt:
            # The user interrupted. That's perfectly fine...
            pass
        self.last_job_id = job_id

    def do_jobs(self, _):
        """job
Lists all the jobs in the space.
Current job, if any, is indicated with an arrow."""
        jobs = self.client.get_jobs()
        self.jobs = []
        print('     #   status     id                                    creation date             inputs')
        for i, j in enumerate(jobs, start=1):
            # Prepare list of input files
            names = ', '.join(j.names)
            # Add this job id in the list, to allow for translation from job number
            self.jobs.append(j.id)
            # Mark the job used if none specified
            mark = '   '
            if j.id == self.last_job_id:
                mark = '=> '
            print(f'{mark}{i:>3}: {j.status:>10}  {j.id}  {j.created}  {names}')

    def do_log(self, job_id):
        """log [job]
Prints the engine log for the given job.
job is either a job number or a job id. Uses current job if not specified."""
        job_id = self._number_to_id(job_id)
        log = self.client.get_log(job_id)
        print(log)
        self.last_job_id = job_id

    def do_output(self, job_id):
        """output [job]
Downloads all the outputs of a job.
job is either a job number or a job id. Uses current job if not specified."""
        job_id = self._number_to_id(job_id)
        outputs = self.client.get_output(job_id)
        for name, content in outputs:
            self.save_content(job_id, name, content)
        self.last_job_id = job_id

    @staticmethod
    def save_content(job_id, name, content):
        file_name = f'{job_id}_{name}'
        with open(file_name, 'wb') as f:
            print(f'Storing {file_name}')
            f.write(content)

    def do_details(self, arguments, printer=pprint.pprint):
        """details [job] [full]
Prints most of the details for the given job. Add 'full' to get the actual contents of inputs and outputs.
job is either a job number or a job id. Uses current job if not specified."""
        full = False
        job_id = None
        for arg in arguments.split():
            if arg == 'full':
                full = True
            else:
                job_id = self._number_to_id(arg)
        job_id = self._number_to_id(job_id)
        details = self.client.get_job_details(job_id, with_contents=full)
        printer(details, indent=4, width=120)
        self.last_job_id = job_id

    def do_delete(self, job_id):
        """delete [job|*]
Deletes the job specified. Use '*' to delete all the jobs.
job is either a job number or a job id. Uses current job if not specified."""
        if job_id == '*':
            while self.jobs:
                job = self.jobs[0]
                self.delete_one_job(job)
        else:
            self.delete_one_job(job_id)

    def delete_one_job(self, job_id):
        job_id = self._number_to_id(job_id)
        self.client.delete_job(job_id, True)
        if job_id in self.jobs:
            self.jobs.remove(job_id)
        assert job_id not in self.jobs  # Because a job appears only once
        if self.last_job_id == job_id:
            self.last_job_id = None

    def do_cancel(self, job_id):
        """cancel [job]
Stops the job specified.
job is either a job number or a job id. Uses current job if not specified."""
        job_id = self._number_to_id(job_id)
        self.client.delete_job(job_id, False)
        self.last_job_id = job_id


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Interactive program for DO on WML')
    parser.add_argument('-w', '--wml-cred-file', default=None,
                        help=f'Name of the file from which to read WML '
                             f'credentials. If not specified, credentials ' 
                             f'are read from environment variable '
                             f'${DOWMLClient.ENVIRONMENT_VARIABLE_NAME}.')
    args = parser.parse_args()

    # The force parameter is not listed in the arguments to basicConfig
    # noinspection PyArgumentList
    logging.basicConfig(force=True, format='%(asctime)s %(message)s',
                        level=logging.INFO)
    try:
        dowml = DOWMLInteractive(args.wml_cred_file)
        while True:
            again = False
            try:
                dowml.cmdloop()
            except ApiRequestFailure as failure:
                # This happens when an invalid job id is specified. We want
                # to keep running.
                again = True
            except requests.exceptions.ConnectionError as e:
                print(e)
                again = True
            except CommandNeedsJobID:
                print(f'This command requires a jod id or number, but you '
                      f'didn\'t specify one.  And there is no current job either.')
                again = True
            finally:
                # But let's not print again the starting banner
                dowml.intro = ''
            if not again:
                break
    except InvalidCredentials:
        print(f'\nERROR: credentials not found!\n')
        parser.print_help()
