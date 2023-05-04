# Requirements Checker

This is a python3 program that checks if the libraries in the requirements.txt file are up to date.

## Usage

To run the program, you need to have python3 and the modules listed in the requirements.txt file installed on your system. You can install them using pip:

`pip install requests beautifulsoup4`

Then you can run the program with the following command:

`python3 requirements_checker.py [-p PATH] [-v] [-f]`

The optional arguments are:

- `-p PATH` or `--path PATH`: specify the path of the requirements file (default is requirements.txt)
- `-v` or `--verbose`: display additional information such as errors and release dates
- `-f` or `--force`: to overwrite the requirements.txt

The program will print the results on the terminal and create a new file called requirements-updated.txt with the updated versions of the libraries.

## Example

Here is an example of running the program with a sample requirements.txt file:

`python3 requirements_checker.py -v`
or 
`python3 requirements_checker.py --force`

