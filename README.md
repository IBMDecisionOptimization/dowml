# dowml
A library and command line client to use Decision Optimization on WML

## tldr;

```
$ git clone git@github.ibm.com:xavier-nodet/dowml.git
$ cd dowml
$ source venv/bin/activate
$ cat tests/test_credentials.txt
{
    'apikey': '<apikey>',
    'url': 'https://us-south.ml.cloud.ibm.com',
    'cos_resource_crn' = 'crn:v1:bluemix:public:cloud-object-storage:global:a/76260f9...',
    'ml_instance_crn': 'crn:v1:bluemix:public:pm-20:eu-de:a/76260f...'
}
$ cp tests/test_credentials.txt my-credentials.txt
$ open my-credentials.txt
... put your own credentials
$ python3 dowml.py -w my-credentials.txt
dowml> solve examples/afiro.mps
dowml> wait
dowml> log
dowml> exit
```

## Introduction

The class `DOWMLLib` provides an API to upload Decision Optimization models (CPLEX, CP Optimizer, OPL or docplex) to WML, check their status, and download results.  The script `dowml.py` is an interactive program on top of that library.

In order to use either of them, you need to provide IBM Cloud credentials.
1. By default, `DOWMLLib` (and therefore the Interactive) look for these credentials in an environment variable named `DOWML_CREDENTIALS`. This variable shoud have a value looking like
   ```
   {
       'apikey': '<apikey>',
       'url': 'https://us-south.ml.cloud.ibm.com',
       'cos_resource_crn' = 'crn:v1:bluemix:public:cloud-object-storage:global:a/76260f9...',
       'ml_instance_crn': 'crn:v1:bluemix:public:pm-20:eu-de:a/76260f...',
   }
   ```
   See below for how/where to get these credentials.
2. As an alternative, you can specify a file name as argument to `DOWMLLib.__init__`. The credentials will then be read from that file instead of the environment variable. Accordingly, the Interactive has a command line option `-w` (or `--wml-cred-file`) that must be followed by the path of the file.

