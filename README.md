# miniprojekti

[![CI workflow badge](https://github.com/eepek/miniprojekti/workflows/CI/badge.svg)](https://github.com/eepek/miniprojekti/actions/workflows/CI.yml)
[![Codecov badge](https://codecov.io/gh/eepek/miniprojekti/graph/badge.svg?token=TFLFQVR8IK)](https://codecov.io/gh/eepek/miniprojekti)

OHTU miniprojekti

## Documentation

[Definition of Done](https://github.com/eepek/miniprojekti/blob/main/documentation/DefinitionOfDone.md)

[Backlog](https://docs.google.com/spreadsheets/d/19v00G-VI-Rlz3bFYKhHjXqyY6iUIFJM2/edit?usp=drive_link&ouid=103137629498632882562&rtpof=true&sd=true)

[User Manual](https://github.com/eepek/miniprojekti/blob/main/Documents/UserManual.md)

## Installation

1. Clone repository [Miniprojekti](https://github.com/eepek/miniprojekti)
2. install dependencies:

```bash
poetry install
```

## Command line actions

All command line actions to be run on project main folder.

1. Start Poetry shell:

```bash
poetry poetry shell
```

All following actions are to be run on Poetry shell.

2. Start Program:

```bash
python3 src/index.py
```

3. Static code analysis is run with:

```bash
pylint src
```

4. Unit tests are run with:

```bash
pytest src
```

5. Test coverage is run with:

```bash
coverage run --branch -m pytest src
```

6. Test coverage report can be generated with:

```bash
coverage report -m
```

7. Html format can be generated

```bash
coverage html
```
