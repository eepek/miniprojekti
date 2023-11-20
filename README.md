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

1. To start program run:

```bash
poetry run invoke start
```

2. Static code analysis is run with:

```bash
poetry run invoke lint
```

3. Unit tests are run with:

```bash
poetry run invoke test
```

4. Test coverage is run with:

```bash
poetry run invoke coverage
```

5. Test coverage report can be generated with:

```bash
poetry run invoke coverage-report
```

6. Html format can be generated

```bash
poetry run invoke coverage-report-html
```
