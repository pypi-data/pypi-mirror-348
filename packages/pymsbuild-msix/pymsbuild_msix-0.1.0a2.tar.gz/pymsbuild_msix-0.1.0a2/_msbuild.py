import os
from pymsbuild import *

METADATA = {
    "Metadata-Version": "2.2",
    "Name": "pymsbuild-msix",
    "Version": "0.0.1",
    "Author": "Steve Dower",
    "Author-email": "steve.dower@python.org",
    "Project-url": [
        "Homepage, https://github.com/zooba/pymsbuild-msix",
        "Report bug, https://github.com/zooba/pymsbuild-msix/issues",
    ],
    "Summary": "A pymsbuild extension for producing MSIX packages.",
    "Description": File("README.md"),
    "Description-Content-Type": "text/markdown",
    "Keywords": "build,pep-517,msbuild,packaging,msix,Windows",
    "Classifier": [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Compilers",
        "Topic :: Utilities",
    ],
    "Requires-Dist": [
        "pymsbuild>=1.2.2a1",
        "entrypoints",
    ],
    "WheelTag": "py3-none-any",
}


PACKAGE = Package(
    "",
    Package("pymsbuild_msix",
        PyFile("pymsbuild_msix/*.py"),
        #File("pymsbuild_msix/targets/*", name="targets/*"),
    ),
    File("entry_points.txt", IncludeInDistinfo=True),
)


def init_METADATA():
    version = os.getenv("BUILD_BUILDNUMBER")
    ghref = os.getenv("GITHUB_REF")
    if ghref:
        version = ghref.rpartition("/")[2]
    if version:
        METADATA["Version"] = version


def update_file(file, content):
    if not file.is_file() or file.read_text("utf-8").strip() != content.strip():
        file.parent.mkdir(parents=True, exist_ok=True)
        with file.open("w", encoding="utf-8") as f:
            print(content, file=f)


def init_PACKAGE(tag=None):
    if tag is None:
        return
    tmpdir = get_current_build_state().temp_dir
    # GENERATE _version MODULE
    ver_py = tmpdir / "_version.py"
    update_file(ver_py, f"__version__ = {METADATA['Version']!r}")
    PACKAGE.find("pymsbuild_msix").members.append(PyFile(ver_py))
