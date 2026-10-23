import pytest
import book
import library
import user


@pytest.mark.wip
def test_borrow_book():
    book1 = book.Book('Orgullo y Prejuicio', 'Tenoch', 2026, 'ISBN001')

    assert book1.title == 'Orgullo y Prejuicio'

    book1.borrow()
    assert book1.borrowed == True


@pytest.mark.wi
def test_borrow_two_times_book():
    book1 = book.Book('Orgullo y Prejuicio', 'Tenoch', 2026, 'ISBN001')

    book1.borrow()
    assert book1.borrowed == True

    with pytest.raises(ValueError, match="The book is already borrowed"):
        book1.borrow()


@pytest.mark.wi
def test_return_book():
    book1 = book.Book('Orgullo y Prejuicio', 'Tenoch', 2026, 'ISBN001')

    book1.borrow()
    assert book1.borrowed == True

    book1.return_book()
    assert book1.borrowed == False


@pytest.fixture
def lib_init():
    lib = library.Library()

    book1 = book.Book('Orgullo y Prejuicio', 'Tenoch', 2026, 'ISBN001')
    lib.add_book(book1)

    usuario = user.User('Tenoch', 'ID0001')
    lib.add_user(usuario)

    return lib


@pytest.mark.wi
def test_library_borrow(lib_init):
    lib = lib_init

    lib.borrow_book('ID0001', 'ISBN001')

    assert lib.books[0].borrowed == True


@pytest.mark.poi
def test_library_user_not_found(lib_init):
    lib = lib_init

    with pytest.raises(ValueError, match="User not found"):
        lib.borrow_book('ID0003', 'ISBN001')


@pytest.mark.cap
def test_capsys(lib_init, capsys):
    lib = lib_init

    lib._find_user('ID0001')

    captured = capsys.readouterr()

    assert "User not found" in captured.err


def test_try_except():
    book1 = book.Book('Orgullo y Prejuicio', 'Tenoch', 2026, 'ISBN001')

    book1.borrow()

    try:
        book1.borrow()
    except ValueError as e:
        assert str(e) == "The book is already borrowed"
    else:
        pytest.fail("Se esperaba un ValueError")


@pytest.mark.parametrize("titulo", [
    "1984",
    "Orgullo y Prejuicio",
    "Moby Dick"
])
def test_parametrize(titulo):
    book1 = book.Book(titulo, 'Tenoch', 2026, 'ISBN001')

    assert book1.title == titulo


def test_monkeypatch_setattr(monkeypatch):
    book1 = book.Book('Orgullo y Prejuicio', 'Tenoch', 2026, 'ISBN001')

    monkeypatch.setattr(book1, "borrowed", True)

    assert book1.borrowed == True

    with pytest.raises(ValueError, match="The book is already borrowed"):
        book1.borrow()


def test_monkeypatch_delattr(monkeypatch):
    book1 = book.Book('Orgullo y Prejuicio', 'Tenoch', 2026, 'ISBN001')

    monkeypatch.delattr(book1, "title")

    assert not hasattr(book1, "title")