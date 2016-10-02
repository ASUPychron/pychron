#!/usr/bin/env bash
# This script is used to install pychron
# First in downloads and installs miniconda
# miniconda is used to manage the python dependencies
# conda is used to create a new environment
# conda and pip are used to install the dependencies
# a Pychron support directory is created and some boilerplate support files are written
# the pychron source code is downloaded from the available releases stored at github
#    (i.e the source is not a git clone just a static directory)
# if update_flag is set then clone the repository into .pychron/updates/
# the source code is stored in the Pychron support directory
# a launcher script is created and copied to the desktop

# =========== User Questions ==============
default=NMGRL
echo -n "Github organization [$default] >> "
read go
[ -z "$go" ] && go=$default

default=nmgrluser
echo -n "Github user name [$default] >> "
read gu
[ -z "$gu" ] && gu=$default

echo -n "Github password for ${gu} >> "
read gp

default=16
echo -n "MassSpec Database Version [$default] >> "
read dbv
[ -z "$dbv" ] && dbv=$default

default=NMGRL
echo -n "Pychron Fork [$default] >> "
read pychron_fork
[ -z "$pychron_fork" ] && pychron_fork=$default

default=release/v16.7
echo -n "Pychron Version [$default] >> "
read pychron_release
[ -z "$pychron_release" ] && pychron_release=$default

default=yes
echo -n "Make a MacOSX application [$default] >> "
read use_app_bundle
[ -z "$use_app_bundle" ] && use_app_bundle=$default

if [[ ${use_app_bundle} == "yes" ]]
then
  default=Pychron
  echo -n "Application name [$default] >> "
  read app_name
  [ -z "$app_name" ] && app_name=$default
fi



# =========== Configuration ===============
WORKING_DIR=~/pychron_install_wd

MINICONDA_URL=https://repo.continuum.io/miniconda/Miniconda-latest-MacOSX-x86_64.sh
MINICONDA_INSTALLER_SCRIPT=miniconda_installer.sh
MINICONDA_PREFIX=$HOME/miniconda2

CONDA_ENV=pychron
DOWNLOAD_URL=https://github.com/NMGRL/pychron/archive/v3.tar.gz

PYCHRONDATA_PREFIX=~/Pychron
ENTHOUGHT_DIR=$HOME/.enthought
PREFERENCES_ROOT=pychron.view.application.root

USE_UPDATE=1

LAUNCHER_SCRIPT_PATH=pychron_launcher.sh
APPLICATION=pyview_debug
PYCHRON_GIT_SOURCE_URL=https://github.com/{$pychron_fork}/pychron.git

PYCHRON_PATH=${PYCHRONDATA_PREFIX}/src

ICON_NAME=pyexperiment_icon.icns

CONDA_REQ="qt=4.8.5
statsmodels
scikit-learn
PyYAML
traits
traitsui
chaco
enable
pyface
envisage
sqlalchemy
Reportlab
lxml
xlrd
xlwt
pip
PySide
matplotlib
PyMySQL=0.6.6
requests
keyring
pil
paramiko"

PIP_REQ="uncertainties
pint
GitPython
peakutils
qimage2ndarray"

# =========== Setup Working dir ===========
cd

if ! [ -e ${WORKING_DIR} ]
 then
  echo Making working directory
  mkdir ${WORKING_DIR}
fi
cd ${WORKING_DIR}

# =========== Conda =======================
# check for conda
if type ${MINICONDA_PREFIX}/bin/conda >/dev/null
then
    # update conda
    echo conda already installed
    ${MINICONDA_PREFIX}/bin/conda update --yes conda
    echo Conda Updated
else
    echo conda doesnt exist
    # install conda

     # download miniconda installer script
     if ! [ -e ./${MINICONDA_INSTALLER_SCRIPT} ]
     then
         echo Downloading conda
        curl -L ${MINICONDA_URL} -o ${MINICONDA_INSTALLER_SCRIPT}
     fi

     chmod +x ./${MINICONDA_INSTALLER_SCRIPT}

     echo Installing conda. This may take a few minutes. Please be patient
     ./${MINICONDA_INSTALLER_SCRIPT} -b

     echo Conda Installed
     ${MINICONDA_PREFIX}/bin/conda update --yes conda
     echo Conda Updated
fi

${MINICONDA_PREFIX}/bin/conda create --yes -n${CONDA_ENV} pip

# install requirements
${MINICONDA_PREFIX}/envs/${CONDA_ENV}/bin/conda install -n${CONDA_ENV} --yes ${CONDA_REQ}
${MINICONDA_PREFIX}/envs/${CONDA_ENV}/bin/pip install ${PIP_REQ}

