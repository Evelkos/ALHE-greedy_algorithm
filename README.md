# ALHE-greedy_algorithm
Implementation of greedy algorithm


### Instrukcja tworzenia środowiska

1. Zainstaluj `pyenv` - https://github.com/pyenv/pyenv-installer ( `$ curl https://pyenv.run | bash` )
2. Zainstaluj `poetry` - https://poetry.eustace.io/docs/#introduction
3. Żeby zmusić `poetry` do stworzenia `venv`'a w repo użyj: `poetry config settings.virtualenvs.in-project true`.
4. Przejdź do katalogu `<repo>/src`
5. Zainstaluj Python'a 3.7.2:
    ```shell
    pyenv install 3.7.2
    pyenv local 3.7.2
    ```
6. Uruchom polecenie `poetry install`.


### Uruchamianie środowiska
`source .venv/bin/activate`

### Testowanie
1. Przejdź do katalogu `<repo>/src`
2. Wpisz: `make test`
3. Jeśli testy przeszły, to wszystko zrobiono poprawnie
