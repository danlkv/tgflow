False
# <p align="center">tgflow

<p align="center">A declarative-style telegram bot<a href="https://core.telegram.org/bots/api">Telegram Bot API</a> framework

* [Getting started.](#getting-started)
* [Writing your first bot](#writing-your-first-bot)
* [Architecture](#architecture)
* [Types](#types)
  * [Prepare](#prepare)
  * [Actions](#actions)
  * [Post processing](#post)
* [Usage](#usage)
  * [Prepare](#prepare)
  * [Actions](#actions)
  * [Post processing](#post-processing)
* [CofeeUI](#coffeui)
* [What you should care of](#what-you-should-care-of)
* [More examples](#more-examples)

## Getting started.

There are two ways to install the library:

* Installation using pip (a Python package manager)*:

```
pip3 install tgflow
```
* Installation from source (requires git):

```
$ git clone https://github.com/DaniloZZZ
$ cd tgflow
$ python3 setup.py install
```

It is generally recommended to use the first option.

**While the API is production-ready, it is still under development and it has regular updates, do not forget to update it regularly by calling `pip install tgflow --upgrade`*

## Writing your first bot

