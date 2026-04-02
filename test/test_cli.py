from unittest import mock
from rbuild.cli import get_rocm_path

def test_get_rocm_path_from_env(monkeypatch):
    monkeypatch.setenv('ROCM_PATH', '/custom/rocm')
    assert get_rocm_path() == '/custom/rocm'

def test_get_rocm_path_env_over_glob(monkeypatch):
    monkeypatch.setenv('ROCM_PATH', '/custom/rocm')
    with mock.patch('glob.glob', return_value=['/opt/rocm-5.0']):
        assert get_rocm_path() == '/custom/rocm'

def test_get_rocm_path_single_glob(monkeypatch):
    monkeypatch.delenv('ROCM_PATH', raising=False)
    with mock.patch('glob.glob', return_value=['/opt/rocm-5.0']):
        assert get_rocm_path() == '/opt/rocm-5.0'

def test_get_rocm_path_multiple_globs(monkeypatch):
    monkeypatch.delenv('ROCM_PATH', raising=False)
    with mock.patch('glob.glob', return_value=['/opt/rocm-5.0', '/opt/rocm-6.0']):
        assert get_rocm_path() == '/opt/rocm'

def test_get_rocm_path_no_glob(monkeypatch):
    monkeypatch.delenv('ROCM_PATH', raising=False)
    with mock.patch('glob.glob', return_value=[]):
        assert get_rocm_path() == '/opt/rocm'
