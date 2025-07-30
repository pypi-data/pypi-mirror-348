# strath

## FRANÇAIS

Cette bibliothèque aide à assurer qu'un chemin de fichier soit de type `str` ou
`pathlib.Path`.

En Python, il est possible de représenter des chemins de fichier au moyen de
chaînes de caractères (`str`) ou d'instances de `pathlib.Path`. Ces types
étant employés de façons fort différentes, un développeur peut avoir besoin de
vérifier le type des objets et d'effectuer des conversions.

La bibliothèque `strath` permet de faire ces deux tâches en un seul appel de
fonction.

### Contenu

#### `ensure_path_is_pathlib`

Si le chemin est une chaîne de caractères, cette fonction le convertit en une
instance de `pathlib.Path` et renvoie cette dernière. Si le chemin est une
instance de `pathlib.Path`, la fonction renvoie le chemin.

#### `ensure_path_is_str`

Si le chemin est une instance de `pathlib.Path`, cette fonction le convertit en
une chaîne de caractères et renvoie cette dernière. Si le chemin est une chaîne
de caractères, la fonction renvoie le chemin.

#### Paramètres et exception `TypeError`

Les fonctions ci-dessus ont les mêmes paramètres.

`some_path` (`str` ou `pathlib.Path`): le chemin d'un fichier ou d'un dossier.

`is_none_allowed` (`bool`): détermine si `some_path` peut être `None`.

Si l'argument `some_path` est `None` et l'argument `is_none_allowed` est vrai
(`True`), les fonctions renvoient `None`. Par contre, si `is_none_allowed` est
faux (`False`), une exception `TypeError` est levée.

Si l'argument `some_path` n'est pas `None` ni une instance de `str` ou de
`pathlib.Path`, une exception `TypeError` est levée.

Pour plus d'informations, consultez la documentation des fonctions et les démos
dans le dépôt de code source.

### Démos

`demos/demo_fnc_calls.py` contient des exemples d'appel des fonctions de
`strath`.

```
python demos/demo_fnc_calls.py
```

`demos/demo_pathlib_to_str.py` contient une fonction qui utilise une chaîne de
caractères, mais ne connaît pas le type de son argument.

```
python demos/demo_pathlib_to_str.py .. . .github/workflows demos strath tests
```

`demos/demo_str_to_pathlib.py` contient une fonction qui utilise une instance
de `pathlib.Path`, mais ne connaît pas le type de son argument.

```
python demos/demo_str_to_pathlib.py demos/the_planets.txt
```

### Dépendances

Cette commande installe les dépendances nécessaires au développement.

```
pip install -r requirements-dev.txt
```

Cependant, `strath` fonctionne sans dépendances.

### Tests automatiques

Cette commande exécute les tests automatiques.

```
pytest tests
```

## ENGLISH

This library helps ensuring that a file path is of type `str` or
`pathlib.Path`.

In Python, it is possible to represent file paths with character strings
(`str`) or `pathlib.Path` instances. Since these types are used in very
different ways, a developer might need to verify the objects' type and to
perform conversions.

Library `strath` allows to do both tasks with one function call.

### Content

#### `ensure_path_is_pathlib`

If the path is a string, this function converts it to a `pathlib.Path`
instance, which it returns. If the path is a `pathlib.Path` instance, the
function returns the path.

#### `ensure_path_is_str`

If the path is a `pathlib.Path` instance, this function converts it to a
string, which it returns. If the path is a string, the function returns the
path.

#### Parameters and exception `TypeError`

The above functions have the same parameters.

`some_path` (`str` or `pathlib.Path`): the path to a file or directory.

`is_none_allowed` (`bool`): determines whether `some_path` can be `None`.

If argument `some_path` is `None` and argument `is_none_allowed` is `True`,
the functions return `None`. However, if `is_none_allowed` is `False`, a
`TypeError` is raised.

If argument `some_path` is not `None` nor an instance of `str` or
`pathlib.Path`, a `TypeError` is raised.

For more information, consult the functions' documentation and the demos in the
source code repository.

### Demos

`demos/demo_fnc_calls.py` contains examples of calling `strath`'s functions.

```
python demos/demo_fnc_calls.py
```

`demos/demo_pathlib_to_str.py` contains a function that uses a string,
but does not know its argument's type.

```
python demos/demo_pathlib_to_str.py .. . .github/workflows demos strath tests
```

`demos/demo_str_to_pathlib.py` contains a function that uses a `pathlib.Path`
instance, but does not know its argument's type.

```
python demos/demo_str_to_pathlib.py demos/the_planets.txt
```

### Dependencies

This command installs the dependencies necessary for development.

```
pip install -r requirements-dev.txt
```

However, `strath` works without dependencies.

### Automated tests

This command executes the automated tests.

```
pytest tests
```
