# Khod-Nevis: An LLM-based code-writing agent

[![khod-kaar CI](https://github.com/danmohad/khod-kaar/actions/workflows/ci-main.yml/badge.svg)](https://github.com/danmohad/khod-kaar/actions/workflows/ci-main.yml)

## What is it
A program to write, test, document and execute arbitrary code.

## How does it work
-- Diagram --
The code performs three key functions: interaction with an LLM, LLM output parsing for code, and code execution via the shell.


## MIT License
This repo is under an MIT License. Still, I urge you to be responsible with the abilities it gives you.

## Don't be evil
It's not difficult to think of ways to perform nefarious and antisocial actions with AI in general and LLMs in particular. Don't do them.

## Don't be dumb
Understand that `khod-nevis` interacts with the shell where it is run. Commands and code executed by `khod-nevis` may damage your machine or even other machines; it has just as much authority over the environment in which it is run as you do. Be sure you understand each shell command `khod-nevis` will execute before approving it. Exercise extreme caution in using the autopilot `-a` flag.

## How to run it


## Containerized with Docker
Running the code in a containerized environment is safer for your file system. A Docker file is provided with the repo to set up a Debian environment with some common dependencies.

## Contributing
Forks and pull requests are welcome! For some ideas on what to work on, see the `Good first issues`. Please adhere to the Google style guide for Python TODO --link--.

## Ready-for-dev with VSCode
The easiest way to get started contributing to `khod-kaar` is by loading it as a dev container in VSCode. 


