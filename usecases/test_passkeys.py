import pytest

from maybe import is_nothing
from testsupport.authenticator import SoftwareAuthenticator
from testsupport.bank import ORIGIN

pytestmark = pytest.mark.integration


def authenticator(attachment: str = "cross-platform") -> SoftwareAuthenticator:
    return SoftwareAuthenticator(ORIGIN, attachment)


def registered(bank, login: str, key: SoftwareAuthenticator):
    return bank.register_with_passkey(login, key)\
        .or_else_throw(AssertionError(f"{login} could not register"))


@pytest.mark.parametrize("attachment", ["platform", "cross-platform"])
def test_client_registers_and_signs_in_with_a_passkey(bank, attachment):
    key = authenticator(attachment)

    alice = registered(bank, "alice", key)
    signed_in = bank.sign_in_with_passkey("alice", key)

    assert alice.login == "alice"
    assert signed_in.or_else_throw(AssertionError()) == alice


def test_a_registered_client_has_a_bank_account(bank):
    alice = registered(bank, "alice", authenticator())

    assert len(list(bank.get_accounts.execute(alice.id))) == 1


def test_a_taken_login_cannot_be_registered_again(bank):
    registered(bank, "alice", authenticator())

    assert is_nothing(bank.start_registration.execute("alice"))


@pytest.mark.parametrize("login", ["", "   ", "x" * 65])
def test_invalid_logins_cannot_be_registered(bank, login):
    assert is_nothing(bank.start_registration.execute(login))


def test_an_unknown_login_cannot_sign_in(bank):
    assert is_nothing(bank.start_authentication.execute("nobody"))


def test_someone_elses_passkey_does_not_sign_in(bank):
    registered(bank, "alice", authenticator())
    mallory_key = authenticator()
    registered(bank, "mallory", mallory_key)

    # Mallory answers Alice's sign-in with her own, valid, passkey.
    ceremony = bank.start_authentication.execute("alice")\
        .or_else_throw(AssertionError())
    [mallory_credential] = mallory_key.credential_ids()
    assertion = mallory_key.get(ceremony.public_key, mallory_credential)

    assert is_nothing(bank.finish_authentication.execute(
        ceremony.ceremony_id, assertion
    ))


def test_a_sign_in_cannot_be_replayed(bank):
    key = authenticator()
    registered(bank, "alice", key)
    ceremony = bank.start_authentication.execute("alice")\
        .or_else_throw(AssertionError())
    assertion = key.get(ceremony.public_key)
    first = bank.finish_authentication.execute(ceremony.ceremony_id, assertion)

    replayed = bank.finish_authentication.execute(
        ceremony.ceremony_id, assertion
    )
    other_ceremony = bank.start_authentication.execute("alice")\
        .or_else_throw(AssertionError())
    replayed_elsewhere = bank.finish_authentication.execute(
        other_ceremony.ceremony_id, assertion
    )

    assert not is_nothing(first)
    assert is_nothing(replayed)
    assert is_nothing(replayed_elsewhere)


def test_a_registration_ceremony_cannot_be_used_to_sign_in(bank):
    key = authenticator()
    registered(bank, "alice", key)
    registration = bank.start_registration.execute("bob")\
        .or_else_throw(AssertionError())
    sign_in = bank.start_authentication.execute("alice")\
        .or_else_throw(AssertionError())

    assertion = key.get(sign_in.public_key)

    assert is_nothing(bank.finish_authentication.execute(
        registration.ceremony_id, assertion
    ))


def test_a_phishing_site_cannot_relay_a_sign_in(bank):
    key = authenticator()
    registered(bank, "alice", key)

    key.origin = "https://bank-login.example"

    assert is_nothing(bank.sign_in_with_passkey("alice", key))


def test_a_phishing_site_cannot_relay_a_registration(bank):
    key = authenticator()
    key.origin = "https://bank-login.example"

    assert is_nothing(bank.register_with_passkey("alice", key))
    assert not is_nothing(bank.start_registration.execute("alice"))


def test_a_cloned_authenticator_is_rejected(bank):
    key = authenticator()
    registered(bank, "alice", key)
    bank.sign_in_with_passkey("alice", key).or_else_throw(AssertionError())

    [credential] = key.credential_ids()
    key.rewind_sign_count(credential)

    assert is_nothing(bank.sign_in_with_passkey("alice", key))
