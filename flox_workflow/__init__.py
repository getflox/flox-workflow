from flox_workflow.command import flox_workflow
from floxcore.config import Configuration
from floxcore.plugin import Plugin


class WorkflowConfiguration(Configuration):
    def parameters(self):
        return tuple()

    def schema(self):
        pass


class WorkflowPlugin(Plugin):
    def configuration(self):
        return WorkflowConfiguration()

    def add_commands(self, cli):
        cli.add_command(flox_workflow)


def plugin():
    return WorkflowPlugin()