# =========== Support files ================
# make root
if [ -d ${PYCHRONDATA_PREFIX} ]
then
    echo ${PYCHRONDATA_PREFIX} already exists
else
    echo Making root directory ${PYCHRONDATA_PREFIX}
    mkdir ${PYCHRONDATA_PREFIX}
    mkdir ${PYCHRONDATA_PREFIX}/setupfiles
    mkdir ${PYCHRONDATA_PREFIX}/preferences

    cat ${PYCHRONDATA_PREFIX}/preferences/dvc.ini << EOF
[pychron.dvc]
organization=NMGRLData
meta_repo_name=MetaData
EOF

    cat ${PYCHRONDATA_PREFIX}/setupfiles/initialization.xml << EOF
<root>
  <globals>
  </globals>
  <plugins>
    <general>
      <plugin enabled='true'>ArArConstants</plugin>
      <plugin enabled='true'>DVC</plugin>
      <plugin enabled='true'>GitHub</plugin>
      <plugin enabled='true'>Pipeline</plugin>
      <plugin enabled='true'>Update</plugin>
    </general>
    <hardware>
    </hardware>
    <data>
    </data>
    <social>
      <plugin enabled='false'>Email</plugin>
      <plugin enabled='false'>Twitter</plugin>
    </social>
  </plugins>
</root>
EOF

    cat ${PYCHRONDATA_PREFIX}/setupfiles/startup_tests.yaml << EOF
- plugin: ArArConstantsPlugin
  tests:
- plugin: DVC
  tests:
    - test_database
    - test_dvc_fetch_meta
- plugin: GitHub
  tests:
    - test_api
EOF

fi

# ========= Enthought directory ============
if [ -d ${ENTHOUGHT_DIR} ]
then
    echo ${ENTHOUGHT_DIR} already exists
else
    echo Making root directory ${ENTHOUGHT_DIR}
    mkdir ${ENTHOUGHT_DIR}
fi

# ============== Install Pychron source ==============
if [[ ${USE_UPDATE} == "1" ]]
then
    if [ -d ~/.pychron/ ]
        then
            if [ ! -d ~/.pychron/updates ]
            then
               mkdir ~/.pychron/updates
            fi
        else
            mkdir ~/.pychron/
            mkdir ~/.pychron/updates
        fi
    git clone ${PYCHRON_GIT_SOURCE_URL} --branch=${pychron_release} ~/.pychron/updates
    PYCHRON_PATH=~/.pychron/updates
else
    # =========== Unpack Release ===============
    cd ${PYCHRONDATA_PREFIX}
    mkdir ./src
    curl -L ${DOWNLOAD_URL} -o pychron_src.tar.gz
    tar -xf ./pychron_src.tar.gz -C ./src --strip-components=1
fi

# ========== Launcher Script ===============
touch ${LAUNCHER_SCRIPT_PATH}

echo export GITHUB_ORGANIZATION=${go} >> ${LAUNCHER_SCRIPT_PATH}
echo export GITHUB_USER=${gu} >> ${LAUNCHER_SCRIPT_PATH}
echo export GITHUB_PASSWORD=${gp} >> ${LAUNCHER_SCRIPT_PATH}
echo export MassSpecDBVersion=${dbv} >> ${LAUNCHER_SCRIPT_PATH}

echo ROOT=${PYCHRON_PATH} >> ${LAUNCHER_SCRIPT_PATH}

echo ENTRY_POINT=\$ROOT/launchers/${APPLICATION}.py >> ${LAUNCHER_SCRIPT_PATH}
echo export PYTHONPATH=\$ROOT >> ${LAUNCHER_SCRIPT_PATH}

echo ${MINICONDA_PREFIX}/envs/${CONDA_ENV}/bin/python.app \$ENTRY_POINT >> ${LAUNCHER_SCRIPT_PATH}
if [[ ${use_app_bundle} == "1" ]]
then
  #  Create the app bundle
  APPNAME=${app_name}
  DIR="${APPNAME}.app/Contents/MacOS";
  mkdir -p "${DIR}";

  cp "${LAUNCHER_SCRIPT_PATH}" "${DIR}/${APPNAME}";
  chmod +x "${DIR}/${APPNAME}";

  mkdir -p "${APPNAME}.app/Contents/Resources";

  # write plist
  PLIST="${APPNAME}.app/Contents/Info.plist"
  touch ${PLIST}
   printf "<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>CFBundleIconFile</key><string>${ICON_NAME}</string>
</dict>
</plist>
" > ${PYCHRONDATA_PREFIX}/preferences/dvc.ini
  # copy info file
else
  chmod +x ${LAUNCHER_SCRIPT_PATH}
  cp ${LAUNCHER_SCRIPT_PATH} ~/Desktop/
fi
# ============= EOF =============================================
