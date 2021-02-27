import click as click
from slugify import slugify

from flox_workflow.exceptions import WorkflowException
from floxcore.command import execute_stages
from floxcore.context import Flox


@click.group(name="flow")
def flox_workflow():
    """
    Rapid development with automated workflow
    """
    pass


@flox_workflow.command()
@click.argument("description", required=False)
@click.pass_obj
def start(flox: Flox, description):
    """Start implementation workflow"""
    if flox.local.flow:
        raise WorkflowException("Already in active flow, you need to finish opened flow before starting a new one")

    if not description:
        description = click.prompt("Provide description of your work")

    flow_id = slugify(description)

    execute_stages(flox, "workflow_start", flow_id=flow_id, description=description)

    flox.local.flow = dict(flow_id=flow_id, description=description)


@flox_workflow.command()
@click.argument("message", required=False)
@click.pass_obj
def publish(flox: Flox, message):
    """Publish current state"""
    message = message or "Auto state publish"

    if not flox.local.flow:
        raise WorkflowException("No active flow, you need to start one before publishing changes")

    execute_stages(flox, "workflow_publish", **flox.local.flow, message=message)


@flox_workflow.command()
@click.pass_obj
def finish(flox: Flox):
    """Finish implementation"""
    if not flox.local.flow:
        raise WorkflowException("No active flow, you need to start one before finishing")

    execute_stages(flox, "workflow_finish", **flox.local.flow)
    flox.local.flow = None
