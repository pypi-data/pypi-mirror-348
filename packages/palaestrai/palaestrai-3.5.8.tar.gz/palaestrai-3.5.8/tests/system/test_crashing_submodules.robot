*** Settings ***
Documentation   Test handling of crashing submodules
...             palaestrAI runs user code in many places, all of which could
...             potentially crash. However, palaestrAI should handle this
...             gracefully. This test suite simulates crashes of various
...             submodules and validates palaestrAI's handling of the crashes.

Library         Process
Library         OperatingSystem
Library         String
Suite Teardown  Clean Files

*** Keywords ***
Clean Files
    Remove File                     stdout_crashme.txt
    Remove File                     stderr_crashme.txt
    Remove File                     ${TEMPDIR}${/}stdout_conf_crashme.txt
    Remove File                     ${TEMPDIR}${/}runtime_conf_crashme.yaml

Singularize Ports
    ${LOGPORT}                      Evaluate    str(24243 + random.randrange(1000 * (${PABOTQUEUEINDEX}+1)))
    ${EXECUTORPORT}                 Evaluate    str(24242 - random.randrange(1000 * (${PABOTQUEUEINDEX}+1)))
    ${result}                       Run Process         palaestrai  runtime-config-show-default  stdout=${TEMPDIR}${/}stdout_conf_crashme.txt
    ${conf} =                       Replace String      ${result.stdout}  4242  ${EXECUTORPORT}
    ${conf} =                       Replace String      ${conf}  4243  ${LOGPORT}
    Create File                     ${TEMPDIR}${/}runtime_conf_crashme.yaml  ${conf}

*** Test Cases ***
Test handling of crashing environments
    [Setup]                         Singularize Ports
    [Teardown]                      Clean Files
    ${pythonpath} =                 Get Environment Variable  PYTHONPATH  default=""
    Set Environment Variable        PYTHONPATH  ${pythonpath}:${CURDIR}${/}..
    Start Process                   palaestrai  -c  ${TEMPDIR}${/}runtime_conf_crashme.yaml  experiment-start  ${CURDIR}${/}..${/}fixtures${/}crashing_env_dummy_run.yml  stdout=${TEMPDIR}/stdout_crashme.txt  stderr=${TEMPDIR}/stderr_crashme.txt
    ${result} =                     Wait For Process  timeout=90  on_timeout=kill
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}  0
    ${match} =                      Should Match Regexp  ${result.stdout}   RuntimeError: Mwaaaahhhrgh!!
    ${match} =                      Should Match Regexp  ${result.stdout}   Execution of RunGovernor[^ ]* failed:
