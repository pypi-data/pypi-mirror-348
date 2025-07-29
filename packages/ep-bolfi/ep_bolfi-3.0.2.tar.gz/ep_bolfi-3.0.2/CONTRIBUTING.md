# Contributing to EP-BOLFI

If you'd like to contribute to EP-BOLFI, thank you very much and please have a look at the guidelines below.

## Workflow

We use [GIT](https://en.wikipedia.org/wiki/Git) and [GitLab](https://en.wikipedia.org/wiki/GitLab) to coordinate our work. When making any kind of update, we try to follow the procedure below.

### Before you begin

1. Create an [issue](https://docs.gitlab.com/ee/user/project/issues/) where new proposals can be discussed before any coding is done.
2. Download the source code onto your local system, by cloning the repository:
    ```bash
    git clone https://gitlab.dlr.de/cec/ep-bolfi
    ```
3. Install the library in editable mode:
    ```bash
    pip install -e ep-bolfi
    ```
4. Create a branch of this repo, where all changes will be made, and "checkout" that branch so that your changes live in that branch:
    ```bash
    git branch <branch_name>
    git checkout <branch_name>
    ```
    Or as a short-hand:
    ```bash
    git checkout -b <branch_name>
    ```

### Writing your code

4. EP-BOLFI is written in [Python](https://en.wikipedia.org/wiki/Python_(programming_language)), and makes heavy use of [ELFI](https://github.com/elfi-dev/elfi) as well as [PyBaMM](https://github.com/pybamm-team/PyBaMM).
5. Make sure to follow our [coding style guidelines](#coding-style-guidelines).
6. Commit your changes to your branch with [useful, descriptive commit messages](https://chris.beams.io/posts/git-commit/): Remember these are visible to all and should still make sense a few months ahead in time. While developing, you can keep using the GitLab issue you're working on as a place for discussion. [Refer to your commits](https://stackoverflow.com/questions/8910271/how-can-i-reference-a-commit-in-an-issue-comment-on-github) when discussing specific lines of code.
7. If you want to add a dependency on another library, or re-use code you found somewhere else, have a look at [these guidelines](#dependencies-and-reusing-code).

### Merging your changes with EP-BOLFI

8. Make sure that your code runs successfully. Ideally, implement tests.
9. Run `flake8` on your code to fix formatting issues ahead of time.
10. When you feel your code is finished, or at least warrants serious discussion, create a [merge request](https://docs.gitlab.com/ee/user/project/merge_requests/) (MR) on the [GitLab page of EP-BOLFI](https://gitlab.dlr.de/cec/ep-bolfi).
11. Once a MR has been created, it will be reviewed by any member of the group. Changes might be suggested which you can make by simply adding new commits to the branch. When everything's finished, someone with the right GitLab permissions will merge your changes into the EP-BOLFI main repository.

## Coding style guidelines

EP-BOLFI follows the [PEP8 recommendations](https://www.python.org/dev/peps/pep-0008/) for coding style. These are very common guidelines, and community tools have been developed to check how well projects implement them.

### Flake8

We use [flake8](http://flake8.pycqa.org/en/latest/) to check our PEP8 adherence. To try this on your system, navigate to the ep_bolfi directory in a terminal and type:

```bash
flake8
```

### Documentation

The documentation is generated with [Sphinx](https://www.sphinx-doc.org/) from the source code. This happens automatically during the CI/CD pipeline, with the result being available through GitLab Pages.

Hence, please copy the structure of the in-code documentation for your own comments. It is known as [reStructuredText](https://peps.python.org/pep-0287/).

## Dependencies and reusing code

While it's a bad idea for developers to "reinvent the wheel", it's important for users to get a _reasonably_ sized download and an easy install. In addition, external libraries can sometimes cease to be supported, and when they contain bugs it might take a while before fixes become available as automatic downloads to EP-BOLFI users.
For these reasons, all dependencies in EP-BOLFI should be thought about carefully, and discussed on GitHub.

Direct inclusion of code from other packages is possible, as long as their license permits it and is compatible with ours, but again should be considered carefully and discussed in the group. Snippets from blogs and [stackoverflow](https://stackoverflow.com/) are often incompatible with other licences than [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/) and hence should be avoided. You should attribute (and document) any included code from other packages, by making a comment with a link in the source code.

## Building from source

Before pushing your changes, make sure that the version in version.txt is incremented and unique. The CI/CD pipeline will use this to upload a Release with the respective version in each of the kadi tools.

The following instructions are just here to inform you how to package the code yourself if you so desire.

### Build and install wheel from source (pip)

Install the build command and execute it:
```bash
pip install build
python3 -m build
```

The wheel file should be at dist/ep_bolfi-${VERSION}-py3-none-any.whl. Please do not commit these.

### Build conda package from wheel (conda)

First build the wheel from source via pip. Then install the necessary packages for building conda packages:
```bash
conda install build conda-build conda-verify
```

Then build:
```bash
conda-build .
```

The file you need for installing with conda install lies inside your Anaconda distribution, on Windows at conda-bld/win-64/ep_bolfi-${VERSION}-py39_0.tar.bz2.

### Building the .xml representations of the kadi tools

In order to generate the .xml files for the workflow editor from your version of the kadi_tools, you may use the following on Linux only:

```bash
cd ep_bolfi/kadi_tools
mkdir xml_representations
for file in ./*.py; do
if [ $file = "./__init__.py" ]; then
continue
fi
python $file --xmlhelp > xml_representations/${file:2:-3}.xml
done
```

On Windows, the files get the wrong encoding (UTF-16). If you know what this means, you may generate the .xml files on Windows and manually fix the encoding to be UTF-8.

Please note that, when developing, the version displayed by the workflow editor will always be VERSION, since the actual version is automatically inserted during the CI/CD pipeline.

In the case where spurious lines like "warning in ...: failed to import cython module: falling back to numpy" show up, these are due to an unfortunate design decision in GPy. Either delete them manually, or try installing GPy from source like so to improve performance as well:

```bash
git clone https://github.com/SheffieldML/GPy.git
cd GPy
pip install .
```

## Infrastructure

### GitLab

GitLab does some magic with particular filenames. In particular:

- The first page people see when they go to [our GitLab page](https://gitlab.dlr.de/cec/ep-bolfi) displays the contents of [README.md](README.md), which is written in the [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) format. Some guidelines can be found [here](https://help.github.com/articles/about-readmes/).
- This file, [CONTRIBUTING.md](CONTRIBUTING.md) is recognised as the contribution guidelines and a link is [automatically](https://github.com/blog/1184-contributing-guidelines) displayed when new issues or pull requests are created.

## Acknowledgements

This CONTRIBUTING.md file was adapted from the excellent [Pints GitHub repo](https://github.com/pints-team/pints).
