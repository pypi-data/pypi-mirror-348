from importlib.metadata import version
from markdown import markdown
from os import remove, system, makedirs
from packaging.version import parse
from pathlib import Path
from requests import get, Timeout, ConnectionError
from site import getsitepackages
from time import sleep
from webbrowser import open as op

from toml import load, dump

global_config_path = Path.home() / "appdata" / "xystudio" / "pyplus" / "config.toml"
local_config_path = Path.cwd() / ".xystudio" / "pyplus" / "config.toml"
global_config = {}
local_config = {}
union_config = {}

LOCAL = "local"
GLOBAL = "global"

ALL = "all"
NEW = "news"
WILL = "will"

makedirs(global_config_path.parent, exist_ok=True)

if not global_config_path.exists():
    global_config_path.touch()
else:
    with open(global_config_path, 'r', encoding="utf-8") as f:
        global_config = load(f)

if global_config.get("library", {"autoCreateLocalConfig" : True}).get("autoCreateLocalConfig", True):
    makedirs(local_config_path.parent, exist_ok=True)
    if not(local_config_path.exists()):
        local_config_path.touch()

try:
    with open(local_config_path, 'r', encoding="utf-8") as f:
        local_config = load(f)
except FileNotFoundError:
    pass

first_used_config = global_config.get("library", {"firstUsedConfig" : "local"}).get('firstUsedConfig', "local")

if first_used_config == "local":
    union_config = global_config | local_config
else:
    union_config = local_config | global_config

with open(getsitepackages()[1] + "\\pyplus\\data\\config\\update.toml", "r", encoding="utf-8") as f:
     updates = load(f)

with open(
    getsitepackages()[1] + "\\pyplus\\data\\config\\config_help.toml",
    "r",
    encoding="utf-8",
) as f:
    config_help = load(f)

with open(
    getsitepackages()[1] + "\\pyplus\\data\\config\\alias.toml", "r", encoding="utf-8"
) as f:
    lang_alias = load(f)

with open(
    getsitepackages()[1] + "\\pyplus\\data\\config\\doc_help.toml",
    "r",
    encoding="utf-8",
) as f:
    doc_help = load(f)


def get_update(namespace, version):
    """get the version update doc."""
    try:
        open_dict = updates["release"][namespace]["update_info"]
    except KeyError:
        raise ValueError("This namespace not found.")

    if version == ALL:
        out_obj = open_dict
    elif version == NEW:
        out_obj = open_dict.get(
            updates["release"][namespace]["version"],
            "This version is not found. Maybe it is not recorded.",
        )
    elif version == WILL:
        out_obj = open_dict.get(
            WILL, "This version is not found. Maybe it is not recorded."
        )
    else:
        out_obj = open_dict.get(
            str(version), "This version is not found. Maybe it is not recorded."
        )

    print(out_obj)
    return out_obj


def get_version_update_time(namespace, version):
    """Get the version update time."""
    try:
        open_dict = updates["release"][namespace]["update_time"]
    except KeyError:
        raise ValueError("This namespace not found.")

    if version == ALL:
        out_obj = open_dict
    elif version == NEW:
        out_obj = open_dict.get(
            updates["release"][namespace]["version"],
            "This version is not found. Maybe it is not recorded.",
        )
    elif version == WILL:
        raise ValueError("`get_version_update_time` cannot get will update time.")
    else:
        out_obj = open_dict.get(
            str(version), "This version is not found. Maybe it is not recorded."
        )

    print(out_obj)
    return out_obj


def get_version(namespace):
    """Get the version."""
    return updates["release"][namespace]["version"]


def get_pre_version():
    """Get the pre version."""
    return updates["pre-release"]["version"]