Here's a sample session:
```
$ python3 dowml.py -h
usage: dowml.py [-h] [-w WML_CRED_FILE] [--verbose]
                [--commands [COMMANDS [COMMANDS ...]]] [--input] [-s SPACE]

Interactive program for DO on WML

optional arguments:
  -h, --help            show this help message and exit
  -w WML_CRED_FILE, --wml-cred-file WML_CRED_FILE
                        Name of the file from which to read WML credentials.
                        If not specified, credentials are read from
                        environment variable $DOWML_CREDENTIALS.
  --verbose, -v         Verbose mode. Causes the program to print debugging
                        messages about its progress. Multiple -v options
                        increase the verbosity. The maximum is 4.
  --commands [COMMANDS [COMMANDS ...]], -c [COMMANDS [COMMANDS ...]]
                        Carries out the specified commands. Each command is
                        executed as if it had been specified at the prompt.
                        The program stops after last command.
  --input, -i           Prompts for new input commands even if some commands
                        have been specified as arguments using --commands.
  -s SPACE, --space SPACE
                        Id of the space to connect to. Takes precedence over
                        the one specified in the credentials under the
                        'space_id' key, if any.
$
$
$ python3 dowml.py -c help type size 'inline yes' 'solve examples/afiro.mps' jobs wait jobs log 'type docplex' 'solve examples/markshare.py examples/markshare1.mps.gz' wait jobs output

Decision Optimization in WML Interactive.
Submit and manage Decision Optimization models interactively.

Type ? for a list of commands.

Most commands need an argument that can be either a job id, or the number
of the job, as displayed by the 'jobs' command.  If a command requires a
job id, but none is specified, the last one is used.

dowml> help

Documented commands (type help <topic>):
========================================
cancel  details  help    jobs  output  solve  type
delete  exit     inline  log   size    time   wait

dowml> type
Current model type: cplex. Known types: cplex, cpo, opl, docplex
dowml> size
Current size: S. Known sizes: S, M, XL
dowml> inline yes
dowml> solve examples/afiro.mps
Job id: 7c4a13ac-63a0-44fa-ba78-88d7ae040b14
dowml> jobs
     #  status      id                                    creation date        type     size  inputs
=>   1: running     7c4a13ac-63a0-44fa-ba78-88d7ae040b14  2021-03-26 12:26:15  cplex    S     afiro.mps
dowml> wait
dowml> jobs
     #  status      id                                    creation date        type     size  inputs
=>   1: completed   7c4a13ac-63a0-44fa-ba78-88d7ae040b14  2021-03-26 12:26:15  cplex    S     afiro.mps
dowml> log
[2021-03-26T12:26:16Z, INFO] CPLEX version 12100000
[2021-03-26T12:26:16Z, WARNING] Changed parameter CPX_PARAM_THREADS from 0 to 1
[2021-03-26T12:26:16Z, INFO] Param[1,067] = 1
[2021-03-26T12:26:16Z, INFO] Param[1,130] = UTF-8
[2021-03-26T12:26:16Z, INFO] Param[1,132] = -1
[2021-03-26T12:26:16Z, INFO]
[2021-03-26T12:26:16Z, INFO] Selected objective sense:  MINIMIZE
[2021-03-26T12:26:16Z, INFO] Selected objective  name:  obj
[2021-03-26T12:26:16Z, INFO] Selected RHS        name:  rhs
[2021-03-26T12:26:16Z, INFO] Version identifier: 12.10.0.0 | 2020-01-09 | 0d94640
[2021-03-26T12:26:16Z, INFO] CPXPARAM_Threads                                 1
[2021-03-26T12:26:16Z, INFO] CPXPARAM_Output_CloneLog                         -1
[2021-03-26T12:26:16Z, INFO] CPXPARAM_Read_APIEncoding                        "UTF-8"
[2021-03-26T12:26:16Z, INFO] Tried aggregator 1 time.
[2021-03-26T12:26:16Z, INFO] LP Presolve eliminated 9 rows and 10 columns.
[2021-03-26T12:26:16Z, INFO] Aggregator did 7 substitutions.
[2021-03-26T12:26:16Z, INFO] Reduced LP has 11 rows, 15 columns, and 37 nonzeros.
[2021-03-26T12:26:16Z, INFO] Presolve time = 0.01 sec. (0.03 ticks)
[2021-03-26T12:26:16Z, INFO]
[2021-03-26T12:26:16Z, INFO] Iteration log . . .
[2021-03-26T12:26:16Z, INFO] Iteration:     1   Scaled dual infeas =             1.200000
[2021-03-26T12:26:16Z, INFO] Iteration:     5   Dual objective     =          -464.753143
[2021-03-26T12:26:17Z, INFO] There are no bound infeasibilities.
[2021-03-26T12:26:17Z, INFO] There are no reduced-cost infeasibilities.
[2021-03-26T12:26:17Z, INFO] Max. unscaled (scaled) Ax-b resid.          = 1.77636e-14 (1.77636e-14)
[2021-03-26T12:26:17Z, INFO] Max. unscaled (scaled) c-B'pi resid.        = 5.55112e-17 (5.55112e-17)
[2021-03-26T12:26:17Z, INFO] Max. unscaled (scaled) |x|                  = 500 (500)
[2021-03-26T12:26:17Z, INFO] Max. unscaled (scaled) |slack|              = 500 (500)
[2021-03-26T12:26:17Z, INFO] Max. unscaled (scaled) |pi|                 = 0.942857 (1.88571)
[2021-03-26T12:26:17Z, INFO] Max. unscaled (scaled) |red-cost|           = 10 (10)
[2021-03-26T12:26:17Z, INFO] Condition number of scaled basis            = 1.5e+01
[2021-03-26T12:26:17Z, INFO] optimal (1)
dowml> type docplex
dowml> solve examples/markshare.py examples/markshare1.mps.gz
Job id: a1c5057b-a49f-48ef-836e-e5890a75fa9f
dowml> wait
dowml> jobs
     #  status      id                                    creation date        type     size  inputs
     1: completed   7c4a13ac-63a0-44fa-ba78-88d7ae040b14  2021-03-26 12:26:15  cplex    S     afiro.mps
=>   2: completed   a1c5057b-a49f-48ef-836e-e5890a75fa9f  2021-03-26 12:26:25  docplex  S     markshare.py, markshare1.mps.gz
dowml> output
Storing a1c5057b-a49f-48ef-836e-e5890a75fa9f_solution.json
Storing a1c5057b-a49f-48ef-836e-e5890a75fa9f_log.txt
Storing a1c5057b-a49f-48ef-836e-e5890a75fa9f_details.json
```


