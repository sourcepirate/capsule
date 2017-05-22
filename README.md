## Capsule

Store and clone the github repositories you like without any commit history. 


## Installation
```
pip install capsule_cli
```

## Usage

```
usage: 
Save  your favorite repo

capsule <command> <param>

These are the commands:
-----------------------------------------------------
add         Adds a new url record to capsule with name
rupture     Clones the urls to the specified directory
list        List all saved repos

-h for help

positional arguments:
  command     Subcommand to run

optional arguments:
  -h, --help  show this help message and exit

```

## Instructions

```
#adding a repo
capsule add https://github.com/facebook/react.git

#rupture a capsule
capsule rupture react

#add help
usage: capsule [-h] [-n NAME] url

#rupture help
usage: capsule [-h] [-b BRANCH] [-o OUT] [-d DNAME] name


```

## License
MIT