def get_pre_update(version):
    """Get the pre-release version update doc."""
    try:
        open_dict = updates["pre-release"]["update_info"]
    except KeyError:
        raise ValueError("This namespace not found.")

    if version == ALL:
        out_obj = open_dict
    elif version == NEW:
        out_obj = open_dict.get(
            updates["pre-release"]["version"],
            "This version is not found. Maybe it is not recorded.",
        )
    elif version == WILL:
        out_obj = open_dict.get(
            WILL, "This version is not found. Maybe it is not recorded."
        )
    else:
        out_obj = open_dict.get(
            str(version), "This version is not found. Maybe it is not recorded."
        )

    print(out_obj)
    return out_obj


def get_pre_version_update_time(version):
    """Get the pre-release version update time."""
    try:
        open_dict = updates["pre-release"]["update_time"]
    except KeyError:
        raise ValueError("This namespace not found.")

    if version == NEW:
        out_obj = open_dict
    elif version == NEW:
        out_obj = open_dict.get(
            updates["pre-release"]["version"],
            "This version is not found. Maybe it is not recorded.",
        )
    elif version == WILL:
        raise ValueError("`get_version_update_time` cannot get will update time.")
    else:
        out_obj = open_dict.get(
            str(version), "This version is not found. Maybe it is not recorded."
        )
    print(out_obj)
    return out_obj


def open_doc(doc_name, lang="en"):
    doc_html_path = Path.cwd() / ".xystudio" / "pyplus" / "cache" / "doc.html"
    doc_name = doc_name.lower()

    for key, values in lang_alias.items():
        if lang.lower() in values:
            lang = key
    lang = lang.lower()

    makedirs(doc_html_path.parent, exist_ok=True)

    if doc_name == "index":
        op(getsitepackages()[1] + f"\\pyplus\\data\\docs\\web\\{lang}\\index.html")
    else:
        with open(
            getsitepackages()[1]
            + f"\\pyplus\\data\\docs\\markdown\\{lang}\\{doc_name}.md",
            "r",
            encoding="utf-8",
        ) as f:
            html = markdown(f.read())

        with open(doc_html_path, "w", encoding="utf-8") as f:
            f.write(html)

        op(doc_html_path)
        sleep(1)
        remove(doc_html_path)


def get_doc_help(doc_name=ALL):
    print()
    if doc_name == ALL:
        for doc_namespace, doc_des in doc_help.items():
            print(f"{doc_namespace} : {doc_des}")
    else:
        print(f"{doc_name}: {doc_help.get(doc_name, 'Not found.')}")


def get_alias(lang=ALL):
    print()
    match_alias = None
    for k, v in lang_alias.items():
        if lang.lower() in v:
            match_alias = k
            break

    if lang == ALL:
        for k, v in lang_alias.items():
            print(f"alias {k} -> {', '.join(v)}")
    elif match_alias is not None:
        print(f"alias {match_alias} -> {lang}")
    else:
        print(f"alias {lang} -> {', '.join(lang_alias.get(lang, ["Not found."]))}")


def config(config_name, value, config_type=first_used_config):
    global local_config, global_config, union_config

    if config_type == LOCAL:
        makedirs(local_config_path.parent, exist_ok=True)
        if not(local_config_path.exists()):
            local_config_path.touch()

        config_split = config_name.split(".", 1)
        config_char_1 = config_split[0]
        try:
            config_char_2 = config_split[1]
        except IndexError:
            raise ValueError("config name must use 'a.b'.")

        with open(local_config_path, "w+", encoding="utf-8") as f:
            config = load(f) | {config_char_1 : {config_char_2 : value}}
            local_config |= config
            dump(config, f)
    elif config_type == GLOBAL:
        config_split = config_name.split(".")
        config_char_1 = config_split[0]
        try:
            config_char_2 = config_split[1]
        except IndexError:
            raise ValueError("config name must use 'a.b'.")

        with open(global_config_path, "w+", encoding="utf-8") as f:
            config = load(f) | {config_char_1 : {config_char_2 : value}}
            global_config |= config
            dump(config, f)
    else:
        raise ValueError("This config type not found.")
    union_config |= config


