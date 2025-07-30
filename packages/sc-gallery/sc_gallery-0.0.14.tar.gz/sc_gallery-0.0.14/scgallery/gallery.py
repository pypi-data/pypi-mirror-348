#!/usr/bin/env python3

import argparse
import inspect
import json
import os
import shutil
import sys
import threading
from collections.abc import Container
import fnmatch

import siliconcompiler
from siliconcompiler import Schema
from siliconcompiler.schema.parametertype import NodeType
from siliconcompiler.utils import default_credentials_file
from siliconcompiler.tools._common import has_input_files
from siliconcompiler.tools._common.asic import get_mainlib
from siliconcompiler.flowgraph import RuntimeFlowgraph

from scgallery.targets.freepdk45 import (
    nangate45 as freepdk45_nangate45
)
from scgallery.targets.asap7 import (
    asap7sc7p5t_rvt as asap7_asap7sc7p5t_rvt
)
from scgallery.targets.skywater130 import (
    sky130hd as sky130_sky130hd
)
from scgallery.targets.gf180 import (
    gf180mcu_fd_sc_mcu7t5v0 as gf180_gf180mcu_fd_sc_mcu7t5v0,
    gf180mcu_fd_sc_mcu9t5v0 as gf180_gf180mcu_fd_sc_mcu9t5v0
)
from scgallery.targets.ihp130 import (
    sg13g2_stdcell as ihp130_sg13g2_stdcell
)
from scgallery.targets import linting as gallery_lint
from siliconcompiler.flows import lintflow

from scgallery import __version__

from scgallery.checklists import asicflow_rules


