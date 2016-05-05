from invoke import task, run, call
import contextlib
import os
import shutil

@task
def graphs():
    """ Compiles graphs into project site folder. """
    site_path = os.path.join(os.getcwd(), "site")
    run("plantuml -tsvg -o {0} {1}".format(os.path.join(site_path, "graphs"), os.path.join("docs", "graphs")), echo=True)

@task
def api():
    """ Compiles API reference into project site folder. """
    lein("codox")

@task
def examples():
    """ Compiles examples into project site folder. """
    site_path = os.path.join(os.getcwd(), "site")

    for example_name in os.listdir("examples"):
        example_path = os.path.join("examples", example_name)
        if os.path.isfile(os.path.join(example_path, "project.clj")):
            with chdir(example_path):
                lein("clean")

                if example_name == "todomvc":
                    lein("cljsbuild-min")
                else:
                    lein("cljsbuild once min")

                shutil.copytree(os.path.join("resources", "public"),
                                os.path.join(site_path, "examples", example_name))

@task(post=[call(graphs), call(api), call(examples)])
def site():
    """ Cleans site folder, builds project site, compiles graphs and examples into site folder. """
    run("mkdocs build --clean", echo=True)

################################################### HELPERS
@contextlib.contextmanager
def chdir(dirname):
    curdir = os.getcwd()
    try:
        os.chdir(dirname)
        print("current dir: %s" % dirname)
        yield
    finally:
        os.chdir(curdir)

def lein(args):
    run("lein {0}".format(args), echo=True)
