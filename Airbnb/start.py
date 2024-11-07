import os
#Create an empty virtual environment
if not os.path.isdir('.venv'):
    command = 'python3 -m venv .venv'
    os.system(command)
    print('.venv is now created')
else: print('.venv already exists. ')

#Activate virtual environment and install all the needed libraries
command = 'source .venv/bin/activate && pip install -r requirements.txt'
os.system(command)
print('libraries are now installed')

#start streamlit
command = 'source .venv/bin/activate && streamlit run main.py'
os.system(command)
