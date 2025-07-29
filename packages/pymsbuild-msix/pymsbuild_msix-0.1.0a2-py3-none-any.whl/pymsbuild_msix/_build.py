import os
import subprocess
import sys
import winreg
from pathlib import Path

def get_tools():
    sdk = os.getenv("WindowsSdkDir")
    if not sdk:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows Kits\Installed Roots",
            access=winreg.KEY_READ | winreg.KEY_WOW64_32KEY,
        ) as key:
            sdk, keytype = winreg.QueryValueEx(key, "KitsRoot10")

        if keytype != winreg.REG_SZ:
            print("Unexpected registry value for Windows Kits root.", file=sys.stderr)
            print("Try setting %WindowsSdkDir%", file=sys.stderr)
            sys.exit(1)

    sdk = Path(sdk)

    sdk_ver = os.getenv("WindowsSDKVersion", "10.*")

    bins = list((sdk / "bin").glob(sdk_ver))[-1] / "x64"
    if not bins.is_dir():
        print("Unable to locate Windows Kits binaries.", file=sys.stderr)
        sys.exit(2)

    tools = dict(
        makeappx=bins / "makeappx.exe",
        makepri=bins / "makepri.exe",
    )

    for name, tool in tools.items():
        if not tool.is_file():
            print("Unable to locate Windows Kit tool", name, "at", tool, file=sys.stderr)
            sys.exit(3)

    return tools


def do_build(bs):
    bs.finalize()
    bs.prepare_wheel_distinfo()
    bs.layout_wheel(statefile=False)

    name, version = bs.metadata["Name"], bs.metadata["Version"]
    bs.layout_metadata["msix_name"] = f"{name}-{version}.msix"
    bs.layout_metadata["msix_appinstaller_name"] = f"{name}.appinstaller"

    tools = get_tools()
    _run = subprocess.check_output if bs.quiet else subprocess.check_call

    root = bs.layout_dir / bs.package.name
    for i, f in enumerate(bs.package.findall("$ResourcesXml")):
        # TODO: Figure out how to actually make this work for multiple files
        if i > 0:
            bs.write("WARNING: Multiple resources.pri files are currently not supported.")
            bs.write("Skipping additional files.")
            break
        cmd = [
            tools["makepri"],
            "new", "/o", "/v",
            "/pr", root,
            "/cf", f.source,
            "/of", root / "resources.pri",
            "/mf", "appx"
        ]
        try:
            bs.log("Executing", cmd)
            _run(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as ex:
            if bs.quiet:
                try:
                    print(ex.stdout.decode("utf-16", "strict"))
                except UnicodeDecodeError:
                    print(ex.stdout.decode("oem", "replace"))
            sys.exit(1)

    if bs._perform_layout:
        # Running 'pack' will trigger our do_pack() call below
        bs.write_state("_pack_msix")
    else:
        return _pack(bs, bs.layout_dir.rglob(r"**\*"))


def do_pack(bs):
    return _pack(bs, bs.layout_files)


def _pack(bs, layout_files):
    tools = get_tools()
    _run = subprocess.check_output if bs.quiet else subprocess.check_call
    layout_files = list(layout_files)

    manifests = [f for f in layout_files if f.match("appxmanifest.xml")]
    if not manifests:
        bs.log("Failed to find an appxmanifest.xml in this project.")
        sys.exit(1)
    elif len(manifests) != 1:
        bs.log("Found multiple appxmanifests in this project. Only building", manifests[0])
    manifest = manifests[0]

    msix_name = (os.getenv("PYMSBUILD_MSIX_NAME")
        or bs.layout_metadata.get("msix_name")
        or bs.distinfo_name.rpartition(".")[0]
    )
    msix = bs.output_dir / msix_name
    if not msix.match("*.msix"):
        msix = msix.parent / f"{msix.name}.msix"
    msix.parent.mkdir(parents=True, exist_ok=True)

    map_file = bs.layout_dir / f"{msix.name}.map"
    map_file.parent.mkdir(parents=True, exist_ok=True)
    with open(map_file, "w", encoding="utf-8-sig") as mf:
        print("[Files]", file=mf)
        for f in layout_files:
            if not f.is_file():
                bs.log("Skipping", f, "because it does not exist or is not a file")
                continue
            try:
                rel = f.relative_to(manifest.parent)
            except ValueError:
                bs.log("Skipping", f, "because it is outsite the package")
                continue
            print(f'"{f}" "{rel}"', file=mf)
    cmd = [tools["makeappx"], "pack", "/o", "/f", map_file, "/p", msix]
    bs.log("Executing", cmd)
    bs.log("Map file", map_file, "contains:")
    bs.log(map_file.read_text("utf-8-sig"))
    try:
        _run(cmd)
    except subprocess.CalledProcessError as ex:
        if bs.quiet:
            print(ex.stdout.decode("oem", "replace"))
        sys.exit(1)

    bs.write("Wrote MSIX to", msix)
    return msix.name