def get_config(config_name):
    try:
        config_split = config_name.split(".")
        config_char_1 = config_split[0]
        try:
            config_char_2 = config_split[1]
            return union_config[config_char_1][config_char_2]
        except IndexError:
            raise ValueError("config name must use two texts, example : 'a.b'.")
    except KeyError:
        return None

def get_config_help(config_type = ALL):
    if config_type == ALL:
        for config_t,config_docs in config_help.items():
            print("*" * 22 + "-" * 8 + config_t + "-" * 8 + "*" * 22)
            for doc_name, doc_des in config_docs.items():
                print()
                print(f"{doc_name} : {doc_des}")
            print(f"\n{'-'*30}\n")
        print(
            "\nWhen you set config,you need use 'pyplus config set local name.config value'"
        )
    else:
        print("*" * 22 + "-" * 8 + config_type + "- " * 8 + "*" * 22)
        try:
            for doc_name, doc_des in config_help[config_type].items():
                print(f"{doc_name} : {doc_des}")
        except KeyError:
            print("This document is not found.")
        else:
            print(
                "When you set config,you need use 'pyplus config set local name.config value'"
            )


def open_doc(doc_name, lang="en"):
    doc_html_path = Path.cwd() / ".xystudio" / "pyplus" / "cache" / "doc.html"
    doc_name = doc_name.lower()

    for key, values in lang_alias.items():
        if lang.lower() in values:
            lang = key
    lang = lang.lower()

    makedirs(doc_html_path.parent, exist_ok=True)

    if doc_name == "index":
        op(getsitepackages()[1] + f"\\pyplus\\data\\docs\\web\\{lang}\\index.html")
    else:
        with open(
            getsitepackages()[1]
            + f"\\pyplus\\data\\docs\\markdown\\{lang}\\{doc_name}.md",
            "r",
            encoding="utf-8",
        ) as f:
            html = markdown(f.read())

        with open(doc_html_path, "w", encoding="utf-8") as f:
            f.write(html)

        op(doc_html_path)
        sleep(1)
        remove(doc_html_path)


def remove_config(config_name, config_type=first_used_config):
    global local_config, global_config, union_config

    if config_type == LOCAL:
        del local_config[config_name]
        with open(local_config_path, "w", encoding="utf-8") as f:
            dump(local_config, f)
    elif config_type == GLOBAL:
        del global_config[config_name]
        with open(global_config_path, "w", encoding="utf-8") as f:
            dump(global_config, f)
    else:
        raise ValueError("This config type not found.")

    del union_config[config_name]
    return union_config

def xml_to_json(xmlFile, jsonFile):
    from xmltodict import parse
    from json import dumps

    with open(xmlFile, "r", encoding="utf-8") as f:
        json = dumps(parse(f.read()), indent=4)

    with open(jsonFile, "w", encoding="u8") as f:
        f.writelines(json)

    return "".join(json)


def csv_to_tsv(csvFile, tsvFile):
    with open(csvFile, "r", encoding="utf-8") as f:
        csv = f.readlines()

    o = []
    for i in csv:
        o.append(i.replace(", ", "\t"))

    with open(tsvFile, "w", encoding="utf-8") as f:
        f.writelines(o)
    return o


def tsv_to_csv(tsvFile, csvFile):
    with open(tsvFile, "r", encoding="utf-8") as f:
        csv = f.readlines()
    o = []

    for i in csv:
        o.append(i.replace("\t", ", "))
    with open(csvFile, "w", encoding="utf-8") as f:
        f.writelines(o)
    return o


def csv_to_json(csvFile, jsonFile):
    from json import dump

    with open(csvFile, "r", encoding="utf-8") as f:
        csv = f.read()

    with open(jsonFile, "w", encoding="utf-8") as f:
        dump(csv.split(","))


