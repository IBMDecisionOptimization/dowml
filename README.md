# dowml
A library and command line client to use Decision Optimization on WML

*Note that this tool is not an official IBM product, and is not supported by IBM. This is educational material, 
use at your own risks.*

## tldr;

```
$ pip install dowml
$ cat my_credentials.txt
{
    'apikey': '<apikey>',
    'region': 'us-south',
    'cos_resource_crn': 'crn:v1:bluemix:public:cloud-object-storage:global:a/76260f9...',
    'ml_instance_crn': 'crn:v1:bluemix:public:pm-20:eu-de:a/76260f...'
}
$ dowml -w my-credentials.txt
dowml> solve examples/afiro.mps
dowml> wait
dowml> log
dowml> exit
```

## Introduction

The class `DOWMLLib` provides an API to upload Decision Optimization models (CPLEX, CP Optimizer, OPL or docplex) to WML, check their status, and download results.  The script `dowml.py` is an interactive program on top of that library.

In order to use either of them, you need to provide IBM Cloud credentials.
- By default, `DOWMLLib` (and therefore the Interactive) look for these credentials in an environment variable named `DOWML_CREDENTIALS`. This variable shoud have a value looking like
```
{
    'apikey': '<apikey>',
    'region': 'us-south',
    'cos_resource_crn': 'crn:v1:bluemix:public:cloud-object-storage:global:a/76260f9...',
    'ml_instance_crn': 'crn:v1:bluemix:public:pm-20:eu-de:a/76260f...',
}
```
See below for how/where to get these credentials.
- As an alternative, you can specify a file name as argument to 
`DOWMLLib.__init__`. The credentials will then be read from that file instead 
of the environment variable. Accordingly, the Interactive has a command line 
option `-w` (or `--wml-cred-file`) that must be followed by the path of the file.
- Finally, if none of the above options are used, the code will look for
environment variable `DOWML_CREDENTIALS_FILE`. If it exists, it must be the path
to a file that contains credentials such as the ones above.

