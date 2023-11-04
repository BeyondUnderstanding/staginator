from copy import copy


class ConfigManager:
    def __init__(self):
        self.known_vars = [
            ('[deploy_path]', 'deploy_path'),
            ('[deploy_port]', 'deploy_port'),
            ('[stage_name]', 'stage_name'),
            ('[branch]', 'branch'),
            ('[repository_name]', 'repository_name'),
        ]

    def assign_vars(self, var_list, source: str):
        """
        Vars
        [deploy_path]
        [deploy_port]
        [stage_name]
        [branch]
        [repository_name]
        """
        source_copy = copy(source)
        for var in self.known_vars:
            if var[0] in source_copy:
                source_copy = source_copy.replace(var[0], str(var_list[var[1]]))
        return source_copy

    def generate_nginx(self, var_list) -> str:
        with open('template.nginx', 'r') as f:
            file = f.read()

            return self.assign_vars(var_list, file)
