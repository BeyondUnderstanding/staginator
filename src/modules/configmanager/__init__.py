import os
from copy import copy


class ConfigManager:
    def __init__(self):
        self.known_vars = [
            ('[stage_name]', 'stage_name'),
            ('[logs_path]', 'logs_path'),
            ('[deploy_port]', 'deploy_port'),
        ]

    def parse(self, **kwargs):
        """
        Vars
        stage_name
        logs_path
        deploy_port
        """
        _return = {}
        for var in self.known_vars:
            if var[1] in kwargs.keys():
                _return[var[1]] = kwargs[var[1]]

        return _return

    def _assign_vars(self, var_list: dict, source: str):
        source_copy = copy(source)
        for var in self.known_vars:
            if var[0] in source_copy:
                source_copy = source_copy.replace(var[0], str(var_list[var[1]]))
        return source_copy

    def _generate_nginx(self, var_list) -> str:
        cwd = os.getcwd()+'/src/modules/configmanager'
        with open(f'{cwd}/template.nginx', 'r') as f:
            file = f.read()

            return self._assign_vars(var_list, file)

    def write_nginx_config(self, vars_list, cwd):
        config = self._generate_nginx(vars_list)
        with open(f'{cwd}', 'w') as f:
            f.write(config)
            f.close()

