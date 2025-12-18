import pytest

from src.accounts_registry import AccountsRegistry


@pytest.fixture
def registry():
    return AccountsRegistry()


def test_add_and_get_by_id(registry):
    acc_id = registry.add_personal_account("John", "Doe", "98309201942")
    acc = registry.get_by_id(acc_id)
    assert acc is not None
    assert acc.first_name == "John"
    assert acc.last_name == "Doe"
    assert acc.pesel == "98309201942"


def test_get_by_pesel_and_promo_bonus(registry):
    # 6103.. -> rok 1961, więc kwalifikuje się do bonusu z poprawnym kodem
    acc_id = registry.add_personal_account("Jane", "Smith", "61030512345", promo_code="PROMO_ABC")
    assert isinstance(acc_id, int)
    acc = registry.get_by_pesel("61030512345")
    assert acc is not None
    assert acc.balance == 50


@pytest.mark.parametrize("pesel", ["", "92019", "983092034631974", None])
def test_add_rejects_invalid_pesel(registry, pesel):
    with pytest.raises(ValueError, match="PESEL"):
        registry.add_personal_account("A", "B", pesel)  # type: ignore[arg-type]


def test_duplicate_pesel_is_rejected(registry):
    registry.add_personal_account("A", "B", "98309201942")
    with pytest.raises(ValueError):
        registry.add_personal_account("X", "Y", "98309201942")


def test_remove_frees_pesel_and_returns_bool(registry):
    acc_id = registry.add_personal_account("A", "B", "98309201942")
    assert registry.remove(acc_id) is True
    assert registry.get_by_id(acc_id) is None
    # po usunięciu można dodać ten sam PESEL ponownie
    new_id = registry.add_personal_account("A", "B", "98309201942")
    assert new_id != acc_id


def test_list_all_counts_and_content(registry):
    assert len(registry.list_all()) == 0
    registry.add_personal_account("A", "B", "61030512345")
    registry.add_personal_account("C", "D", "55081267890")
    all_accounts = registry.list_all()
    assert len(all_accounts) == 2
    assert {"61030512345", "55081267890"} == {a.pesel for a in all_accounts}
