import inquirer
from inquirer import themes
from clarity_cli.exceptions import StopCommand
from clarity_cli.outputs import CliOutput

out = CliOutput()


class CliInputs():

    def ask_for_confirmation(self, confirmation_message, default=True, hard_stop=False):
        questions = [
            inquirer.Confirm('confirm', message=f"{confirmation_message}", default=default)]

        answers = inquirer.prompt(questions, theme=themes.GreenPassion())
        if not answers:
            out.vprint("Command was canceled")
            raise StopCommand()
        if hard_stop and not answers['confirm']:
            out.vprint("Command was not confirmed")
            raise StopCommand()
        return answers['confirm']

    def ask_for_input_from_list(self, message, options: list):
        questions = [inquirer.List('list_input', message=message, choices=options)]
        answers = inquirer.prompt(questions, theme=themes.GreenPassion())
        if not answers or not answers['list_input']:
            out.warning("Command was canceled")
            raise StopCommand()
        return answers.get('list_input')

    def ask_for_text_input(self, message, default="", optional=False):
        final_message = f"{message} [Optional]" if optional else message
        questions = [inquirer.Text('text_input', message=final_message, default=default)]
        answers = inquirer.prompt(questions, theme=themes.Default())
        if not answers or (optional and not answers['text_input']):
            out.warning("Command was canceled")
            raise StopCommand()
        return answers.get('text_input')

    def ask_for_password_input(self, message):
        questions = [inquirer.Password('pass_input', message=message)]
        answers = inquirer.prompt(questions, theme=themes.Default())
        if not answers or not answers['pass_input']:
            out.warning("Command was canceled")
            raise StopCommand()
        return answers.get('pass_input')
