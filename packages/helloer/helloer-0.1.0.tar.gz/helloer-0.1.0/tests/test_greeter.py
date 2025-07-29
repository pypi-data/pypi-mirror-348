from helloer import say_hello

def test_say_hello(capsys):
    say_hello("Manav")
    captured = capsys.readouterr()
    assert captured.out == "Hello, Manav\n"