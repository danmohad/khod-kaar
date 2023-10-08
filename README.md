# Khod-Kaar: An LLM-based code-writing agent

[![khod-kaar CI](https://github.com/danmohad/khod-kaar/actions/workflows/ci-main.yml/badge.svg)](https://github.com/danmohad/khod-kaar/actions/workflows/ci-main.yml)

## What is it
A program to write, test, document and execute arbitrary code.

## How does it work
-- Diagram --
The code performs three key functions: interaction with an LLM, LLM output parsing for code, and code execution via the shell.

## What's with the name?
In many languages of south-central Asia and the Indian subcontinent, the word _khod_ means 'self' and _kaar_ means 'work' or 'action'. Thus, to many people, _khod kaar_ can render a meaning like 'autonomous action', which is what this repo does. _Khod_ also sounds like 'code', and _code kaar_ has a meaning approaching 'code worker', which is what this repo is. In Persian the term _khod kaar_ specifically means 'ball-point pen'. When compared to a quill or reed, a ball-point pen is certainly closer to autonomous action by easing the task of the writer, and that is also what this repo aims to do.

## MIT License
This repo is under an MIT License. Still, I urge you to be responsible with the abilities it gives you.

## Don't be evil
It's not difficult to think of ways to perform nefarious and antisocial actions with AI in general and LLMs in particular. Don't do them.

## Don't be dumb
Understand that `khod-kaar` interacts with the shell where it is run. Commands and code executed by `khod-kaar` may damage your machine or even other machines; it has just as much authority over the environment in which it is run as you do. Be sure you understand each shell command `khod-kaar` will execute before approving it. Exercise extreme caution in using the autopilot `-a` flag.

## How to run it


## Containerized with Docker
Running the code in a containerized environment is safer for your file system. A Docker file is provided with the repo to set up a Debian environment with some common dependencies.

## Contributing
Forks and pull requests are welcome! For some ideas on what to work on, see the `Good first issues`. Please adhere to the Google style guide for Python TODO --link--.

## Ready-for-dev with VSCode
The easiest way to get started contributing to `khod-kaar` is by loading it as a dev container in VSCode. 


