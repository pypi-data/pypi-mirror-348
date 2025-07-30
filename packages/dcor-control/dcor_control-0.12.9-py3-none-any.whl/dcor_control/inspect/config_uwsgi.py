import logging

from dcor_shared.paths import get_uwsgi_config_path

from .common import ask


logger = logging.getLogger(__name__)


def check_uwsgi(harakiri, autocorrect=False):
    """Set harakiri timeout of uwsgi (important for data upload)

    Parameters
    ----------
    harakiri: int
        uwsgi timeout in minutes
    """
    did_something = 0
    path_uwsgi = get_uwsgi_config_path()
    if path_uwsgi.exists():
        with open(path_uwsgi) as fd:
            lines = fd.readlines()
        for ii, line in enumerate(lines):
            data = line.split("=", 1)
            if len(data) < 2:
                continue
            else:
                key, value = data
                key = key.strip()
            if key == "harakiri":
                value = int(value)
                if value != harakiri:
                    if autocorrect:
                        change = True
                        print("Setting UWSGI harakiri to "
                              "{} min".format(harakiri))
                    else:
                        change = ask(
                            "UWSGI timeout should be '{}' min".format(harakiri)
                            + ", but is '{}' min".format(value))
                    if change:
                        did_something += 1
                        lines[ii] = line.replace(str(value), str(harakiri))
                        with open(path_uwsgi, "w") as fd:
                            fd.writelines(lines)
    else:
        logger.error(f"UWSGI configuration file '{path_uwsgi}' not found. "
                     f"Not checking UWSGI configuration.")

    return did_something
