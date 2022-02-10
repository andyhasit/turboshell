#!/bin/bash
#
# This script installs turboshell.
#
# It can be run via:
#
#   curl:
#      bash -c "$(curl -fsSL https://raw.githubusercontent.com/andyhasit/turboshell/master/scripts/install.sh)"
#   wget:
#      bash -c "$(wget -qO- https://raw.githubusercontent.com/andyhasit/turboshell/master/scripts/install.sh)"
#   fetch:
#      bash -c "$(fetch -o - https://raw.githubusercontent.com/andyhasit/turboshell/master/scripts/install.sh)"
#
# Or you can download it and run it yourself:
#
#   bash install.sh


#
# Detect whether we're in  bash or zsh
#
if [ -n "`$SHELL -c 'echo $ZSH_VERSION'`" ]; then
  RC_FILE=$HOME/.zshrc
elif [ -n "`$SHELL -c 'echo $BASH_VERSION'`" ]; then
  RC_FILE=$HOME/.bashrc
else
  RC_FILE=''
fi

#
# Create turboshell directory and cd into it
#
echo "Turboshell will create a directory here:"
echo
echo "    $HOME/turboshell"
echo
echo "Hit ENTER to accept, or provide a different path:"
read -p ">" location
TURBOSHELL_USER_DIR=${location:-~/turboshell}
TURBOSHELL_USER_DIR="${TURBOSHELL_USER_DIR/#\~/$HOME}"
mkdir -p $TURBOSHELL_USER_DIR
cd $TURBOSHELL_USER_DIR

#
# Check python version in that directory is > 3.6
#
if ! python3 -c 'import sys; assert sys.version_info >= (3,6)' > /dev/null; then
  echo 
  echo Error: python3 must point to a version of python 3.6 or above. 
  echo
  echo Recommended solution:
  echo
  echo "  1. Install pyenv https://github.com/pyenv/pyenv"
  echo "  2. Install a recent version of python:"
  echo
  echo "        $ pyenv install-latest"
  echo
  echo "     Keep note of the version (e.g. 3.7.5)"
  echo "  3. Create a virtualenv from that version and name it 'turboshell':"
  echo
  echo "        $ pyenv virtualenv 3.7.5 turboshell"
  echo
  echo "  4. Tell pyenv to use it in your directory:"
  echo
  echo "        $ cd ~/turboshell"
  echo "        $ pyenv local turboshell"
  echo
  echo "     Provided you installed pyenv correctly, it should activate that"
  echo "     environment whenever you enter that directory."
  echo "  5. Check it worked:"
  echo
  echo "        $ python -V"
  echo
  exit 1
fi


create_venv () {
  # if [ ! -d ".venv" ]; then
  #   echo Creating virtual environment at .venv
    
  # else
  #   echo Directory .venv already exists.
  # fi
  python3 -m venv .venv
  . .venv/bin/activate
  TURBOSHELL_VENV_DIR=$(python3 -c 'import sys; print(sys.prefix)')
}


prompt_install_venv () {
  echo "Shall we create a virtual env at .venv for you?"
  while true; do
    read -p "(yes/no)" yn
    case $yn in
        [Yy]* ) create_venv; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
  done
}

#
# Detect virtual env or prompt to create one.
#
if ! python3 -c 'import sys; assert sys.prefix != sys.base_prefix' > /dev/null; then
  echo "No virtual environment detected."
  prompt_install_venv
else
  TURBOSHELL_VENV_DIR=$(python3 -c 'import sys; print(sys.prefix)')
  echo "Using virtual environment detected at $TURBOSHELL_VENV_DIR"
fi

#
# Install turboshell
#
echo "Installing turboshell from pip"
pip install turboshell

#
# Create initial files
#
echo "Creating initial files"
python -m turboshell init

#
# Add lines to shell rc file
#
echo "\n" >> $RC_FILE
echo "# Turboshell variables:" >> $RC_FILE
echo "export TURBOSHELL_VENV_DIR=$TURBOSHELL_VENV_DIR" >> $RC_FILE
echo "export TURBOSHELL_USER_DIR=$TURBOSHELL_USER_DIR" >> $RC_FILE
echo "source \$TURBOSHELL_USER_DIR/build/definitions" >> $RC_FILE

#
# Source from rc file
#
. $RC_FILE