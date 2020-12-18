from pkg_resources import parse_version
from configparser import ConfigParser
import setuptools
import os

assert parse_version(setuptools.__version__) >= parse_version("36.2")

PATH_ROOT = os.path.dirname(__file__)


def load_requirements(
    path_dir=PATH_ROOT, file_name="requirements.txt", comment_char="#"
):
    with open(os.path.join(path_dir, file_name),
              "r", encoding="utf-8",
              errors="ignore") as file:
        lines = [ln.strip() for ln in file.readlines()]

    reqs = []
    for ln in lines:
        if comment_char in ln:  # filer all comments
            ln = ln[: ln.index(comment_char)].strip()
        if ln.startswith("http"):  # skip directly installed dependencies
            continue
        if ln:  # if requirement is not empty
            reqs.append(ln)
    return reqs


def load_long_description():
    text = open("README.md", encoding="utf-8", errors="ignore").read()
    # replace relative repository path to absolute link to the release
    # text = text.replace('](docs', f']({url}')
    # SVG images are not readable on PyPI, so replace them  with PNG
    text = text.replace(".svg", ".png")
    return text


# note: all settings are in settings.ini; edit there, not here
config = ConfigParser(delimiters=["="])
config.read("settings.ini")
cfg = config["DEFAULT"]

cfg_keys = "version description keywords author author_email".split()
expected = (
    cfg_keys
    + "lib_name user branch license status min_python audience language".split()
)
for o in expected:
    assert o in cfg, "missing expected setting: {}".format(o)
setup_cfg = {o: cfg[o] for o in cfg_keys}

licenses = {
    "mit": (
        "MIT License",
        "OSI Approved :: MIT License",
    ),
}
statuses = [
    "1 - Planning",
    "2 - Pre-Alpha",
    "3 - Alpha",
    "4 - Beta",
    "5 - Production/Stable",
    "6 - Mature",
    "7 - Inactive",
]
py_versions = "3.6 3.7 3.8".split()

lic = licenses[cfg["license"]]
min_python = cfg["min_python"]

setuptools.setup(
    name=cfg["lib_name"],
    license=lic[0],
    classifiers=[
        "Development Status :: " + statuses[int(cfg["status"])],
        "Intended Audience :: " + cfg["audience"].title(),
        "License :: " + lic[1],
        "Natural Language :: " + cfg["language"].title(),
    ]
    + [
        "Programming Language :: Python :: " + o
        for o in py_versions[py_versions.index(min_python):]
    ],
    url=cfg["git_url"],
    packages=setuptools.find_packages(exclude=["tests", "docs"]),
    include_package_data=True,
    install_requires=load_requirements(),
    dependency_links=cfg.get("dep_links", "").split(),
    python_requires=">=" + cfg["min_python"],
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    zip_safe=False,
    entry_points={"console_scripts": cfg.get("console_scripts", "").split()},
    **setup_cfg
)
