# Cities number generator

Simple script that takes a file containing city names and generates
a number for each city name and allows you to run a query for a name to
get the number.


## Reasons for decisions

* There is a inventory which is used for adding and storing city names. It
  uses a Trie/Prefix tree data structure under the hood for efficient string
  searching. I could have used a more simple data structure like a Dict but I
  took the opportunity to showcase some code.

* I was not sure what I needed to do for the actual number calculation so I
  chose to just use the rune value for each character and add them up to
  give me a number. This algorithm does not cater for different words with
  the same amount of letters and the same letters. eg: add <-> dad will give
  the same number.


## Usage

This is a standalone application

### Help output

```bash
$ python3.5 generator.py -h
usage: generator.py [-h] -f FILENAME CITY

Return a generated number for a city name.

positional arguments:
  CITY                  City name.

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --file FILENAME
                        Filename containing city names.
```

### Running

Successful find

```bash
$ python3.5 generator.py -f cities.txt cork
City 'cork' has a number 431
```

Missing city name

```bash
$ python3.5 generator.py -f cities.txt unknown
Can not find 'unknown'
```
