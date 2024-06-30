from view.cliView import CLIView, BaseView


def main():
    view: BaseView = CLIView()
    view.run_app()



if __name__ == '__main__':
    main()
