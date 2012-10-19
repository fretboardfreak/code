#!/bin/bash

SCRIPT=$0

# Turn on debug output
DEBUG=0

# Turn on integration with Fret's virtualenv.sh environment config
USE_VIRTUALENV_SH=1

usage () {
    # Ruler 80 chars
    #       |--------------------------------------------------------------------------------|
    echo -e "Usage: $SCRIPT [-h|--help] [options] ENV_NAME"
    echo -e "\n  $SCRIPT creates python virtual environments\n"
    echo -e "Options:"
    echo -e "  -h|--help                   : print this message"
    echo -e "  -i|--interpreter PYEXEC     : choose the python executable to configure"
    echo -e "  -p|--prompt PROMPT          : choose the prompt string"
    echo -e "  -r|--req-file PIPREQ    : Requirements file for pip"
    exit 1
};

parseOpts () {
    #echo -e "Args for parsOpts:\n$@\n"

    # Options with no args have no colon
    # Option with required arg has 1 colon
    # Option with optional arg has 2 colons
    ARGS=`getopt --options "dhi:p:r:" \
                 --long "help,interpreter:,prompt:,req-file:" \
                 --name "$SCRIPT" -- "$@"`

    if [ $? -ne 0 ]; then
        # bad arguments found
        usage;
        exit 1;
    fi
    eval set -- "$ARGS"

    while true ; do
        case "$1" in
            -h|--help) usage ; shift ; continue ;;
            -d) DEBUG=1 ; shift ;;
            -i|--interpreter) PYEXEC="--python $2"; shift 2 ; continue ;;
            -p|--prompt) PROMPT="--prompt $2" ; shift 2 ; continue ;;
            -r|--req-file) PIPREQ="$2" ; shift 2 ; continue ;;
            --) shift ; break ;;
            *) echo "not recognized $1" ; exit 1 ;;
        esac
    done

    if [[ $# -eq 1 ]]; then
        ENV_NAME=$1
    else
        echo "No ENV_NAME found, exiting..."
        exit 1
    fi
}

debug () {
    echo "Debug info:"
    echo "  pwd=$PWD"
    echo "  envname=$ENV_NAME"
    echo "  pyexec=$PYEXEC"
    echo "  prompt=$PROMPT"
    echo "  pipreq=$PIPREQ"
}

createEnv () {
    echo -e "Creating Virtual Environment..."
    if [[ $USE_VIRTUALENV_SH -eq 1 ]] ; then
        pushd $VIRTUALENV_DIR
        virtualenv $PROMPT $PYEXEC $ENV_NAME
        popd
    else
        exec echo "createEnv not implemented for non virtualenv.sh compatible mode"
    fi
};

runPipInstall () {
    if [[ -z $PIPREQ ]] ; then
        echo "Skipping pip install because PIPREQ is empty"
        exit 1;
    fi
    echo -e "Running pip Install..."
    if [[ $USE_VIRTUALENV_SH -eq 1 ]] ; then
        $VIRTUALENV_DIR$ENV_NAME/bin/pip install -r $PIPREQ
    else
        exec echo "runPipInstall not implemented for non virtualenv.sh compatible mode"
    fi
};

# ---- Main ----

parseOpts $@

if [[ DEBUG -eq 1 ]] ; then
    debug ;
fi

createEnv ;
runPipInstall ;
