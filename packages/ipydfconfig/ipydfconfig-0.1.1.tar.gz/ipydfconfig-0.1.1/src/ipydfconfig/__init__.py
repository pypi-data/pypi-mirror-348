from IPython.core.magic import magics_class, Magics, cell_magic
from IPython import get_ipython
import ast
import importlib
import json
import sys
import warnings


SUPPORTED_LIBS = {"pandas", "polars"}

DEFAULT_SHORTCUTS = {
    "nr": {"pd": ["display.max_rows", "display.min_rows"], "pl": ["tbl_rows"]},
    "rows": {"pd": ["display.max_rows", "display.min_rows"], "pl": ["tbl_rows"]},
    "nc": {"pd": ["display.max_columns"], "pl": ["tbl_cols"]},
    "cols": {"pd": ["display.max_columns"], "pl": ["tbl_cols"]},
    "strlen": {"pd": ["display.max_colwidth"], "pl": ["fmt_str_lengths"]},
    "listlen": {
        "pd": ["display.max_seq_items"],
        "pl": ["fmt_table_cell_list_length"],
    },
}


def flatten_options(d, prefix=""):
    flat = {}
    for k, v in d.items():
        full_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            flat.update(flatten_options(v, full_key))
        else:
            flat[full_key] = v
    return flat


class IpyDfConfigWarning(UserWarning):
    pass


@magics_class
class IpyDfConfigMagics(Magics):
    def __init__(self, shell):
        super().__init__(shell)

        self.libs = {}
        self.shortcuts = DEFAULT_SHORTCUTS.copy()
        self._plconfig_states = {}
        self._pdconfig_states = {}

        shell.events.register("post_run_cell", self._restore_plconfig_after_cell_hook())
        shell.events.register("post_run_cell", self._restore_pdconfig_after_cell_hook())

    def has_lib(self, lib_name):
        return self.get_lib(lib_name) is not None

    def get_lib(self, lib_name, force_load=False):
        if lib_name not in self.libs:
            if lib_name in SUPPORTED_LIBS:
                if lib_name not in sys.modules:
                    if force_load:
                        self.libs[lib_name] = importlib.import_module(lib_name)
                elif lib_name in sys.modules:
                    self.libs[lib_name] = sys.modules[lib_name]
        if lib_name in self.libs:
            return self.libs[lib_name]

        # implicitly return None if the library is not found

    def parse_args(self, line):
        args = {}
        for arg in line.split():
            if "=" in arg:
                key, value = arg.split("=", 1)
                try:
                    args[key] = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    args[key] = value
        return args

    def expand_shortcuts(self, config_kwargs, prefix):
        expanded_kwargs = {}
        for key, value in config_kwargs.items():
            if key in self.shortcuts and prefix in self.shortcuts[key]:
                for exp_key in self.shortcuts[key][prefix]:
                    expanded_kwargs[exp_key] = value
            else:
                expanded_kwargs[key] = value
        return expanded_kwargs

    @cell_magic
    def dfconfig(self, line, cell):
        config_kwargs = self.parse_args(line)
        if len(config_kwargs) < 1:
            return

        if self.has_lib("pandas"):
            expanded_kwargs = self.expand_shortcuts(config_kwargs, "pd")
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", IpyDfConfigWarning)
                self.set_pdconfig(cell, expanded_kwargs)
        if self.has_lib("polars"):
            expanded_kwargs = self.expand_shortcuts(config_kwargs, "pl")
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", IpyDfConfigWarning)
                self.set_plconfig(cell, expanded_kwargs)
        get_ipython().run_cell(cell)

    @cell_magic
    def plconfig(self, line, cell):
        config_kwargs = self.parse_args(line)
        expanded_kwargs = self.expand_shortcuts(config_kwargs, "pl")
        if len(expanded_kwargs) < 1:
            return

        self.set_plconfig(cell, expanded_kwargs)
        get_ipython().run_cell(cell)

    def set_plconfig(self, cell, config_kwargs):
        pl = self.get_lib("polars", force_load=True)
        exec_count = get_ipython().execution_count

        saved_state = pl.Config.save()
        self._plconfig_states[exec_count] = saved_state

        for key, val in config_kwargs.items():
            if hasattr(pl.Config, f"set_{key}"):
                getattr(pl.Config, f"set_{key}")(val)
            else:
                warnings.warn(f"Invalid polars option: {key}", IpyDfConfigWarning)

    @cell_magic
    def pdconfig(self, line, cell):
        config_kwargs = self.parse_args(line)
        expanded_kwargs = self.expand_shortcuts(config_kwargs, "pd")
        if len(expanded_kwargs) < 1:
            return

        self.set_pdconfig(cell, expanded_kwargs)
        get_ipython().run_cell(cell)

    def set_pdconfig(self, cell, config_kwargs):
        pd = self.get_lib("pandas", force_load=True)
        exec_count = get_ipython().execution_count
        saved_state = json.dumps(flatten_options(pd.options.d))
        self._pdconfig_states[exec_count] = saved_state

        for key, val in config_kwargs.items():
            try:
                pd.set_option(key, val)
            except pd.errors.OptionError:
                warnings.warn(f"Invalid pandas option: {key}", IpyDfConfigWarning)

    def _restore_pdconfig_after_cell_hook(self):
        def _restore_pdconfig_after_cell(result):
            exec_count = result.execution_count
            if exec_count in self._pdconfig_states:
                pd = self.get_lib("pandas", force_load=True)
                saved_state = self._pdconfig_states.pop(exec_count)
                options_d = json.loads(saved_state)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", FutureWarning)
                    for k, v in options_d.items():
                        pd.set_option(k, v)

        return _restore_pdconfig_after_cell

    def _restore_plconfig_after_cell_hook(self):
        def _restore_plconfig_after_cell(result):
            exec_count = result.execution_count
            if exec_count in self._plconfig_states:
                pl = self.get_lib("polars", force_load=True)
                saved_state = self._plconfig_states.pop(exec_count)
                pl.Config.load(saved_state)

        return _restore_plconfig_after_cell


def load_ipython_extension(ipython):
    ip = get_ipython()
    ip.register_magics(IpyDfConfigMagics)
