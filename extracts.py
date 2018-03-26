#!/usr/bin/env python
import json
import os
import re
import subprocess
import time
import urllib.request
import zipfile
from pexpect import pxssh
import distro

from celery import shared_task

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CTAFramework.settings")
from django import setup

setup()

## Project import
from apps.Products.models import Argument, Source, Command


@shared_task()
def run_extract(config):
    """
    run_extract(config)

    Main function that gets configuration to run a given extract:
        2       -    M-extract
        3       -    P-Extract
        3 or 4  -    R-Extract
    """
    category = int(config.get('category'))
    if category is 2:
        # Extract Manpages
        m = MExtract(api_config=config)
        m.run()

    elif category is 3:
        # Extract Product Commands
        p = PExtract(config)
        p.run()

    elif category in (4, 5):
        # Extract Robot
        r = RExtract(config)
        r.run_r_extract()


class MExtract:
    """
    MExtract    -   Manpages Extract

    Class created to extract information for man pages, designed to get the parameters of commands
    """
    # TODO: It is a little bit confusing of what p_config[0] store, it seems like there is a list
    # of commands in a multiline string _split_list_of_commands, but in _ssh_connect seems like
    # it is a command that would be sent into a server to get the list of commands in the
    # multiline string format, so the TODO is verify if this information is correct or if there
    # is an error in the script.
    def __init__(self, sections_list=None, p_config=None, api_config=None):
        """
        __init__(self, sections_list=None, p_config=None, api_config=None)

        Initialization of MExtract:
            sections_list - list of sections of man pages information
            p_config      - list of configuration options it should contains the regular expression
                            in case user wants to extract man pages info with an especific format,
                            p_config is stored with next format:
                                [commands, arguments_re]
                                    where commands is a multiline string of commands as a list
                                    or a command to get commands in case user wants to get commands
                                    remotely (e.g., ls /<path_of_bin>/)
                                    arguments_re is a regular expression
                            Note: p_config is just used when PExtract but can be used for other
                                  linux distros that have a different Man pages format.
            api_config    - Dictionary that have connection data in case user wants to extract
                            information remotely, the keys are:
                                "host"
                                "username"
                                "password"
                                "port"
        """
        self.default_sections_list = [
            'NAME',
            'DESCRIPTION',
            'SYNOPSIS',
            'OPTIONS',
            'SEE ALSO'
        ]
        self.sections_list = self.default_sections_list if sections_list is None else sections_list
        self.p_config = p_config
        self.api_config = api_config
        self.initial_time = time.time()

    def _split_list_of_commands(self):
        """
        _split_list_of_commands(self)

        Section that use regular expression to split the list of commands
        """
        self.sections_re = re.compile('(^[A-Z]+\s*[A-Z]*\s*[A-Z]*\n)', flags=re.M)
        self.sp_arguments_re = re.compile(
            "( {2}-\w+, --\w+[ =]| {2}-\w+[ =]|"
            " {2}--\w+[ =]|"
            " {2}--\w+-\w+[ =]|"
            " {2}-\w+, --\w+-\w+[ =])(?=[<\w])",
            flags=re.M
        )
        if self.p_config is None:
            # Run this in case not a regular expression provided, get commands using compgen
            compgen = '/bin/bash -c "compgen -c"'
            commands = subprocess.getoutput(compgen)
            self.list_of_commands = commands.splitlines()
            # Generating reular expression for generic linux distros
            self.arguments_re = re.compile("( {2}-\w+, --\w+[ \n=]| {2}-\w+[ \n=]| {2}--\w+[ \n=]|"
                                           " {2}--\w+-\w+[ \n=]|"
                                           " {2}-\w+, --\w+-\w+[ \n=])(?=[ <]*)",
                                           flags=re.M
                                           )
            self.source = self._getSource(category=2)
        else:
            # Run this in case a non common commands wants to be extracted
            commands = self.p_config[0]
            self.list_of_commands = commands.splitlines()
            if self.p_config[1]:
                self.arguments_re = self.p_config[1]
            else:
                self.arguments_re = re.compile(
                    "( {2}-\w+, --\w+[ \n=]| {2}-\w+[ \n=]|"
                    " {2}--\w+[ \n=]| {2}--\w+-\w+[ \n=]|"
                    " {2}-\w+, --\w+-\w+[ \n=])(?=[ <]*)",
                    flags=re.M
                )
            self.source = self._getSource(category=3)

    def _ssh_regex(self):
        """
        _ssh_regex(self) -> <string_to_get_commands>

        Is used to setup the way that commands will be get remotely

        returns a string for get commands
        """
        self.sections_re = re.compile('(^[A-Z]+\s*[A-Z]*\s*[A-Z]*\n)', flags=re.M)
        self.sp_arguments_re = re.compile(
            "( {2}-\w+, --\w+[ =]| {2}-\w+[ =]|"
            " {2}--\w+[ =]|"
            " {2}--\w+-\w+[ =]|"
            " {2}-\w+, --\w+-\w+[ =])(?=[<\w])",
            flags=re.M
        )
        if self.p_config is None:
            # If not config, we suppose to get commands using standard linux way
            commands = '/bin/bash -c "compgen -c"'
            self.arguments_re = re.compile("( {2}-\w+, --\w+[ \n=]| {2}-\w+[ \n=]| {2}--\w+[ \n=]|"
                                           " {2}--\w+-\w+[ \n=]|"
                                           " {2}-\w+, --\w+-\w+[ \n=])(?=[ <]*)",
                                           flags=re.M
                                           )
            self.source = self._getSource(category=2)
        else:
            # If config, we need to setup a command that returns the list of commands in a multiline string
            commands = self.p_config[0]
            if self.p_config[1]:
                self.arguments_re = self.p_config[1]
            else:
                self.arguments_re = re.compile(
                    "( {2}-\w+, --\w+[ \n=]| {2}-\w+[ \n=]|"
                    " {2}--\w+[ \n=]| {2}--\w+-\w+[ \n=]|"
                    " {2}-\w+, --\w+-\w+[ \n=])(?=[ <]*)",
                    flags=re.M
                )
            self.source = self._getSource(category=3)

        return commands

    def run(self):
        """
        run(self)

        Launchs _run_with_ssh() or _run_with_default() depending of <api_config> configuration
        """
        if self.api_config.get('host'):
            self._run_with_ssh()
        else:
            self._run_with_default()

    # TODO: remove duplicity of _run_with_default and _run_with_ssh codes
    def _run_with_default(self):
        """
        _run_with_default(self)

        Get commands and arguments for local configuration
        """
        self._split_list_of_commands()

        if not self.list_of_commands:
            raise Exception("There where no commands for extraction")

        for command in self.list_of_commands:
            manpage = self._get_manpage(command)
            if manpage is None:
                continue
            self._parse_sections(manpage, command)
            for section in ('OPTIONS', 'DESCRIPTION'):
                self._parse_arguments(section)  # TODO. Needs to change for modularity
            self._save_into_db()

    def _run_with_ssh(self):
        """
        _run_with_ssh(self)

        Get commands and arguments remotely
        """
        self._ssh_connect()
        if not self.ssh_commands_man:
            raise Exception("There where no commands for extraction")

        for (command, manpage) in self.ssh_commands_man.items():
            if manpage is None:
                continue
            self._parse_sections(manpage, command)
            for section in ('OPTIONS', 'DESCRIPTION'):
                self._parse_arguments(section)  # TODO. Needs to change for modularity
            self._save_into_db()

    def _ssh_connect(self):
        """
        _ssh_connect(self)

        Establish connection with remote server running a bash shell.
        Get the commands and respective man pages
        """
        self.ssh_commands_man = dict()
        command_string = self._ssh_regex()
        hostname = self.api_config.get("host")
        username = self.api_config.get("username")
        password = self.api_config.get("password")
        port = int(self.api_config.get("port"))
        try:
            # Ssh connect with a remote server
            ssh_connection = pxssh.pxssh(timeout=50)
            ssh_connection.login(hostname, username, password, port=port)
            # Send to server the command to get the multiline string of commands
            ssh_connection.sendline(command_string)
            ssh_connection.prompt()
            raw_commands = ssh_connection.before
            commands = raw_commands.decode('utf-8')
            # Get the list of command into python list
            ssh_list_of_commands = commands.splitlines()
            for command in ssh_list_of_commands:
                print("Generating manpage for {}".format(command))
                get_man = 'man -L en {} | cat '.format(command)
                # Getting the man pages info of a command
                ssh_connection.sendline(get_man)
                ssh_connection.prompt()
                raw_manpage = ssh_connection.before
                try:
                    man = raw_manpage.decode('utf-8')
                except: # TODO: add an specific exception type
                    continue
                if "No manual" in man:
                    manpage = None
                else:
                    # Getting the manpage after apply the regular expression configured
                    manpage = re.split(self.sections_re, man)
                # Assigning manpages to a <ssh_commands_man> dictionary using <command> as a key
                self.ssh_commands_man[command] = manpage

        except pxssh.ExceptionPxssh as e:
            connection = False
            print("pxssh failed on login.")
            print(e)
            raise Exception('{0}'.format(e))

        ssh_connection.logout()

    def _get_manpage(self, command):
        """
        _get_manpage(self, command) -> [man_pages_regular_expression_splitted] | None

        Get the man pages for a <command> in a local environment

        Returns a python list depending of the regular expression configured
        """
        try:
            man = subprocess.getoutput("man -L en {0}".format(command))
        except: # TODO: add an specific exception type
            man = subprocess.getoutput("man -L en {0}".format(command.encode('utf-8')))
        if 'No manual' in man:
            return None
        return re.split(self.sections_re, man)

    def _parse_sections(self, manpage, command):
        """
        _parse_sections(self, manpage, command)

        Parse the sections of the manpage for an specific command
        """
        print("Working in {0} {1:.5}".format(command, time.time() - self.initial_time))
        self.sections_dict = dict()
        self.arguments_dict = dict()
        save_section_flag = False
        section_name = " "
        name_description = " "

        for block in manpage:
            bloc_stripped = block.strip()
            if bloc_stripped in self.sections_list:
                save_section_flag = True
                section_name = bloc_stripped
                continue
            if save_section_flag:
                if section_name in 'NAME':  ## TODO Needs to change for modularity
                    self.sections_dict[section_name] = command
                    name_description = re.split(" [-—] ", bloc_stripped)
                elif section_name in "SYNOPSIS":  ## TODO Needs to change for modularity
                    try:
                        self.sections_dict[section_name] = name_description[1]
                    except:
                        pass
                else:
                    self.sections_dict[section_name] = block
                    save_section_flag = False

    def _parse_arguments(self, section):
        """
        _parse_arguments(self, section)

        Once the section is parsed, it is necessary to parse the arguments of a given section
        """
        try:
            arguments_list = re.split(self.arguments_re, self.sections_dict[section])
            sp_arguments_list = re.findall(self.sp_arguments_re, self.sections_dict[section])
            argument_name = ""
            flag_list = [False, " "]
            save_arg_body = False
            for line in arguments_list:
                stripped_line = line.strip()
                if not stripped_line:
                    continue
                if "-" in stripped_line[0]:
                    argument_name = stripped_line
                    if line in sp_arguments_list:
                        flag_list[0] = True
                    else:
                        flag_list[0] = False
                    save_arg_body = True
                    continue
                if save_arg_body:
                    flag_list[1] = stripped_line
                    self.arguments_dict[argument_name] = flag_list
                    save_arg_body = False
                    flag_list = [False, " "]
        except Exception as error:
            pass # TODO: improve the exception handling
            # print(" error in Parse Argument: {}".format(error))

    def _getSource(self, category):
        """
        _getSource(self, category) -> Source object (check models.py of apps/Products)

        Method that gets the source depending of category:
            1   -   Flow Sentences
            2   -   OS
            3   -   Product
            4   -   Robot Framework
            5   -   External Libraries

            Just 2 and 3 are used.

        Returns source object
        """
        if category is 2:
            if self.api_config.get('host'):
                name = "{0} - {1}".format(distro.linux_distribution()[0], distro.linux_distribution()[1])
                version = self.api_config.get('host')
            else:
                name = distro.linux_distribution()[0]
                version = distro.linux_distribution()[1]
            # name = "dummy"
            # version = "dummy"
            try:
                source, created = Source.objects.get_or_create(
                    name=name,
                    version=version,
                    category=2
                )
            except Exception as error:
                source = "None"
                print(" error in get OS: {}".format(error))
        elif category is 3:
            try:
                source = Source.objects.get(id=self.api_config.get("source"))
            except Exception as error:
                source = "None"
                print(" error in get OS: {}".format(error))
        else:
            source = None
        return source

    def _save_into_db(self):
        """
        _save_into_db(self)

        Metod to save the command created and the arguments
        """
        # TODO: raise exceptions
        try:
            # Generating command
            command, created = Command.objects.get_or_create(
                name=self.sections_dict['NAME'],  ## TODO: Needs to change for modularity
                description=self.sections_dict['SYNOPSIS'],  ## TODO: Needs to change for modularity
            )
            try:
                command.source.add(self.source)
            except Exception as error:
                pass
                # print(" error in saving OS: {}".format(error))
            command.save()
        except Exception as error:
            pass
            # print(" error in Command DB: {}".format(error))

        try:
            # Getting all arguments and assigning to the command
            for key, value in self.arguments_dict.items():
                args, created = Argument.objects.get_or_create(
                    command=command,
                    name=key,
                    description=value[1],
                    needs_value=value[0]
                )
                args.save()

        except Exception as error:
            pass
            print(" error in Argument DB: {}".format(error))


class PExtract(MExtract):
    """
    PExtract(MExtract)

    Class created to extract information for man pages, designed to get the parameters of product commands
    """
    def __init__(self, config, sections_list=None):
        """
        __init__(self, config, sections_list=None)

        Initialization of PExtract:
            config        - Dictionary that have connection data in case user wants to extract
                            information remotely, the keys are:
                                "host"
                                "username"
                                "password"
                                "port"
                            It will be used as <api_config> in MExtract.__init__ method
            sections_list - list of sections of man pages information
        """
        arguments_re = None
        if config.get('host'):
            commands = "ls {} -p | grep -v /".format(config.get('path'))
        else:
            try:
                commands = subprocess.getoutput("ls {} -p | grep -v /".format(config.get('path')))
            except Exception as error:
                print("Invalid Directory = {}".format(error))
                return

        if config.get('regex'):
            try:
                arguments_re = re.compile(config.get('regex'), flags=re.M)
            except re.error as error:
                print("Invalid Regular Expression = {}".format(error))
                return

        self.p_config = (commands, arguments_re)
        self.api_config = config
        MExtract.__init__(self, sections_list=sections_list, p_config=self.p_config,
                          api_config=self.api_config)


class RExtract():
    """
    RExtract

    Class created to extract information from Robot Framework documentations
    """
    def __init__(self, config):
        """ 
        __init__(self, config)

        Initialization of RExtract:
            config - Dictionary that have the information of where to get Robot
                     documentation, the keys can be:
                         "source"
                         "category" Can be 4 that means Robot Framework
                                    or 5 that means External Libraries
                         "zip" - zipfile path
                         "url"
        """
        robot_version = Source.objects.get(id=config.get("source"))
        self.r_version = robot_version
        self.libraries = list()
        self.extra_libraries = list()
        self.source_dict = dict()
        _category = int(config.get('category'))
        if _category is 4:
            self.zip = zipfile.ZipFile(config.get("zip"))
            for path in self.zip.namelist():
                if re.search(r'/libraries/', path):
                    name = path.split('/')[-1].split('.')[0]
                    self.libraries.append({
                        'name': name,
                        'lib_page': self.zip.open(path).readlines()
                    })
                    source, created = Source.objects.get_or_create(
                        name=name,
                        version=self.r_version.version,
                        category=5,
                    )
                    instance = source
                    instance.depends.add(self.r_version)
                    instance.save()
                    self.source_dict[name] = instance
        elif _category is 5:
            self.lib_url = config.get("url")
            req = urllib.request.Request(self.lib_url)
            res = urllib.request.urlopen(req)
            name = self.lib_url.split('/')[-1].split('.')[0]
            self.libraries.append({
                'name': name,
                'lib_page': res.readlines()
            })
            self.source_dict[name] = robot_version



    def _lib_parser(self, lib):
        """
        _lib_parser(self, lib) -> True | False

        Parses a Robot library from a json formated string
        format is expected to be like the Robot Framework 3.0 page
        """
        lib_name = lib['name']
        libdoc = False
        for x in lib['lib_page']:
            # libdoc is the JS variable where the docs are stored.
            # webpage renders doc tables based on this json
            line = x.decode('utf-8')
            if re.search(r'libdoc =', line):
                libdoc = True
                line = re.sub(r'\\x3c', '<', line)
                line = re.sub(r';', '', line)
                #print(line.split('=', 1)[1])
                lib_dict = json.loads(line.split('=', 1)[1])
                for keyword in lib_dict['keywords']:
                    try:
                        rbt_keyw, created = Command.objects.get_or_create(
                            name=keyword['name'],
                            description=keyword['shortdoc']
                        )
                        rbt_keyw.source.add(self.source_dict[lib_name])
                        rbt_keyw.save()
                    except Exception as error:
                        print(error)
                    for arg in keyword['args']:
                        is_required = True
                        if "=" in arg:
                            is_required = False
                        arg_split = arg.split('=')
                        arg_name = arg_split[0]
                        try:
                            keyw_opt, created = Argument.objects.get_or_create(
                                command = rbt_keyw,
                                name=arg_name,
                                description=rbt_keyw,
                                requirement=is_required,
                                needs_value=True
                            )
                            rbt_keyw.save()
                        except Exception as error:
                            print(error)
        # endfor
        return libdoc

    def run_r_extract(self):
        """
        run_r_extract(self) -> True | False

        Runs R Extract with loaded libraries
        """
        for lib in self.libraries:
            print("Running parser for {}".format(lib['name']))
            result = self._lib_parser(lib)
            if result:
                print("Library {} added".format(lib['name']))
                continue
            else:
                return False
        return True
