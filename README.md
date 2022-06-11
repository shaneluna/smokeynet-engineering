# SmokeyNet Engineering
This project was created for wildfire smoke detection analysis, and aims to improve upon a smoke detection model, SmokeyNet, originally built by the San Diego Supercomputer Center at UCSD.

**Note**: Processed data may change over time depending on latest camera/weather station updates and if the configured timeframe is changed.

## Getting Started

1. Ensure dependencies installed:
- python3

2. With git installed, clone project:
   ```
   git clone git@github.com:shaneluna/smokeynet-api.git
   ```

   _Note: You may need to setup an ssh key if first time using git_

3. Change directory into cloned repo:
   ```
   cd smokeynet-api
   ```

4. Create a virtual environment:
   ```
   python -m venv venv
   ```

5. Start virutal environment:<br>
   Linux & Mac:
   ```
   source venv/bin/activate
   ```
   Windows:
   ```
   ./venv/Scripts/activate
   ```

6. Install requirements:
   ```
   pip install -r requirements.txt
   ```

7. Run the following to fix jupyter lab code formatter:
   ```
   jupyter server extension enable --py jupyterlab_code_formatter
   ```

## Naming Standards

- All folder names + filenames should be lowercase
    - 1 exception is for README files
- All folder names + filesnames should be snakecase

- Required notebooks for data getting/processing should have #_ prefix<br>
`I.e. 1_process_camera_metadata.ipynb`
- Save prefix 0_ for notebooks that retrieve initial raw data<br>
`I.e. 0_get_camera_metadata.ipynb`


## Coding Standards

- black python formatting<br>

VS Code:<br>
Code > Preferences > Settings > Search `python formatting provider` > Select `black` > Search `format on save` > Check box for `Editor: Format on Save`<br>

JupyterLab:<br>
[JupyterLab Code Formatter](https://jupyterlab-code-formatter.readthedocs.io/en/latest/) has beeng added by default with black and isort formatting.<br>
Make sure to update on save options within JupyterLab: Settings > Advanced Settings Editor > JSON Settings Editor > Jupyterlab Code Formatter > Add the following to User Preferences:<br>
`{ "formatOnSave": true }`