Here's a sample session:
```
$ dowml -h
usage: dowml [-h] [--wml-cred-file WML_CRED_FILE] [--verbose]
             [--commands [COMMANDS [COMMANDS ...]]] [--input] [--space SPACE] [--url URL]
             [--region REGION]

Decision Optimization in WML Interactive, version 1.5.0.
Submit and manage Decision Optimization models interactively.
(c) Copyright Xavier Nodet, 2021

optional arguments:
  -h, --help            show this help message and exit
  --wml-cred-file WML_CRED_FILE, -w WML_CRED_FILE
                        Name of the file from which to read WML credentials. If not specified,
                        credentials are read from environment variable $DOWML_CREDENTIALS. If no
                        such variable exists, but variable $DOWML_CREDENTIALS_FILE exists, tries
                        to read that file.
  --verbose, -v         Verbose mode. Causes the program to print debugging messages about its
                        progress. Multiple -v options increase the verbosity. The maximum is 4.
  --commands [COMMANDS [COMMANDS ...]], -c [COMMANDS [COMMANDS ...]]
                        Carries out the specified commands. Each command is executed as if it had
                        been specified at the prompt. The program stops after last command, unless
                        --input is used.
  --input, -i           Prompts for new input commands even if some commands have been specified
                        as arguments using --commands.
  --space SPACE, -s SPACE
                        Id of the space to connect to. Takes precedence over the one specified in
                        the credentials under the 'space_id' key, if any.
  --url URL, -u URL     URL to use for the Machine Learning service. Takes precedence over the one
                        specified in the credentials under the 'url' key, if any. Incompatible
                        with --region argument.
  --region REGION, -r REGION
                        Region to use for the Machine Learning service. Takes precedence over the
                        region or URL specified in the credentials, if any. Incompatible with
                        --url argument. Possible values for the region are ['us-south', 'eu-de',
                        'eu-gb', 'jp-tok'].
$
$
$ dowml -c help type size 'inputs inline' 'solve examples/afiro.mps' jobs wait jobs log 'type docplex' 'solve examples/markshare.py examples/markshare1.mps.gz' wait jobs dump 'shell ls -l *-*-*-*-*' 'delete *'

Decision Optimization in WML Interactive, version 1.5.0.
Submit and manage Decision Optimization models interactively.
(c) Copyright Xavier Nodet, 2021

Type ? for a list of commands.

Most commands need an argument that can be either a job id, or the number
of the job, as displayed by the 'jobs' command.  If a command requires a
job id, but none is specified, the last one is used.

dowml> help

Documented commands (type help <topic>):
========================================
cancel  details  exit  inline  jobs  output   shell  solve   time  version
delete  dump     help  inputs  log   outputs  size   status  type  wait

dowml> type
Current model type: cplex.
Known types: cplex, cpo, opl, docplex.
dowml> size
Current size: S.
Known sizes: S, M, XL.
dowml> inputs inline
dowml> solve examples/afiro.mps
Job id: f4a6a1ca-8e91-4ef1-bf03-47010d87d21c
dowml> jobs
     #  status      id                                    creation date        type     ver.   size  inputs
=>   1: queued      f4a6a1ca-8e91-4ef1-bf03-47010d87d21c  2021-11-12 14:27:52  cplex    20.1   S     afiro.mps
dowml> wait
Job is completed.
Job has finished with status 'completed'.
dowml> jobs
     #  status      id                                    creation date        type     ver.   size  inputs
=>   1: completed   f4a6a1ca-8e91-4ef1-bf03-47010d87d21c  2021-11-12 14:27:52  cplex    20.1   S     afiro.mps
dowml> log
[2021-11-12T13:28:09Z, INFO] CPLEX version 20010000
[2021-11-12T13:28:09Z, WARNING] Changed parameter CPX_PARAM_THREADS from 0 to 1
[2021-11-12T13:28:09Z, INFO] Param[1,067] = 1
[2021-11-12T13:28:09Z, INFO] Param[1,130] = UTF-8
[2021-11-12T13:28:09Z, INFO] Param[1,132] = -1
[2021-11-12T13:28:09Z, INFO]
[2021-11-12T13:28:09Z, INFO] Selected objective sense:  MINIMIZE
[2021-11-12T13:28:09Z, INFO] Selected objective  name:  obj
[2021-11-12T13:28:09Z, INFO] Selected RHS        name:  rhs
[2021-11-12T13:28:09Z, INFO] Version identifier: 20.1.0.0 | 2020-11-10 | 9bedb6d68
[2021-11-12T13:28:09Z, INFO] CPXPARAM_Threads                                 1
[2021-11-12T13:28:09Z, INFO] CPXPARAM_Output_CloneLog                         -1
[2021-11-12T13:28:09Z, INFO] CPXPARAM_Read_APIEncoding                        "UTF-8"
[2021-11-12T13:28:09Z, INFO] Tried aggregator 1 time.
[2021-11-12T13:28:09Z, INFO] LP Presolve eliminated 9 rows and 10 columns.
[2021-11-12T13:28:09Z, INFO] Aggregator did 7 substitutions.
[2021-11-12T13:28:09Z, INFO] Reduced LP has 11 rows, 15 columns, and 37 nonzeros.
[2021-11-12T13:28:09Z, INFO] Presolve time = 0.00 sec. (0.03 ticks)
[2021-11-12T13:28:09Z, INFO]
[2021-11-12T13:28:09Z, INFO] Iteration log . . .
[2021-11-12T13:28:09Z, INFO] Iteration:     1   Scaled dual infeas =             1.200000
[2021-11-12T13:28:09Z, INFO] Iteration:     5   Dual objective     =          -464.753143
[2021-11-12T13:28:09Z, INFO] There are no bound infeasibilities.
[2021-11-12T13:28:09Z, INFO] There are no reduced-cost infeasibilities.
[2021-11-12T13:28:09Z, INFO] Max. unscaled (scaled) Ax-b resid.          = 1.77636e-14 (1.77636e-14)
[2021-11-12T13:28:09Z, INFO] Max. unscaled (scaled) c-B'pi resid.        = 5.55112e-17 (5.55112e-17)
[2021-11-12T13:28:09Z, INFO] Max. unscaled (scaled) |x|                  = 500 (500)
[2021-11-12T13:28:09Z, INFO] Max. unscaled (scaled) |slack|              = 500 (500)
[2021-11-12T13:28:09Z, INFO] Max. unscaled (scaled) |pi|                 = 0.942857 (1.88571)
[2021-11-12T13:28:09Z, INFO] Max. unscaled (scaled) |red-cost|           = 10 (10)
[2021-11-12T13:28:09Z, INFO] Condition number of scaled basis            = 1.5e+01
[2021-11-12T13:28:09Z, INFO] optimal (1)
dowml> type docplex
dowml> solve examples/markshare.py examples/markshare1.mps.gz
Job id: 82467929-dbe8-46f0-99eb-f83aea04142a
dowml> wait
Job is completed.
Job has finished with status 'completed'.
dowml> jobs
     #  status      id                                    creation date        type     ver.   size  inputs
     1: completed   f4a6a1ca-8e91-4ef1-bf03-47010d87d21c  2021-11-12 14:27:52  cplex    20.1   S     afiro.mps
=>   2: completed   82467929-dbe8-46f0-99eb-f83aea04142a  2021-11-12 14:28:14  docplex  20.1   S     markshare.py, markshare1.mps.gz
dowml> dump
Storing 82467929-dbe8-46f0-99eb-f83aea04142a/markshare.py
Storing 82467929-dbe8-46f0-99eb-f83aea04142a/markshare1.mps.gz
Storing 82467929-dbe8-46f0-99eb-f83aea04142a/model.lp
Storing 82467929-dbe8-46f0-99eb-f83aea04142a/solution.json
Storing 82467929-dbe8-46f0-99eb-f83aea04142a/kpis.csv
Storing 82467929-dbe8-46f0-99eb-f83aea04142a/stats.csv
Storing 82467929-dbe8-46f0-99eb-f83aea04142a/log.txt
Storing 82467929-dbe8-46f0-99eb-f83aea04142a/details.json
dowml> shell ls -l *-*-*-*-*
total 88
-rw-rw-r--  1 nodet  staff  5598 Nov 12 14:28 details.json
-rw-rw-r--  1 nodet  staff    39 Nov 12 14:28 kpis.csv
-rw-rw-r--  1 nodet  staff  7162 Nov 12 14:28 log.txt
-rw-rw-r--  1 nodet  staff   670 Nov 12 14:28 markshare.py
-rw-rw-r--  1 nodet  staff  1607 Nov 12 14:28 markshare1.mps.gz
-rw-rw-r--  1 nodet  staff  4203 Nov 12 14:28 model.lp
-rw-rw-r--  1 nodet  staff  1770 Nov 12 14:28 solution.json
-rw-rw-r--  1 nodet  staff   341 Nov 12 14:28 stats.csv
dowml> delete *
```


## WML credentials

The DOWML client requires some information in order to connect to the Watson
Machine Learning service.  Two pieces of information are required, and the others
are optional.

### Required items

- The `apikey` is a secret that identifies the IBM Cloud user. One typically creates
  one key per application or service, in order to be able to revoke them individually
  if needed.
  To generate such a key, open https://cloud.ibm.com/iam/apikeys, and click the blue
  'Create an IBM Cloud API key' on the right.

- The `url` is the base URL for the REST calls to WML.  The possible values are
  found in https://cloud.ibm.com/apidocs/machine-learning#endpoint-url, 
  and depend on which region you want to use.

- As an alternative to the `url` value, you can use a more user-friendly and 
  easier to remember `region`, with a value that is either `us-south`, `eu-de`,
  `eu-gb` or `jp-tok`.  From this value, _dowml_ will deduce the correct URL to use.
  To avoid ambiguities or duplications, it is not allowed to use both `url` and
  `region`.

### Optional items

Watson Studio and Watson Machine Learning use _spaces_ to group together, and
isolate from each other, the assets that belong to a single project.  These assets 
include the data files submitted, the results of the jobs, and the _deployments_
(software and hardware configurations) that run these jobs.

The DOWML client will connect to the space specified by the user using
either the `--space` command-line argument or the `space_id` item in the credentials.
If neither of these are specified, the client will look for a space named 
_DOWMLClient-space_, and will try to create such a space if one doesn't exist.
To create a new space, the DOWML client will need both `cos_resource_crn` and
`ml_instance_crn` to have been specified in the credentials.

