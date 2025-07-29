"""tests for module runner.py."""

import pathlib
import subprocess
import tomllib
import uuid
from unittest import mock

import pytest

from pysdccc._result_parser import TestSuite
from pysdccc._runner import (
    DIRECT_TEST_RESULT_FILE_NAME,
    INVARIANT_TEST_RESULT_FILE_NAME,
    SdcccRunner,
    SdcccRunnerAsync,
    _BaseRunner,
    check_requirements,
)


def test_check_requirements():
    """Test that the requirements are correctly checked against the provided requirements."""
    provided = {'biceps': {'b1': True}}
    available = {'biceps': {'b1': True, 'b2': True}}
    check_requirements(provided, available)

    provided['biceps']['b3'] = True
    with pytest.raises(KeyError):
        check_requirements(provided, available)

    provided['biceps']['b3'] = False
    check_requirements(provided, available)

    provided['mdpws'] = {}
    provided['mdpws']['m1'] = True
    with pytest.raises(KeyError):
        check_requirements(provided, available)

    provided['mdpws']['m1'] = False
    with pytest.raises(KeyError):
        check_requirements(provided, available)


def test_sdccc_runner_init():
    """Test that the SdcccRunner is correctly initialized and raises ValueError for relative paths."""
    with pytest.raises(ValueError, match='Path to test run directory must be absolute'):
        _BaseRunner(pathlib.Path(), pathlib.Path(__file__))
    with pytest.raises(ValueError, match='Path to executable must be absolute'):
        _BaseRunner(pathlib.Path().absolute(), pathlib.Path())
    runner = _BaseRunner(pathlib.Path().absolute(), pathlib.Path(__file__))
    assert runner.exe == pathlib.Path(__file__).absolute()
    assert runner.test_run_dir == pathlib.Path().absolute()
    with pytest.raises(ValueError, match='Path to requirements file must be absolute'):
        runner._prepare_command(config=pathlib.Path().absolute(), requirements=pathlib.Path())  # noqa: SLF001
    with pytest.raises(ValueError, match='Path to config file must be absolute'):
        runner._prepare_command(config=pathlib.Path(), requirements=pathlib.Path().absolute())  # noqa: SLF001


def test_sdccc_runner_check_requirements():
    """Test that the SdcccRunner correctly checks the requirements."""
    runner = _BaseRunner(
        pathlib.Path().absolute(),
        pathlib.Path(__file__).parent.joinpath('testversion').joinpath('sdccc.exe').absolute(),
    )
    with mock.patch('pysdccc._runner._BaseRunner.check_requirements') as mock_check_requirements:
        runner.check_requirements(pathlib.Path('requirements.toml'))
        mock_check_requirements.assert_called_once()


def test_configuration():
    """Test that the SdcccRunner correctly loads the configuration from the SDCcc executable's directory."""
    run = _BaseRunner(
        pathlib.Path().absolute(),
        pathlib.Path(__file__).parent.joinpath('testversion/sdccc.exe').absolute(),
    )
    loaded_config = run.get_config()
    provided_config = """
[SDCcc]
CIMode=false
GraphicalPopups=true
TestExecutionLogging=true
EnableMessageEncodingCheck=true
SummarizeMessageEncodingErrors=true

[SDCcc.TLS]
FileDirectory="./configuration"
KeyStorePassword="whatever"
TrustStorePassword="whatever"
ParticipantPrivatePassword="dummypass"
EnabledProtocols = ["TLSv1.2", "TLSv1.3"]
EnabledCiphers = [
    # TLS 1.2
    "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
    "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
    "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
    "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256",
    "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384",
    # TLS 1.3
    "TLS_AES_128_GCM_SHA256",
    "TLS_AES_256_GCM_SHA384",
]

[SDCcc.Network]
InterfaceAddress="127.0.0.1"
MaxWait=10
MulticastTTL=128

[SDCcc.Consumer]
Enable=true
DeviceEpr="urn:uuid:857bf583-8a51-475f-a77f-d0ca7de69b11"
# DeviceLocationBed="bed32"
# DeviceLocationPointOfCare="poc32"
# etc.

[SDCcc.Provider]
Enable=false

[SDCcc.gRPC]
ServerAddress="localhost:50051"

[SDCcc.TestParameter]
Biceps547TimeInterval=5
    """
    assert tomllib.loads(provided_config) == loaded_config


