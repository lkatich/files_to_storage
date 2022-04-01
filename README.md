# files_to_storage
The project solving the task below:

There is a service that generates a stream of data files.File sizes vary greatly, from tens of megabytes to several thousand megabytes.
Each file contains lines like “123 12345”. The first number is the consumer identifier, the second is the amount of the consumed resource. Space is used as a separator. The stream of files must be processed by summing up the amount of resource for each individual consumer. The resulting data is be added to some storage.

## Installation

Clone the project and execute the run.sh script.



## Usage

Run.sh script starts docker container with the service which is checking the folder where the files are to come. Folders for files and storage (for calculated data and processed files) are also created via run.sh in the current directory.

To change the period of files checking - go to the conf/config.yml
To change the logs visualization, for example - remove from console - go to the conf/log_config.yml and update the handlers to be only "debug_handler"


To generate test files you may use files_generator script. Run files_generator.py --help to check the usage. 
Set the required -wd parameter as the path to the newly created "files" folder 

```bash
./files_generator.py 

usage: files_generator.py [-h] [-l LINES] [-p PERIOD] [-fn FILES_NUMBER] -wd WORK_DIR

options:
  -h, --help        show this help message and exit
  -l LINES          Quantity of lines in the file (default = 100)
  -p PERIOD         Files creation period in seconds. If none is specified, the program runs once.
  -fn FILES_NUMBER  Quantity of files created per one iteration
  -wd WORK_DIR      Directory to which the files will go

```



