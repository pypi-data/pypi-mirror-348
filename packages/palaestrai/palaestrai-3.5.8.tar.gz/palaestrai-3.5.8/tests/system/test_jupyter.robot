*** Settings ***
Documentation   Run palaestrAI from Jupyter Notebooks
...
...             The Jupyter Notebook kernel is a special environment for
...             palaestrAI to run it. This system test will run
...             jupyter nbconvert --execute for a given iPython notebook in
...             which a palaestrAI experiment is executed.

Library         Process
Library         OperatingSystem
Suite Teardown   Clean Files

*** Keywords ***
Clean Files
    Remove File                     ${TEMPDIR}${/}stdout_jupyter.txt
    Remove File                     ${TEMPDIR}${/}stderr_jupyter.txt

*** Test Cases ***
Dummy experiment run from a Jupyter Notebook
    [Timeout]                       300
    ${result} =                     Run Process    jupyter  nbconvert    --to    html   --execute   ${CURDIR}${/}test_palaestrai_jupyter.ipynb    stdout=${TEMPDIR}${/}stdout_jupyter.txt     stderr=${TEMPDIR}${/}stderr_jupyter.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}   0
    File Should Exist               ${CURDIR}${/}test_palaestrai_jupyter.html
