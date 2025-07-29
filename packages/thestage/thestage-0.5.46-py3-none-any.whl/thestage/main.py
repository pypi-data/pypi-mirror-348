from thestage.services.core_files.config_entity import ConfigEntity

# TODO use this in config_provider
initial_config: ConfigEntity = ConfigEntity()

def main():
    try:
        import warnings
        warnings.filterwarnings(action='ignore', module='.*paramiko.*')

        from . import __app_name__

        from thestage.controllers import base_controller, container_controller, instance_controller, project_controller, \
            config_controller

        base_controller.app.add_typer(project_controller.app, name="project")
        base_controller.app.add_typer(container_controller.app, name="container")
        base_controller.app.add_typer(instance_controller.app, name="instance")
        base_controller.app.add_typer(config_controller.app, name="config")

        import thestage.config
        base_controller.app(prog_name=__app_name__)
    except KeyboardInterrupt:
        print('THESTAGE: Keyboard Interrupt')
