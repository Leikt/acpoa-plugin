import configparser
import glob
import os.path
import shutil


def new(args):
    def _create_target_dir():
        if os.path.isdir(args.path):
            if args.force_erase:
                shutil.rmtree(args.path)
                os.makedirs(args.path)
                print("* Target directory was existing, force deletion.")
            else:
                print("* Target directory already exists (use -F to erase it)")
        else:
            os.makedirs(args.path)
            print("* Target directory created")

    def _copy_defaults():
        print("* Copy default files...")
        default_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "default")
        files = []
        abs_paths = glob.glob(os.path.join(default_dir, "**", "*"), recursive=True)
        for path in abs_paths:
            rel_path = os.path.relpath(path, default_dir)
            final_path = os.path.join(args.path, rel_path)
            if os.path.isdir(path):
                if not os.path.isdir(final_path):
                    print(f" * Create directory '{final_path}'")
                    os.makedirs(final_path)
            else:
                if os.path.isfile(final_path):
                    if args.force_replace:
                        print(f" * Replace '{final_path}'")
                        os.remove(final_path)
                        shutil.copy(path, final_path)
                        files.append(final_path)
                    else:
                        print(f" * Skip '{final_path}'")
                else:
                    print(f" * Copy '{final_path}'")
                    shutil.copy(path, final_path)
                    files.append(final_path)
        return files

    def _config_setup():
        print("* Update 'setup.py'")
        # Load file
        setup_file = os.path.join(args.path, 'setup.py')
        with open(setup_file, 'r') as file:
            text = file.read()
        # Replace elements
        text = text.replace('____name____', args.name)
        text = text.replace('____version____', args.version)
        if args.author is not None:  text = text.replace('____author____', args.author)
        if args.author_email is not None:  text = text.replace('____author_email____', args.author_email)
        if args.description is not None:  text = text.replace('____description____', args.description)
        if args.url is not None:  text = text.replace('____url____', args.url)
        # Save file
        with open(setup_file, 'w') as file:
            file.write(text)

    def _config_config_file():
        print("* Update 'plugin.cfg'")
        config_file = os.path.join(args.path, "plugin.cfg")
        config = configparser.ConfigParser()
        config.add_section('metadata')
        config.set('metadata', 'name', args.name)
        config.set('metadata', 'pretty_name', str(args.pretty_name))
        with open(config_file, 'w') as file:
            config.write(file)

    print(f"Create new plugin directory at '{args.path}'")
    _create_target_dir()
    copied_files = _copy_defaults()
    if os.path.join(args.path, 'setup.py') in copied_files: _config_setup()
    if os.path.join(args.path, 'plugin.cfg') in copied_files: _config_config_file()


def new2(args):
    def _create_directories():
        # Create directory if needed
        if not os.path.isdir(args.path):
            print("* Create parent directories...")
            os.makedirs(args.path)
        # Can't create new plugin directory if it already exists
        if os.path.isdir(args.path):
            print(f" * Directory exists: {args.path}")
            if args.force_erase:
                print(" * Deleting existing directory...")
                shutil.rmtree(args.path)
            elif not args.force_replace:
                raise FileExistsError(f"Directory exists: {args.path}.\n"
                                      f"Use -F option to delete it before create the new one.\n"
                                      f"User -f option to only replace existing files.")

    def _copy_default():
        # Create temp directory
        temp_dir = '.temp-acpoa-plugin'
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)
        # Copy default plugin file
        default_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "default")
        shutil.copytree(default_dir, temp_dir)
        # Move default to wanted folder
        for e in os.listdir(temp_dir):
            if os.path.exists(e):
                print(f"{e} already exists...")
                if args.force_erase or args.force_replace:
                    if os.path.isfile(e):
                        os.remove(e)
                    elif os.path.isdir(e):
                        shutil.rmtree(e)
                    print(f"{e} erased")
            ename = os.path.join(temp_dir, e)
            shutil.move(ename, './')
            print(f"{e} created")
        # Remove temp directory
        shutil.rmtree(temp_dir)

    def _update_files():
        def _create_config():
            print(" * Create config file...")
            config_file = os.path.join(args.path, "plugin.cfg")
            config = configparser.ConfigParser()
            config.add_section('metadata')
            config.set('metadata', 'name', args.name)
            config.set('metadata', 'pretty_name', str(args.pretty_name))
            with open(config_file, 'w') as file:
                config.write(file)

        def _update_setup():
            print(" * Update setup.py...")
            # Load file
            setup_file = os.path.join(args.path, 'setup.py')
            with open(setup_file, 'r') as file:
                text = file.read()
            # Replace elements
            text = text.replace('____name____', args.name)
            text = text.replace('____version____', args.version)
            if args.author is not None:  text = text.replace('____author____', args.author)
            if args.author_email is not None:  text = text.replace('____author_email____', args.author_email)
            if args.description is not None:  text = text.replace('____description____', args.description)
            if args.url is not None:  text = text.replace('____url____', args.url)
            # Save file
            with open(setup_file, 'w') as file:
                file.write(text)

        # Modify plugin directory files with the given parameters
        print("* Modify files to match given informations...")
        # Create configuration file
        _create_config()
        # Update setup.py file
        _update_setup()

    print("Create new plugin directory...")
    _create_directories()
    _copy_default()
    _update_files()
    print("Done")
