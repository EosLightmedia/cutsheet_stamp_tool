import os
import venv
import subprocess


def create_virtual_env(dir_name):
    if not os.path.exists(dir_name):
        venv.create(dir_name, with_pip=True)
        print(f"The virtual environment was created in the {dir_name} directory.")

        # Activate the venv and install requirements
        activate_script = fr'{dir_name}/bin/activate_this.py'
        with open(activate_script) as f:
            exec(f.read(), {'__file__': activate_script})

        subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    else:
        print(f"The {dir_name} directory already exists.")


create_virtual_env('.venv')
