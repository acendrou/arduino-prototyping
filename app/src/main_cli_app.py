from core.frontends.cli import CliState
from core.misc.app import App


def main_app_cli():
    cli_state = CliState()
    cli_state.parser()

    app = App()

    # cli options
    # app.console.set_monitors_parameters(monitor_port=cli_state.monitorPort, monitor_speed=cli_state.monitorSpeed)
    app.console.is_raw_output_saved = cli_state.is_raw_output_saved
    app.console.raw_output_path = cli_state.raw_output_path
    app.run()


if __name__ == '__main__':
    main_app_cli()