def json_to_xml(jsonFile, xmlFile):
    from json import load
    from xml.etree.ElementTree import Element, tostring

    with open(jsonFile, "r", encoding="utf-8") as f:
        json_obj = load(f)

    if isinstance(json_obj, dict):
        element = Element(json_obj.get("tag", "root"))
        for key, value in json_obj.items():
            if key == "tag":
                continue  # Skip the 'tag' key
            sub_element = Element(key)
            sub_element.text = str(value)
            element.append(sub_element)
    elif isinstance(json_obj, list):
        element = Element("root")
        for item in json_obj:
            sub_element = Element("item")
            if isinstance(item, dict):
                for k, v in item.items():
                    sub_sub_element = Element(k)
                    sub_sub_element.text = str(v)
                    sub_element.append(sub_sub_element)
            else:
                sub_element.text = str(item)
            element.append(sub_element)

    o = (
        tostring(element, encoding="utf-8", method="xml", xml_declaration=True).decode(
            "utf-8"
        )
    ).splitlines()[1]
    with open(xmlFile, "w", encoding="utf-8") as f:
        f.write(o)
    return o


def pickle_to_json(pickleFile, jsonFile):
    from json import dump
    from pickle import load

    with open(pickleFile, "rb", encoding="utf-8") as f1, open(
        jsonFile, "w", encoding="utf-8"
    ) as f2:
        dump(load(f1), f2)


def json_to_pickle(jsonFile, pickleFile):
    from pickle import dump
    from json import load

    with open(pickleFile, "wb", encoding="utf-8") as f2, open(
        jsonFile, "r", encoding="utf-8"
    ) as f1:
        dump(load(f1), f2)


def yaml_to_json(yamlFile, jsonFile):
    from yaml import load
    from json import dump

    with open(yamlFile, "r", encoding="utf-8") as f1, open(
        jsonFile, "w", encoding="utf-8"
    ) as f2:
        dump(load(f1), f2)


def json_to_yaml(jsonFile, yamlFile):
    from json import load
    from yaml import dump

    with open(jsonFile, "r", encoding="utf-8") as f1, open(
        yamlFile, "w", encoding="utf-8"
    ) as f2:
        dump(load(f1), f2, allow_unicode=True)


def toml_to_json(tomlFile, jsonFile):
    from toml import load
    from json import dump

    with open(tomlFile, "r", encoding="utf-8") as f1, open(
        jsonFile, "w", encoding="utf-8"
    ) as f2:
        dump(load(f1), f2)


def json_to_toml(jsonFile, tomlFile):
    from json import load
    from toml import dump

    with open(jsonFile, "r", encoding="utf-8") as f1, open(
        tomlFile, "w", encoding="utf-8"
    ) as f2:
        dump(load(f1), f2, allow_unicode=True)


def xml_to_jsons(xml):
    from xmltodict import parse
    from json import dumps

    json = dumps(parse(xml), indent=4)

    return "".join(json)


def csv_to_tsvs(csv):
    o = []

    for i in csv:
        o.append(i.replace(", ", "\t"))

    return o


def tsv_to_csvs(tsv):
    o = []

    for i in tsv:
        o.append(i.replace("\t", ", "))

    return o


def csv_to_jsons(csv):
    return "".join(csv.split(","))


def json_to_xmls(json):
    from json import loads
    from xml.etree.ElementTree import Element, tostring

    json_obj = loads(json)

    if isinstance(json_obj, dict):
        element = Element(json_obj.get("tag", "root"))
        for key, value in json_obj.items():
            if key == "tag":
                continue  # Skip the 'tag' key
            sub_element = Element(key)
            sub_element.text = str(value)
            element.append(sub_element)
    elif isinstance(json_obj, list):
        element = Element("root")
        for item in json_obj:
            sub_element = Element("item")
            if isinstance(item, dict):
                for k, v in item.items():
                    sub_sub_element = Element(k)
                    sub_sub_element.text = str(v)
                    sub_element.append(sub_sub_element)
            else:
                sub_element.text = str(item)
            element.append(sub_element)

    o = (
        tostring(element, encoding="utf-8", method="xml", xml_declaration=True).decode(
            "utf-8"
        )
    ).splitlines()[1]

    return o


