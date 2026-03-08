from pydantic import ValidationError

from app.schemas.entities import UserUpdate


def test_user_update_accepts_partial_payload() -> None:
    payload = UserUpdate(name='Novo Nome')

    assert payload.model_dump(exclude_unset=True) == {'name': 'Novo Nome'}


def test_user_update_rejects_invalid_empty_name() -> None:
    try:
        UserUpdate(name='')
    except ValidationError:
        return

    raise AssertionError('Expected ValidationError for empty name')
