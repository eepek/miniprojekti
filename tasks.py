from invoke import task

@task
def test(c):
    c.run('pytest src', pty=True)

@task
def test_robot(c):
    c.run('export DATABASE_FILENAME=test-database.sqlite; robot src/tests', pty=True)

@task
def coverage(c):
    c.run('coverage run --branch -m pytest src', pty=True)


@task(coverage)
def coverage_report(c):
    c.run('coverage report -m', pty=True)


@task(coverage)
def coverage_report_html(c):
    c.run('coverage html', pty=True)


@task
def lint(c):
    c.run('pylint src', pty=True)


@task
def build(ctx):
    ctx.run('python3 src/build.py', pty=True)