def yaml_to_jsons(yaml):
    from yaml import load
    from json import dumps
    from os import remove

    with open("convert_cache", "w", encoding="utf-8") as f:
        f.write(yaml)

    with open("convert_cache", "r", encoding="utf-8") as f:
        return dumps(load(f))

    remove("convert_cache")


def json_to_yamls(json):
    from json import load
    from yaml import dump
    from os import remove

    with open("convert_cache", "w", encoding="utf-8") as f:
        f.write(json)

    with open("convert_cache", "r", encoding="utf-8") as f:
        return dump(load(f))

    remove("convert_cache")


def toml_to_jsons(toml):
    from toml import load
    from json import dumps
    from os import remove

    with open("convert_cache", "w", encoding="utf-8") as f:
        f.write(toml)

    with open("convert_cache", "r", encoding="utf-8") as f:
        return dumps(load(f))

    remove("convert_cache")


def json_to_tomls(jsonFile, tomlFile):
    from json import load
    from toml import dump

    with open(jsonFile, "r", encoding="utf-8") as f1, open(
        tomlFile, "w", encoding="utf-8"
    ) as f2:
        dump(load(f1), f2, allow_unicode=True)


def json_to_tomls(toml):
    from json import load
    from toml import dumps
    from os import remove

    with open("convert_cache", "w", encoding="utf-8") as f:
        f.write(toml)

    with open("convert_cache", "r", encoding="utf-8") as f:
        return dumps(load(f))

    remove("convert_cache")

def fetch_url(main_url, backup_urls = [], retries = 3, timeout = 5, **kwargs):
    all_urls = [main_url] + backup_urls

    for idx, url in enumerate(all_urls):
        for attempt in range(retries + 1):
            try:
                response = get(url, timeout=timeout, **kwargs)
                response.raise_for_status()
                return response
            except (Timeout, ConnectionError) as e:            
                if attempt == retries:
                    if url != all_urls[-1]:
                        pass
                    break
    raise TimeoutError

def _get_latest_version(
    package_name, url = "https://pypi.org/pypi/%P/json", extra_urls = [], retries = 3, timeout = 5, include_prerelease: bool = False, **kwargs
):
    url = url.replace("%P", package_name)
    extra_urls = [i.replace("%P", package_name) for i in extra_urls]
    
    response = fetch_url(url, extra_urls, retries, timeout, **kwargs)

    data = response.json()
    all_versions = list(data["releases"].keys())  # 获取所有版本列表

    # 解析并过滤版本
    valid_versions = []
    for v in all_versions:
        version = parse(v)
        if not include_prerelease and version.is_prerelease:
            continue  # 跳过预发布版本
        valid_versions.append(version)

    if not valid_versions:
        return None
    latest = max(valid_versions)
    return str(latest)


def check_update(
    package_name,
    include_prerelease = False,
    auto_update = False,
    first_url = "https://pypi.org/pypi/%P/json",
    extra_urls = [], 
    retry_times = 3, 
    timeout = 10, 
    **kwargs
):
    installed_version = version(package_name)
    latest_version = _get_latest_version(
        package_name, first_url, extra_urls, retry_times, timeout, include_prerelease, **kwargs
    )
    if latest_version and installed_version != latest_version:
        if include_prerelease:
            print(
                f"New pre-release version available: {installed_version} → {latest_version}"
            )
        else:
            print(f"New version available: {installed_version} → {latest_version}")
        if auto_update:
            print("Auto-updating...")
            if include_prerelease:
                system(f"pip install --upgrade --pre {package_name}")
            else:
                system(f"pip install --upgrade {package_name}")
            print("Update complete.")
    else:
        print("Already up to date.")


__version__ = get_version("main")