def test_requirements():
    """Test that the SdcccRunner correctly loads the requirements from the SDCcc executable's directory."""
    run = SdcccRunner(
        pathlib.Path().absolute(),
        pathlib.Path(__file__).parent.joinpath('testversion/sdccc.exe').absolute(),
    )
    loaded_config = run.get_requirements()
    provided_config = """
[MDPWS]
R0006=false
R0008=true
R0010=true
R0011=true
R0012=true
R0013=true
R0014=true
R0015=true

[BICEPS]
R0007_0=true
R0021=true
R0023=true
R0025_0=true
R0029_0=true
R0033=true
R0034_0=true
R0038_0=true
R0055_0=false
R0062=true
R0064=true
R0066=true
R0068=true
R0069=true
R0097=true
R0098_0=true
R0100=false
R0101=true
R0104=true
R0105_0=true
R0116=true
R0119=false
R0124=true
R0125=true
R0133=true
R5003=true
R5006=true
B-6_0=true
B-128=false
B-284_0=true
B-402_0=true
C-5=true
C-7=true
C-11=true
C-12=true
C-13=true
C-14=true
C-15=true
C-55_0=true
C-62=true
R5024=true
R5025_0=true
R5039=true
R5040=true
R5041=true
R5042=true
R5046_0=true
R5051=true
R5052=true
R5053=true
5-4-7_0_0=true
5-4-7_1=true
5-4-7_2=true
5-4-7_3=true
5-4-7_4=true
5-4-7_5=true
5-4-7_6_0=true
5-4-7_7=true
5-4-7_8=true
5-4-7_9=true
5-4-7_10=true
5-4-7_11=true
5-4-7_12_0=true
5-4-7_13=true
5-4-7_14=true
5-4-7_15=true
5-4-7_16=true
5-4-7_17=true

[DPWS]
R0001=false
R0013=false
R0019=false
R0031=false
R0034=false
R0040=false

[GLUE]
13=true
8-1-3=true
R0010_0=true
R0011=true
R0012_0_0=true
R0013=false
R0034_0=true
R0036_0=true
R0042_0=true
R0056=true
R0072=false
R0078_0=true
R0080=true
    """
    assert tomllib.loads(provided_config) == loaded_config


def test_parse_result():
    """Test that the SdcccRunner correctly parses the test results from the SDCcc executable's directory."""
    invariant = (
        (
            'BICEPS.R6039',
            'Sends a get context states message with empty handle ref and verifies that the response '
            'contains all context states of the mdib.',
        ),
        (
            'BICEPS.R6040',
            'Verifies that for every known context descriptor handle the corresponding context states are returned.',
        ),
        (
            'BICEPS.R6041',
            'Verifies that for every known context state handle the corresponding context state is returned.',
        ),
        ('SDCccTestRunValidity', 'SDCcc Test Run Validity'),
    )
    direct = (
        (
            'MDPWS.R5039',
            'Sends a get context states message with empty handle ref and verifies that the response '
            'contains all context states of the mdib.',
        ),
        (
            'MDPWS.R5040',
            'Verifies that for every known context descriptor handle the corresponding context states are returned.',
        ),
        (
            'MDPWS.R5041',
            'Verifies that for every known context state handle the corresponding context state is returned.',
        ),
        ('SDCccTestRunValidity', 'SDCcc Test Run Validity'),
    )
    run = _BaseRunner(
        pathlib.Path(__file__).parent.joinpath('sdccc_example_results').absolute(), pathlib.Path(__file__).absolute()
    )
    direct_results = run._get_result(DIRECT_TEST_RESULT_FILE_NAME)  # noqa: SLF001
    invariant_results = run._get_result(INVARIANT_TEST_RESULT_FILE_NAME)  # noqa: SLF001

    def verify_suite(suite: TestSuite | None, data: tuple[tuple[str, str], ...]):
        assert isinstance(suite, TestSuite)
        assert len(data) == len(suite)

    verify_suite(direct_results, direct)
    verify_suite(invariant_results, invariant)


def test_sdccc_runner_version():
    """Test that the SdcccRunner correctly loads the version."""
    runner = SdcccRunner(pathlib.Path().absolute(), pathlib.Path(__file__).absolute())
    version = uuid.uuid4().hex
    with mock.patch('subprocess.run') as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout=version.encode(), stderr=b'')
        assert runner.get_version() == version

    # test exception handling
    returncode = int(uuid.uuid4())
    stdout = uuid.uuid4().hex.encode()
    stderr = uuid.uuid4().hex.encode()
    with mock.patch('subprocess.Popen') as mock_popen:
        mock_popen.return_value.__enter__.return_value.communicate.return_value = stdout, stderr
        mock_popen.return_value.__enter__.return_value.poll.return_value = returncode
        with pytest.raises(subprocess.CalledProcessError) as e:
            assert runner.get_version() == ''
    assert e.value.returncode == returncode
    assert e.value.stdout == stdout
    assert e.value.stderr == stderr


@pytest.mark.asyncio
async def test_sdccc_runner_version_async():
    """Test that the SdcccRunner correctly loads the version."""
    runner = SdcccRunnerAsync(pathlib.Path().absolute(), pathlib.Path(__file__).absolute())
    version = uuid.uuid4().hex
    with mock.patch('anyio.run_process') as mock_process:
        completed_process_mock = mock.MagicMock()
        completed_process_mock.stdout = version.encode()
        mock_process.return_value = completed_process_mock
        assert await runner.get_version() == version

    # test exception handling
    returncode = int(uuid.uuid4())
    stdout = uuid.uuid4().hex.encode()
    stderr = uuid.uuid4().hex.encode()

    def _side_effect(*_, **__):  # noqa: ANN002, ANN003
        raise subprocess.CalledProcessError(returncode=returncode, cmd='', output=stdout, stderr=stderr)

    with (
        mock.patch('anyio.run_process', side_effect=_side_effect) as mock_process,
        pytest.raises(subprocess.CalledProcessError) as e,
    ):
        assert await runner.get_version() == ''
    assert e.value.returncode == returncode
    assert e.value.stdout == stdout
    assert e.value.stderr == stderr
    mock_process.assert_called_with([runner.exe, '--version'], check=True, cwd=runner.exe.parent)