class Gallery:
    SDC_KEY = ('option', 'dir', 'gallery_sdc_path')

    def __init__(self, name=None, path=None):
        self.__name = name
        self.set_path(path)

        self.__lambdalib_techs = {}

        self.__targets = {}
        for name, target in (
                ("freepdk45_nangate45", freepdk45_nangate45),
                ("skywater130_sky130hd", sky130_sky130hd),
                ("asap7_asap7sc7p5t_rvt", asap7_asap7sc7p5t_rvt),
                ("gf180_gf180mcu_fd_sc_mcu9t5v0", gf180_gf180mcu_fd_sc_mcu9t5v0),
                ("gf180_gf180mcu_fd_sc_mcu7t5v0", gf180_gf180mcu_fd_sc_mcu7t5v0),
                ("ihp130_sg13g2_stdcell", ihp130_sg13g2_stdcell),
                ("None", None)):
            self.add_target(name, target)

        self.__designs = {}
        from scgallery.designs import all_designs as sc_all_designs
        for name, design in sc_all_designs().items():
            self.add_design(name, design["module"], rules=design["rules"])

        self.__run_config = {
            "targets": set(),
            "designs": set()
        }

        self.__status = []
        self.__report_chips = {}

        self.__jobname = None
        self.set_clean(False)
        self.set_remote(None)
        self.set_scheduler(None)
        self.set_strict(True)
        self.set_rules_to_skip(None)

    #######################################################
    @property
    def name(self):
        '''
        Name of the gallery

        Returns:
            str/None: Name of gallery
        '''
        return self.__name

    @property
    def has_name(self):
        '''
        Determine if the gallery has a name

        Returns:
            boolean: True, if a name is present, False if not
        '''
        if self.name:
            return True
        return False

    @property
    def title(self):
        '''
        Title string for the gallery

        Returns:
            str: Title for the gallery
        '''
        name = "Gallery"
        if self.has_name:
            name = f"{self.name} gallery"
        return f"{name} generator for SiliconCompiler {siliconcompiler.__version__}"

    #######################################################
    @property
    def path(self):
        '''
        Path to the gallery

        Returns:
            str: Absolute path to the gallery
        '''
        return self.__path

    def set_path(self, path):
        '''
        Set the path to the gallery.

        The path will be converted to an absolute path

        Parameters:
            path (str): path to the gallery output
        '''
        if not path:
            default_path = 'gallery'
            if self.has_name:
                default_path = f'{default_path}-{self.name}'
            path = os.path.join(os.getcwd(),
                                default_path,
                                siliconcompiler.__version__)
        self.__path = os.path.abspath(path)

    #######################################################
    def add_target(self, name, module):
        '''
        Add a target to the gallery.

        Parameters:
            name (str): name of the target
            module (module): python module for the target
        '''
        self.__targets[name] = module

        if module:
            module.register_lambdalib(self)

    def remove_target(self, name):
        '''
        Removes a target from the gallery.

        Parameters:
            name (str): name of the target to remove
        '''
        if name in self.__targets:
            del self.__targets[name]

    def get_targets(self):
        '''
        Get a list of target names registered in the gallery.

        Returns:
            list (str): List of target names
        '''
        return list(self.__targets.keys())

    #######################################################
    def add_design(self, name, module, rules=None, setup=None):
        '''
        Add a design to the gallery.

        Parameters:
            name (str): name of the design
            module (module): python module for the design
            rules (list [path]): list of paths to the rules for this design
            setup (list [function]): list of functions to help configure the design in external
                galleries
        '''
        self.__designs[name] = {
            "module": module,
            "rules": [],
            "setup": []
        }

        if not rules:
            rules = []
        if not isinstance(rules, (list, tuple)):
            rules = [rules]
        for rule in rules:
            self.add_design_rule(name, rule)

        if not setup:
            setup = []
        if not isinstance(setup, (list, tuple)):
            setup = [setup]

        for setup_name, builtin_setup in inspect.getmembers(module, inspect.isfunction):
            if setup_name.startswith('setup_') and builtin_setup not in setup:
                setup.append(builtin_setup)

        for func in setup:
            self.add_design_setup(name, func)

    def remove_design(self, name):
        '''
        Removes a design from the gallery.

        Parameters:
            name (str): name of the design to remove
        '''
        if name in self.__designs:
            del self.__designs[name]

    def get_design(self, design):
        '''
        Gets the configuration for a design.

        Returns:
            dict: Configuration of a design
        '''
        info = self.__designs[design].copy()
        for key in info.keys():
            if key == 'module':
                continue
            info[key] = info[key].copy()
        return info

    def get_designs(self):
        '''
        Get a list of design names registered in the gallery.

        Returns:
            list (str): List of design names
        '''
        return list(self.__designs.keys())

    #######################################################
    def set_remote(self, remote):
        '''
        Set the path to the remote credentials file.

        Parameters:
            remote (str): path to the credentials
        '''
        if remote:
            remote = os.path.abspath(remote)
            if not os.path.isfile(remote):
                raise FileNotFoundError(f'{remote} does not exists or is not a regular file')

        self.__remote = remote

    @property
    def is_remote(self):
        '''
        Determine if the gallery is set to run remotely

        Returns:
            boolean: True, if running remotely, False if not
        '''
        if self.__remote:
            return True
        return False

    #######################################################
    def set_scheduler(self, scheduler):
        '''
        Set the scheduler to use.

        Parameters:
            scheduler (str): scheduler name
        '''
        self.__scheduler = scheduler

    @property
    def has_scheduler(self):
        '''
        Determine if a scheduler is set

        Returns:
            boolean: True, is scheduler is set
        '''
        return self.__scheduler is not None

    @property
    def scheduler(self):
        '''
        Get the name of the scheduler

        Returns:
            str: name of scheduler
        '''
        return self.__scheduler

    #######################################################
    def set_clean(self, clean):
        '''
        Set if the gallery should clean a previous run.

        Parameters:
            clean (boolean): Flag to indicate if clean should be used
        '''
        if clean:
            clean = True
        else:
            clean = False
        self.__clean = clean

    @property
    def is_clean(self):
        '''
        Determine if the gallery is set to clean a previous run

        Returns:
            boolean: True, if resuming, False if not
        '''
        return self.__clean

    #######################################################
    def set_strict(self, strict):
        '''
        Set if the gallery should use strict mode when running siliconcompiler.

        Parameters:
            strict (boolean): Flag to indicate if strict should be used
        '''
        if strict:
            strict = True
        else:
            strict = False
        self.__strict = strict

    @property
    def is_strict(self):
        '''
        Determine if the gallery is set to strict mode

        Returns:
            boolean: True, if using strict, False if not
        '''
        return self.__strict

    ###################################################
    def set_rules_to_skip(self, rules):
        '''
        Set rules to skip during checks

        Parameters:
            rules (list): List of glob rules
        '''
        if not rules:
            rules = []
        elif isinstance(rules, str):
            rules = [rules]
        self.__skip_rules = rules

    @property
    def rules_to_skip(self):
        '''
        Set of rules to skip at the end of run checks.

        Returns:
            list: List of rules to skip during checks
        '''
        return self.__skip_rules

    #######################################################
    def add_design_rule(self, design, rule):
        '''
        Add a new rules file to a design.

        Parameters:
            design (str): name of the design
            rule (path): path to the rules for this design
        '''
        if not rule:
            return

        if not os.path.isfile(rule):
            raise FileNotFoundError(rule)

        self.__designs[design]['rules'].append(rule)

    def get_design_rules(self, design):
        '''
        Get a list of rules for the design.

        Parameters:
            design (str): name of the design

        Returns:
            list (path): list of paths to rules files
        '''
        return self.__designs[design]['rules'].copy()

    def clear_design_rules(self, design):
        '''
        Removes all design rules from a design.

        Parameters:
            design (str): name of the design
        '''
        self.__designs[design]['rules'].clear()

    #######################################################
    def add_design_setup(self, design, func):
        '''
        Add a new setup function to a design.

        Parameters:
            name (str): name of the design
            setup (function): functions to help configure the design in external
                galleries
        '''
        self.__designs[design]['setup'].append(func)

    def get_design_setup(self, design):
        '''
        Get a list of setup functions to a design.

        Parameters:
            name (str): name of the design

        Returns:
            list (function): list of functions to setup the design
        '''
        return self.__designs[design]['setup'].copy()

    #######################################################
    def set_jobname_suffix(self, suffix):
        '''
        Sets a suffix to the default job names.

        Parameters:
            suffix (str): string to append to the job names during a gallery run.
        '''
        self.__jobname = suffix

    #######################################################
    def register_lambdalib(self, pdk, mainlib, library, swaps, add_macrolibs=False):
        '''
        Sets a suffix to the default job names.

        Parameters:
            pdk (str): pdk this library belongs to.
            mainlib (str): main library to match this library to, can be a glob.
            library (module): module to load.
            swaps (list of (str, str)]): library pairs to swap to perform techmapping.
            add_macrolibs (boolean): add additional macros libraries
        '''
        if pdk not in self.__lambdalib_techs:
            self.__lambdalib_techs[pdk] = {}

        if mainlib not in self.__lambdalib_techs[pdk]:
            self.__lambdalib_techs[pdk][mainlib] = []

        macrolibs = []
        if add_macrolibs:
            for lib in library.setup():
                if lib.design.startswith('lambdalib_'):
                    continue
                macrolibs.append(lib.design)

        self.__lambdalib_techs[pdk][mainlib].append(
            {
                "library": library,
                "swap": swaps,
                "macrolibs": macrolibs
            }
        )

    #######################################################
    def set_run_designs(self, designs):
        '''
        Sets the designs to execute during a run.

        Parameters:
            designs (list [str]): list of design names
        '''
        self.__run_config['designs'].clear()
        self.__run_config['designs'].update(designs)

    #######################################################
    def set_run_targets(self, targets):
        '''
        Sets the targets to use during a run.

        Parameters:
            targets (list [str]): list of target names
        '''
        self.__run_config['targets'].clear()
        self.__run_config['targets'].update(targets)

    #######################################################
    @staticmethod
    def _ensure_sdc(chip, setup_module_path):
        has_sdc = Gallery.__design_has_sdc(chip)
        has_clock = Gallery.__design_has_clock(chip)

        # Attempt to find a constraints file
        if not has_clock and not has_sdc:
            if chip.valid(*Gallery.SDC_KEY):
                sdc_path = chip.find_files(*Gallery.SDC_KEY)
                if sdc_path:
                    sdc_path = sdc_path[0]
            else:
                sdc_path = os.path.join(
                    setup_module_path,
                    'constraints')

                if not os.path.exists(sdc_path):
                    sdc_path = None
            if sdc_path:
                sdc_file = os.path.join(sdc_path, f'{get_mainlib(chip)}.sdc')
                if os.path.exists(sdc_file):
                    chip.input(sdc_file)

    @staticmethod
    def __design_has_clock(chip):
        for pin in chip.getkeys('datasheet', 'pin'):
            if chip.get('datasheet', 'pin', pin, 'type', 'global') == "clock":
                return True

        return False

    @staticmethod
    def __design_has_sdc(chip):
        # Reject if no SDC is provided
        if not chip.valid('input', 'constraint', 'sdc'):
            return False

        # Reject of SDC cannot be found
        sdcs = [sdc for sdc in chip.find_files('input', 'constraint', 'sdc', missing_ok=True)
                if sdc]
        if not sdcs:
            return False

        return True

    #######################################################
    def __setup_design(self, design, target):
        if target:
            print(f'Setting up "{design}" with "{target}"')
            if not self.__design_needs_target(self.__designs[design]):
                chip = self.__designs[design]['module'].setup(
                    target=self.__targets[target])
            else:
                chip = self.__designs[design]['module'].setup()
                chip.use(self.__targets[target])
        else:
            print(f'Setting up "{design}"')
            chip = self.__designs[design]['module'].setup()

        self._register_design_sources(chip)

        # Perform additional setup functions
        if self.__designs[design]['setup']:
            for setup_func in self.__designs[design]['setup']:
                setup_func(chip)

        Gallery._ensure_sdc(
            chip,
            os.path.dirname(self.__designs[design]['module'].__file__)
        )

        has_sdc = Gallery.__design_has_sdc(chip)
        has_clock = Gallery.__design_has_clock(chip)

        is_lint = target == "lint"

        is_valid = has_sdc or has_clock or is_lint

        return chip, is_valid

    def __setup_run_chip(self, chip, name, jobsuffix=None):
        pdk = chip.get('option', 'pdk')
        mainlib = get_mainlib(chip)
        jobname = f"{pdk}_{mainlib}"
        if self.__jobname:
            jobname += f"_{self.__jobname}"
        if jobsuffix:
            jobname += jobsuffix
        chip.set('option', 'jobname', f"{chip.get('option', 'jobname')}_{jobname}")

        chip.set('option', 'nodisplay', True)
        chip.set('option', 'quiet', True)
        chip.set('option', 'strict', self.is_strict)

        chip.set('option', 'clean', self.is_clean)

        if self.has_scheduler:
            chip.set('option', 'scheduler', 'name', self.__scheduler)
        elif self.is_remote:
            chip.set('option', 'credentials', self.__remote)
            chip.set('option', 'remote', True)

        if not chip.get('option', 'entrypoint', step=Schema.GLOBAL_KEY, index=Schema.GLOBAL_KEY):
            chip.set('option', 'entrypoint', chip.design)
        chip.set('design', name)

        # Perform lambdalib swaps
        if pdk in self.__lambdalib_techs:
            swaps = set()
            for tech, libraries in self.__lambdalib_techs[pdk].items():
                if fnmatch.fnmatch(mainlib, tech):
                    for library in libraries:
                        chip.use(library['library'])
                        swaps.update(library['swap'])

                        chip.add('asic', 'macrolib', library['macrolibs'])

            for src_lib, dst_lib in swaps:
                chip.swap_library(src_lib, dst_lib)

    def __lint(self, design, tool):
        chip = design['chip']

        if not chip:
            # custom flow, so accept
            return None

        if 'lintflow' in chip.getkeys('flowgraph'):
            chip.schema.remove('flowgraph', 'lintflow')
        chip.use(lintflow, tool=tool)

        self.__setup_run_chip(chip, design["design"], jobsuffix="_lint")

        chip.set('option', 'flow', 'lintflow')

        chip.set('arg', 'step', Schema.GLOBAL_KEY)
        chip.set('arg', 'index', Schema.GLOBAL_KEY)
        if not has_input_files(chip, 'input', 'rtl', 'verilog') and \
                not has_input_files(chip, 'input', 'rtl', 'systemverilog'):
            # Right now there are no linting for non-verilog
            return None
        chip.set('arg', 'step', None)
        chip.set('arg', 'index', None)

        # Make sure there are not set
        chip.unset('asic', 'logiclib')
        chip.unset('asic', 'macrolib')

        try:
            chip.run(raise_exception=True)
        except Exception:
            return False

        if chip.get('metric', 'errors', step='lint', index='0') == 0:
            return True
        return False

    def __run_design(self, design):
        chip = design['chip']

        runtime_setup = design['runtime_setup']
        if runtime_setup:
            print(f'Executing runtime setup for: {design["design"]}')
            try:
                if self.__design_has_target_option(design, setup_func=runtime_setup):
                    chip = runtime_setup(self, target=design['target'])
                else:
                    chip = runtime_setup(self)

                if self.__design_needs_target(self.__designs[design['design']]) and \
                        design['target']:
                    chip.use(design['target'])
            except Exception:
                return chip, False

        self.__setup_run_chip(chip, design["design"])

        try:
            chip.run(raise_exception=True)
        except Exception:
            return chip, False

        return chip, True

    def __finalize(self, design, chip, succeeded):
        report_data = {
            "chip": chip,
            "platform": chip.get('option', 'pdk'),
            "rules": []
        }
        self.__report_chips.setdefault(design, []).append(report_data)

        chip.set('arg', 'step', Schema.GLOBAL_KEY)
        chip.set('arg', 'index', Schema.GLOBAL_KEY)
        mainlib = get_mainlib(chip)
        chip.unset('arg', 'step')
        chip.unset('arg', 'index')

        if succeeded:
            chip.summary()
            chip.snapshot(display=False)

            rules_files = self.__designs[design]['rules']

            if rules_files:
                runtime = RuntimeFlowgraph(
                    chip.schema.get("flowgraph", chip.get('option', 'flow'), field='schema'),
                    from_steps=chip.get('option', 'from'),
                    to_steps=chip.get('option', 'to'),
                    prune_nodes=chip.get('option', 'prune'))

                chip.logger.info(f"Checking rules in: {', '.join(rules_files)}")
                chip.use(
                    asicflow_rules,
                    job=chip.get('option', 'jobname'),
                    flow=chip.get('option', 'flow'),
                    mainlib=mainlib,
                    flow_nodes=runtime.get_nodes(),
                    rules_files=rules_files,
                    skip_rules=self.__skip_rules)
                error = not chip.check_checklist('asicflow_rules',
                                                 verbose=True,
                                                 require_reports=False)
            else:
                error = None
        else:
            error = True

        self.__status.append({
            "design": design,
            "pdk": chip.get('option', 'pdk'),
            "mainlib": mainlib,
            "error": error,
            "chip": chip
        })
        if not succeeded:
            chip.logger.error("Run failed")
        elif error:
            chip.logger.error("Rules mismatch")
        elif rules_files:
            chip.logger.info("Rules match")

        self.__copy_chip_data(chip, report_data)

    def __copy_chip_data(self, chip, report_data):
        jobname = chip.get('option', 'jobname')
        png = os.path.join(chip.getworkdir(), f'{chip.design}.png')

        file_root = f'{chip.design}_{jobname}'

        if os.path.isfile(png):
            img_path = os.path.join(self.path, f'{file_root}.png')
            shutil.copy(png, img_path)
            report_data["path"] = img_path

        chip.archive(include=['reports', '*.log'],
                     archive_name=os.path.join(self.path, f'{file_root}.tgz'))

    def __design_has_target_option(self, design, setup_func=None):
        '''
        Checks if a design as a setup function with a target argument.
        If false, this design cannot be matrixed with targets
        '''
        if not setup_func:
            setup_func = getattr(self.__designs[design]['module'], 'setup', None)

        if not setup_func:
            return False

        return 'target' in inspect.getfullargspec(setup_func).args

    def __design_needs_target(self, design):
        '''
        Checks if the design has 'gallery_needs_target' set and returns the value.
        This will default to true.
        '''
        return getattr(design['module'], 'gallery_needs_target', True)

    def __design_runtime_setup(self, design):
        return getattr(self.__designs[design]['module'], 'runtime_setup', None)

    def __get_runnable_jobs(self):
        regular_jobs = []

        def _run_setup(design, target):
            runtime_setup = self.__design_runtime_setup(design)

            if not runtime_setup:
                chip, valid = self.__setup_design(design, target)
                if not valid:
                    return
            else:
                chip = None

            print_text = f'Running "{design}"'
            if target:
                print_text += f' with "{target}"'

            regular_jobs.append({
                "print": print_text,
                "design": design,
                "runtime_setup": runtime_setup,
                "chip": chip,
                "target": target})

        config_jobs = []
        for design in self.__run_config['designs']:
            if design not in self.__designs:
                print(f'  Error: design "{design}" is not available in gallery')
                continue

            targets = self.__run_config['targets']

            if not self.__design_needs_target(self.__designs[design]):
                if "None" in targets:
                    targets = [None]
                else:
                    continue
            else:
                targets = [target for target in targets if target != "None"]

            for target in targets:
                config_jobs.append(threading.Thread(
                    target=_run_setup,
                    args=(design, target)))

        # Start jobs in parallel
        for job in config_jobs:
            job.start()

        # Wait
        for job in config_jobs:
            if job.is_alive():
                job.join()

        return sorted(regular_jobs, key=lambda x: x["print"])

    def get_run_report(self):
        return self.__report_chips.copy()

    def lint(self, tool):
        '''
        Run lint on the enabled designs.
        '''

        status = {}

        error = False
        for job in self.__get_runnable_jobs():
            print(job['print'])
            lint_status = self.__lint(job, tool)
            if lint_status is not None:
                error |= not lint_status

                status[job['design'], job['target']] = lint_status

        for job, result in status.items():
            design, target = job

            title = f"Lint on \"{design}\""
            if target:
                title += f" with \"{target}\""

            print(title)
            if result:
                print("  Passed")
            else:
                print("  Failed")

        return not error

    def run(self):
        '''
        Main run function which will iterate over the design gallery and generate images and
        summaries for the listed designs and targets.

        Returns:
            boolean: True, if all designs succeeded and no rules were violated, False otherwise.
        '''
        os.makedirs(self.path, exist_ok=True)

        self.__status.clear()
        self.__report_chips.clear()

        regular_jobs = self.__get_runnable_jobs()

        if not regular_jobs:
            return False

        if self.is_remote:
            def _run_remote(chip, design, job):
                if not chip:
                    return
                chip, succeeded = self.__run_design(job)
                self.__finalize(design, chip, succeeded)

            jobs = [threading.Thread(
                target=_run_remote,
                args=(job['chip'], job['design'], job))
                for job in regular_jobs]

            # Submit jobs in parallel
            for job in jobs:
                job.start()

            # Wait
            for job in jobs:
                job.join()
        else:
            for job in regular_jobs:
                chip = job['chip']
                design = job['design']

                print(job['print'])
                chip, succeeded = self.__run_design(job)
                self.__finalize(design, chip, succeeded)

        self.summary()

        failed = any([data["error"] for data in self.__status])
        return not failed

    def summary(self):
        '''
        Print a summary of the previous run.
        '''
        print("Run summary:")
        failed = False
        for status in self.__status:
            print(f" Design: {status['chip'].design} on {status['pdk']} pdk "
                  f"with mainlib {status['mainlib']}")
            error = status['error']
            if error:
                failed = True
                print("  Rules check failed")
            elif error is None:
                # Mark as failed since rules are missing
                failed = True
            else:
                print("  Rules check passed")
        if not failed:
            print('Run passed')

    @staticmethod
    def _register_design_sources(chip):
        chip.register_source(name='scgallery-designs',
                             path='python://scgallery.designs')

    @staticmethod
    def design_commandline(chip, target=None, module_path=None):
        Gallery._register_design_sources(chip)
        args = chip.create_cmdline(chip.design)
        if target and ("target" not in args or not args["target"]):
            chip.use(target)
        if module_path:
            Gallery._ensure_sdc(chip, os.path.dirname(module_path))

    @classmethod
    def main(cls):
        '''
        Main method to initiate the gallery from the commandline.
        '''
        gallery = cls()

        class ArgChoiceGlob(Container):
            def __init__(self, choices):
                super().__init__()

                self.__choices = set(choices)

            def __contains__(self, item):
                if item in self.__choices:
                    return True

                if fnmatch.filter(self.__choices, item):
                    return True

                return False

            def __iter__(self):
                return self.__choices.__iter__()

            def get_items(self, choices):
                items = set()
                for c in choices:
                    items.update(fnmatch.filter(self.__choices, c))
                return sorted(list(items))

        def format_list(items, prefix_len, max_len=80):
            lines = []
            line = None
            while len(items) > 0:
                item = items[0]
                del items[0]
                if not line:
                    line = item
                else:
                    line += f", {item}"

                if len(line) > max_len:
                    lines.append(line)
                    line = None
            if line:
                lines.append(line)

            line_prefix = "".join(prefix_len * [" "])
            format_lines = []
            for n, line in enumerate(lines):
                if n > 0:
                    line = f"{line_prefix}{line}"
                format_lines.append(line)
            return "\n".join(format_lines)

        targets_help = format_list(gallery.get_targets(), 9)
        designs_help = format_list(gallery.get_designs(), 9)

        description = f'''
{gallery.title}

Targets: {targets_help}
Designs: {designs_help}
'''

        design_choices = ArgChoiceGlob(gallery.__designs.keys())
        target_choices = ArgChoiceGlob(gallery.__targets.keys())

        parser = argparse.ArgumentParser(
            prog='sc-gallery',
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        parser.add_argument('-design',
                            action='append',
                            choices=design_choices,
                            metavar='<design>',
                            help='Name of design to run')

        parser.add_argument('-target',
                            action='append',
                            choices=target_choices,
                            metavar='<target>',
                            help='Name of target to run')

        parser.add_argument('-path',
                            metavar='<path>',
                            help='Path to the gallery',
                            default=gallery.path)

        parser.add_argument('-remote',
                            metavar='<path>',
                            nargs='?',
                            action='store',
                            const=default_credentials_file(),
                            default=None,
                            help='Perform a remote run, '
                                 'optionally provides path to remote credentials')

        parser.add_argument('-scheduler',
                            choices=NodeType.parse(
                                Schema().get('option', 'scheduler', 'name', field='type')).values,
                            help='Select the scheduler to use during exection')

        parser.add_argument('-clean',
                            action='store_true',
                            help='Use option,clean')

        parser.add_argument('-gallery',
                            metavar='<module>',
                            help='Python module for custom galleries')

        parser.add_argument('-skip_rules',
                            metavar='<rule>',
                            nargs='+',
                            help='List of regex names for rules to skip in checks')

        parser.add_argument('-json',
                            metavar='<path>',
                            help='Generate json matrix of designs and targets')

        parser.add_argument('-lint',
                            action='store_true',
                            help='Run lint only')

        parser.add_argument('-lint_tool',
                            choices=['verilator', 'slang'],
                            default='verilator',
                            help='Tool to use for linting')

        parser.add_argument('-version', action='version', version=__version__)

        args = parser.parse_args()

        gallery.set_path(args.path)
        gallery.set_clean(args.clean)
        gallery.set_remote(args.remote)

        if args.scheduler:
            gallery.set_scheduler(args.scheduler)

        if args.target:
            gallery.set_run_targets(target_choices.get_items(args.target))
        else:
            gallery.set_run_targets(gallery.__targets.keys())

        if args.design:
            gallery.set_run_designs(design_choices.get_items(args.design))
        else:
            gallery.set_run_designs(gallery.__designs.keys())

        if args.json:
            matrix = []
            for data in gallery.__get_runnable_jobs():
                matrix.append({"design": data["design"], "target": data["target"], "remote": False})

            if os.path.exists(args.json):
                json_matrix = []
                with open(args.json, 'r') as f:
                    json_matrix = json.load(f)

                spare_fields = ('skip', 'cache')
                for config in json_matrix:
                    has_extra = False
                    for key in spare_fields:
                        if key in config:
                            has_extra = True

                    if has_extra:
                        # Copy extra information
                        for new_config in matrix:
                            match = [
                                new_config[key] == config[key] for key in ('design',
                                                                           'target')
                            ]
                            if all(match):
                                if 'skip' in config:
                                    new_config['cache'] = False
                                for key, value in config.items():
                                    new_config[key] = value

            with open(args.json, 'w') as f:
                json.dump(matrix, f, indent=4, sort_keys=True)
            return 0

        if args.lint:
            gallery.add_target("lint", gallery_lint)
            gallery.set_run_targets(["lint"])

            if gallery.lint(args.lint_tool):
                return 0

            return 1

        gallery.set_rules_to_skip(args.skip_rules)
        if not gallery.run():
            return 1
        return 0


if __name__ == "__main__":
    sys.exit(Gallery.main())