- `space_id`: identifier of an existing space to connect to.  Navigate to the 
  'Spaces' tab of your Watson Studio site (e.g. 
  https://eu-de.dataplatform.cloud.ibm.com/ml-runtime/spaces if you are using
  the instance in Germany), right-click on the name of an existing space to
  copy the link. The id of the space is the string of numbers, letters and dashes
  between the last `/` and the `?`.

- `cos_resource_crn`: WML needs to store some data in a Cloud Object Storage 
  instance.  Open
  https://cloud.ibm.com/resources and locate the 'Storage' section.  Create an
  instance of the Cloud Object Storage service if needed. Once it's listed on
  the resource page, click anywhere on the line for that service, except on its
  name.  This will open a pane on the right which lists the CRN.  Click on the
  symbol at the right to copy this information.  This item is required only for 
  the DOWML client to be able to create a space.  If you specified a `space_id`,
  it is not required.
   
- `ml_instance_crn`: similarly, you need to identify an instance of Machine 
  Learning service to use
  to solve your jobs.  In the same page https://cloud.ibm.com/resources, open the
  'Services' section.  The 'Product' columns tells you the type of service.  If
  you don't have a 'Machine Learning' instance already, create one.  Then click
  on the corresponding line anywhere except on the name, and copy the CRN displayed
  in the pane that open on the right.  This item is required only for 
  the DOWML client to be able to create a space.  If you specified a `space_id`,
  it is not required.

## Using data assets in Watson Studio

The DOWML library has two modes of operation with respect to sending the models
to the WML service: inline data, or using data assets in Watson Studio.  By default,
data assets are used for inputs, while inline data is used for outputs. 
This can be changed with the `inputs` and `outputs` commands.

With inline data, the model is sent directly to the WML service in the _solve_
request itself, and the output is part of the job details that are downloaded when
asking for information about the job.  
This is the simplest, but it has a number of drawbacks:

- Sending a large model may take a long time, because of network throughput.  Sending
a very large REST request is not at all guaranteed to succeed.  Similarly, if your
job has large outputs, the job may fail while trying to process them.

- When solving several times the same model (e.g. to evaluate different parameters),
the model has to be sent each time.

- In order to display the names of the files that were sent, the _jobs_ command
needs to request this information, and it comes with the content of the files
  themselves.  In other words, every _jobs_ command requires downloading the content
  of all the inline data files for all the jobs that exist in the space.

Using data assets in Watson Studio as an intermediate step alleviate all these issues:

- Once the model has been uploaded to Watson Studio, it will be reused for
subsequent jobs without the need to upload it again.

- The job requests refer to the files indirectly, via URLs.  Therefore, they don't
take much space, and listing the jobs doesn't imply to download the content of the
  files.

- Uploading to Watson Studio is done through specialized code that doesn't just send a single
request.  Rather, it divides the upload in multiple reasonably sized chunks that each
  are uploaded individually, with restart if necessary.  Uploading big files is
  therefore much less prone to failure.

