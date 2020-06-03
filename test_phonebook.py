import pytest

from phonebook import PhoneBook


@pytest.fixture
def pb():
    pb = PhoneBook()
    yield pb
    pb.close()


def test_phonebook_add(pb):
    pb.add("Joe", "123423452345")
    assert "123423452345" == pb.lookup("Joe")


def test_phonebook_contains_all_names(pb):
    pb.add("Joe", "123423452345")
    assert "Joe" in pb.names()


def test_phonebook_raise_error_on_invalid_key(pb):
    pb.add("Joe", "123423452345")
    with pytest.raises(KeyError):
        pb.lookup("Bob")
