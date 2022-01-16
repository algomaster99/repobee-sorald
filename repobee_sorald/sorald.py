"""An example plugin command."""
import repobee_plug as plug


class HelloWorld(plug.Plugin, plug.cli.Command):
    def command(self):
        plug.echo("Hello, world!")