def shell():
    print("starting shell...")

    from pyplus import tools, science
    import decorators

    from pyplus.tools import (
        colors,
        dec,
        database_convert,
        formula,
        geohash,
        # password,
        permission,
        pydebugger,
        stack,
        tag,
        type,
        update,
        web,
        variables,
        pycppio,
        wait,
        latex,
        geohash
    )

    # from . import () # deprecated moudle

    print(f'python-plus-tools {get_version("main")} ({get_pre_version()})')
    print("type exit to exit the shell.")

    all_code = []
    while True:
        try:
            code = input("pyplus >>> ")
            if code == "exit" or code == "quit" or code == "exit()" or code == "quit()":
                break
            exec(code)
            all_code.append(code)
        except KeyboardInterrupt:
            print("^C\nKeyboardInterrupt")
            break
        except EOFError:
            break
        except Exception as e:
            print(e.with_traceback(None))


def main() -> None:
    import argparse

    class globalAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            self.handle_output(parser, namespace, values)

        @staticmethod
        def handle_output(parser, namespace, values):
            setattr(namespace, "_global", values)

    class allAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            self.handle_output(parser, namespace, values)

        @staticmethod
        def handle_output(parser, namespace, values):
            setattr(namespace, "_all", values)

    class localAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            self.handle_output(parser, namespace, values)

        @staticmethod
        def handle_output(parser, namespace, values):
            setattr(namespace, "_local", values)

    parser = argparse.ArgumentParser(description="imgfit commands")
    subparsers = parser.add_subparsers(dest="command", required=False)

    config_cmd = subparsers.add_parser(
        "config",
        help="Set the config.Usage 'pyplus config get' to get all config.",
    )
    config_namespace = config_cmd.add_subparsers(dest="config_command", required=True)
    set_cmd = config_namespace.add_parser("set", help="Set the config")
    set_namespace = set_cmd.add_subparsers(dest="set_namespace", required=True)
    local_config_cmd = set_namespace.add_parser(
        "local",
        help="Config file only in your project.Local config in './.xystudio/pyplus/config.toml'",
    )
    global_config_cmd = set_namespace.add_parser(
        "global",
        help="Config file in all project.Global config in 'Users/Appdata/roaming/xystudio/pyplus/config.toml'",
    )

    local_config_cmd.add_argument("setting", help="Config setting.")
    local_config_cmd.add_argument("value", help="Config value.")

    global_config_cmd.add_argument("setting", help="Config setting.")
    global_config_cmd.add_argument("value", help="Config value.")

    get_conf = config_namespace.add_parser("get", help="Get the config.")
    get_conf.add_argument(
        "-l",
        "--local",
        action=localAction,
        nargs="?",
        help="Get the local config in your project.Local config in './.xystudio/pyplus/config.toml'",
    )
    get_conf.add_argument(
        "-g",
        "--global",
        action=globalAction,
        nargs="?",
        help="Output the global config.",
    )
    get_conf.add_argument(
        "-a", "--all", nargs="?", action=allAction, help="Output all the config."
    )

    config_namespace.add_parser("get_help", help="Get the config help.").add_argument(
        "-d",
        "--document_description",
        nargs="?",
        help="get one document description.",
        default=ALL,
    )

    remove_namespace = config_namespace.add_parser("remove", help="Remove the config").add_subparsers(dest="remove_namespace", required=True)
    local_config_cmd = remove_namespace.add_parser(
        "local",
        help="Config file only in your project.Local config in './.xystudio/pyplus/config.toml'",
    )
    global_config_cmd = remove_namespace.add_parser(
        "global",
        help="Config file in all project.Global config in 'Users/Appdata/roaming/xystudio/pyplus/config.toml'",
    )

    local_config_cmd.add_argument("setting", help="Config setting.")
    global_config_cmd.add_argument("setting", help="Config setting.")
    doc_namespace = subparsers.add_parser("document", help="Document name.").add_subparsers(dest="doc_namespace", required=True)
    open_doc_command = doc_namespace.add_parser("open", help="Open the document.")
    open_doc_command.add_argument("doc_name", help="Document name.")
    open_doc_command.add_argument(
        "-l", "--lang", help="Document language.", nargs="?", default="en"
    )

    doc_namespace.add_parser(
        "get_help", help="Get the document help."
    ).add_argument(
        "-d",
        "--document_description",
        nargs="?",
        help="get one document description.",
        default=ALL,
    )

    update_namespace = subparsers.add_parser("update", help="Get the update.").add_subparsers(
        dest="update_namespace", required=True
    )

    pre_update_namespace = update_namespace.add_parser("pre", help="Get the pre-release update.").add_subparsers(dest="pre", required=True)

    release_update_namespace = update_namespace.add_parser(
        "release", help="Get the release update."
    ).add_subparsers(
        dest="release_namespace", required=True
    )

    release_update_namespace.add_parser(
        "version", help="Get a release version."
    ).add_argument("namespace", help="A release version namespace.")

    news = release_update_namespace.add_parser("news", help="Get the news.")
    news.add_argument("namespace", help="A release version namespace.", nargs="?")
    news.add_argument("version", help="release version.", nargs="?")

    time = release_update_namespace.add_parser("time", help="Get the time.")
    time.add_argument("namespace", help="A release version namespace.", nargs="?")
    time.add_argument("version", help="release version.", nargs="?")

    pre_update_namespace.add_parser("version", help="Get a pre-release version.")

    pre_update_namespace.add_parser("news", help="Get the pre-release news.").add_argument("version", help="pre-release version.", nargs="?")

    pre_update_namespace.add_parser("time", help="Get the pre-release time.").add_argument("version", help="pre-release version.", nargs="?")

    subparsers.add_parser("shell", help="run pyplus code.")

    parser.add_argument("-v", "--version", help="Get the version.", action="store_true")

    get_alias_command = subparsers.add_parser("get_ailas", help="Get the alias.")

    get_alias_command.add_argument(
        "-l", "--lang", help="Document language.", nargs="?", default=ALL
    )

    check_namespace = subparsers.add_parser(
        "version",
        help="update & check pyplus.",
    ).add_subparsers(dest="check_command", required=True)

    backup_namespace = subparsers.add_parser(
        "backup",
        help="backup your project.",
    ).add_subparsers(dest="backup_command", required=True)

    args = parser.parse_args()

    if args.command == "config":
        if args.config_command == "set":
            if args.value.lower() == "true":
                value = True
            elif args.value.lower() == "false":
                value = False
            else:
                value = args.value
            print("Run code again to set the config.")
            config(args.setting, value, args.set_namespace)
        elif args.config_command == "get_help":
            get_config_help(args.document_description)
        elif args.config_command == "get":
            if hasattr(args, "_local"):
                print(local_config)
            if hasattr(args, "_global"):
                print(global_config)
            if hasattr(args, "_all"):
                print(union_config)
        elif args.config_command == "remove":
            remove_config(args.setting, args.remove_namespace)
    elif args.version:
        print("Version : pyplus pre:", get_pre_version())
        print("Version : pyplus :", get_version("main"))
    elif args.command == "document":
        if args.doc_namespace == "open":
            open_doc(args.doc_name, args.lang)
        elif args.doc_namespace == "get_help":
            get_doc_help(args.document_description)
    elif args.command == "update":
        if args.update_namespace == "release":
            if args.release_namespace == "version":
                print(get_version(args.namespace))
            elif args.release_namespace == "news":
                print(get_update(args.namespace, args.version))
            elif args.release_namespace == "time":
                print(get_version_update_time(args.namespace, args.version))
        elif args.update_namespace == "pre":
            if args.pre == "version":
                print(get_pre_version())
            elif args.pre == "news":
                print(get_pre_update(args.version))
            elif args.pre == "time":
                print(get_pre_version_update_time(args.version))
    elif args.command == "shell":
        shell()
    elif args.command == "get_ailas":
        get_alias(args.lang)
    elif args.command == "version":
        print("This command is not implemented yet.")
    elif args.command == "backup":
        print("This command is not implemented yet.")
    else:
        print("Command not found.Press 'pyplus -h' to get help.")


if __name__ == "__main__":
    check_update("numpy", first_url="https://mirrors.tuna.tsinghua.edu.cn/pypi/web/json/%P", include_prerelease=True, timeout=5)
    main()