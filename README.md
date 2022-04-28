# SmokeyNet Engineering

## Getting Started

1. Ensure python3 installed:<br>
   `python --version`

2. With git installed, clone project:<br>
   `git clone git@github.com:shaneluna/smokeynet-engineering.git`

   _Note: You may need to setup an ssh key if first time using git_

3. Change directory into cloned repo:<br>
   `cd smokeynet-engineering`

4. Create a virtual environment:<br>
   `python -m venv venv`

5. Start virutal environment:<br>
   Linux & Mac:<br>
   `source venv/bin/activate`<br><br>
   Windows:<br>
   `./venv/Scripts/activate`

6. Install requirements:<br>
   `pip install -r requirements.txt`

7. Run the following to fix jupyter lab code formatter:<br>
   `jupyter server extension enable --py jupyterlab_code_formatter`

## Coding Standards

- black python formatting<br>

VS Code:<br>
Code > Preferences > Settings > Search `python formatting provider` > Select `black` > Search `format on save` > Check box for `Editor: Format on Save`<br>

JupyterLab:<br>
[JupyterLab Code Formatter](https://jupyterlab-code-formatter.readthedocs.io/en/latest/) has beeng added by default with black and isort formatting.<br>
Make sure to update on save options within JupyterLab: Settings > Advanced Settings Editor > JSON Settings Editor > Jupyterlab Code Formatter > Add the following to User Preferences:<br>
`{ "formatOnSave": true }`
