import pytest

import timerbot

_TEST_VERSION_ = "Version 1.5"  # This version goes together with the timerbot.py version they should be the same


def test_timerbot_main_without_token_parameter_expect_exception():
    with pytest.raises(Exception) as e_info:
        timerbot.main()


def test_timerbot_version():
    assert timerbot._BOT_VERSION_ == _TEST_VERSION_, "Check the timerbot.py version number should be the same as this test file"


def test_bot_started_datetime():
    import datetime
    assert timerbot._BOT_START_DATETIME_ < datetime.datetime.now()


def test_bot_started_time():
    import time
    assert timerbot._BOT_START_TIME_ < time.time()


def test_timerbot_name():
    assert timerbot._BOT_NAME_ == "Timerbot"


def test_meminfo_expected_keys():
    assert 'MemTotal' in timerbot.meminfo()
    assert 'MemFree' in timerbot.meminfo()
    assert 'MemAvailable' in timerbot.meminfo()
    assert 'Buffers' in timerbot.meminfo()


@pytest.mark.skip("Counters not implemented yet")
def test_send_and_receive_counters():
    assert 1 == 0


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
