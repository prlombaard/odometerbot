import pytest

import timerbot

_VERSION_ = "Version 1.2"  # This version goes together with the timerbot.py version they should be the same


def test_timerbot_main_without_token_parameter_expect_exception():
    with pytest.raises(Exception) as e_info:
        timerbot.main()


def test_timerbot_version():
    assert timerbot._VERSION_ == "Version 1.2"


def test_timerbot_name():
    assert timerbot._BOT_NAME_ == "Timerbot"


def test_meminfo_expected_keys():
    assert 'MemTotal' in timerbot.meminfo()
    assert 'MemFree' in timerbot.meminfo()
    assert 'MemAvailable' in timerbot.meminfo()
    assert 'Buffers' in timerbot.meminfo()


@pytest.mark.skip()
def test_status_command():
    assert 1 == 0


@pytest.mark.skip()
def test_host_status_command():
    assert 1 == 0


@pytest.mark.skip()
def test_help_command():
    assert 1 == 0


@pytest.mark.skip()
def test_set_command():
    assert 1 == 0


@pytest.mark.skip()
def test_unsetall_command():
    assert 1 == 0


@pytest.mark.skip()
def test_list_command():
    assert 1 == 0


@pytest.mark.skip()
def test_alarm_command():
    assert 1 == 0


@pytest.mark.skip()
def test_respawn_command():
    assert 1 == 0


@pytest.mark.skip()
def test_error_reply():
    assert 1 == 0
