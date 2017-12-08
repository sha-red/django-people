import subprocess


try:
    git_describe = subprocess.check_output(['git', 'describe', '--tags'], universal_newlines=True, stderr=subprocess.DEVNULL).strip()
    # v0.2-69-g181f854
    if git_describe[0] in "vr":
        git_describe = git_describe[1:]
    parts = git_describe.split("-")
    VERSION = parts[0].split(".")[:3]
    VERSION += [0] * (3 - len(VERSION))
    git_version = parts[1:]

except subprocess.CalledProcessError:
    # Not yet tagged
    VERSION = [0, 0, 0]
    git_version = []
    try:
        git_version = (
            subprocess.check_output(['git', 'rev-list', '--count', 'HEAD'], universal_newlines=True).strip(),
            subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], universal_newlines=True).strip()
        )
    except subprocess.CalledProcessError:
        git_version = []


# 1.3.0-64-g1f9a30
__version__ = '-'.join(map(str, ['.'.join(map(str, VERSION)), *git_version]))
VERSION.extend(git_version)


default_app_config = 'people.apps.PeopleConfig'