## WML credentials

There are four pieces of information that are required in order to submit jobs on WML.

1. The `apikey` is a secret that identifies the IBM Cloud user. You typically create
   one key per application or service, in order to be able to revoke them individually
   if needed.
   To generate such a key, open https://cloud.ibm.com/iam/apikeys, and click the blue
   'Create an IBM Cloud API key' on the right.

2. The `url` is the base URL for the REST calls to WML.  The possible values are
   found in https://cloud.ibm.com/apidocs/machine-learning, and depend on which
   region you want to use.

3. WML needs to store some data in a Cloud Object Storage instance.  Open
   https://cloud.ibm.com/resources and locate the 'Storage' section.  Create an
   instance of the Cloud Object Storage service if needed. Once it's listed on
   the resource page, click anywhere on the line for that service, except on its
   name.  This will open a pane on the right which lists the CRN.  Click on the
   symbol at the right to copy this information.

4. Similarly, you need to identify an instance of Machine Learning service to use
   to solve your jobs.  In the same page https://cloud.ibm.com/resources, open the
   'Services' section.  The 'Product' columns tells you the type of service.  If
   you don't have a 'Machine Learning' instance already, create one.  Then click
   on the corresponding line anywhere except on the name, and copy the CRN displayed
   in the pane that open on the right.

## Using data assets in Watson Studio

The DOWML library has two modes of operation with respect to sending the models
to the WML service: inline data, or using data assets in Watson Studio.

With inline data, the model is sent directly to the WML service in the _solve_
request itself.  This is the simplest, but it has a number of drawbacks:

- When solving several times the same model (e.g. to evaluate different parameters),
the model has to be sent each time.

- In order to display the names of the files that were sent, the _jobs_ command
needs to request this information, and it comes with the content of the files
  themselves.  In other words, every _jobs_ command requires downloading the content
  of all the files for all the jobs that exist in the space.

- Sending a large model may take a long time, because of network throughput.  Sending
a very large REST request is not at all guaranteed to succeed.

Using data assets in Watson Studio as an intermediate step alleviate all these issues:

- Once the model has been uploaded to WS, it will be reused for
subsequent jobs without the need to upload it again.

- The job requests refer to the files indirectly, via URLs.  Therefore, they don't
take much space, and listing the jobs doesn't imply to download the content of the
  files.

- Uploading to WS is done through specialized code that doesn't just send a single
request.  Rather, it divides the upload in multiple reasonably sized chunks that each
  are uploaded individually, with restart if necessary.  Uploading big files is
  therefore much less prone to failure.

### Connecting to data outside COS

A job in Watson Studio, unless you use inline mode, refers to 'connected-data'
assets, that themselves refer to objects created in the Cloud Object Storage
(COS) service. If you have data or files that exist either in COS or in any other
cloud service, you can create data assets to refer to these.

Indeed, when it creates a job in `inline no` mode, DOWML first checks whether a
data asset of the given name exists.  The name here refers to the base name of the
file specified in the _solve_ command, that is, the name without the path.  If a
data asset with this name already exists, the job will refer to it.  If one such
asset doesn't exist, DOWML creates one and uploads the file.

As DOWML first checks whether a data asset exists before trying to create one,
it is possible to refer in your _solve_ commands to 'files' that don't exist on your
disk, but are data assets in your deployment space.

Creating these is left as an exercise to the reader...
