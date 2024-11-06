from typing import Callable, Iterable, List
import sqlite3
import pickle  # FIXME: add security code during pickleing, e.g. hash


def rfbp(
    loader: Iterable,
    transformer: Callable,
    *,
    failfast: bool = True,
    quite: bool = False,
    log: Callable[str, None] = print,
    db_name: str = "rfbp.db",
) -> List:
    """Start a batch loop which can resume from breakpoint.

    If an exception occurs during the batch process, simply rerun the function without altering any code.

    This function proceeds as follows:
    1. Iterates over items retrieved from the `loader` iterable.
    2. Checks if the `item` exists.
    3. Applies the `transformer` function to the `item`.
    4. Stores the transformed `item` in an sqlite3 database.
    5. Returns a list containing all items.

    When `transformer()` raises an exception, the behavior of `rfbp()` depends on the `failfast` parameter:
    - `failfast=True`: Immediately raises the exception to the outer scope.
    - `failfast=False`: Collects the exception into a group to be raised after the batch completes, and inserts `None` into the return list for the failed item.

    Notes
    -----
        Each unique combination of `loader()` and `transformer()` should correspond to a single database.
        Once the data is no longer needed, rename or delete the database file.

    Parameters
    ----------
    loader : Iterable
        An iterable object that yields input items.
    transformer : Callable
        A function that accepts an item from `loader` and returns a transformed item.
        It is expected that `transformer` may raise exceptions during execution.
    failfast : bool, default=True
        Whether to fail fast when `transformer` raises an exception.
    quiet : bool, default=False
        If `True`, `rfbp()` will not log any messages.
    log : Callable[[str], None], default=print
        The logging function used by `rfbp()`.
    db_name : str, default="rfbp.db"
        The file name of the sqlite3 database.

    Returns
    -------
    List
        A list of transformed items or `None` values if `transformer()` raised an exception.

    Raises
    ------
    Exception
        The exception raised by `transformer()` when `failfast=True`.
    ExceptionGroup
        A group of exceptions raised during the batch loop when `failfast=False`.

    Examples
    --------
    >>> loader = range(5)
    >>> transformer = lambda x: x * 2
    >>> rfbp(loader, transformer, quiet=True)
    [0, 2, 4, 6, 8]
    """
    if quite:
        log = lambda x: None

    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS objects (
            idx INTEGER PRIMARY KEY,
            pickled BLOB
        )
        """
    )
    con.commit()
    result = []
    excs = []
    for idx, item in enumerate(loader):
        log(f"{idx=}")

        if row := cur.execute(
            "SELECT pickled FROM objects WHERE idx = ?", (idx,)
        ).fetchone():
            log("exists, skipped")
            pickled = row[0]
            item = pickle.loads(pickled)

        else:
            log("not exists, transforming...")
            try:
                item = transformer(item)
            except Exception as e:
                if failfast:
                    con.commit()
                    raise e
                else:
                    log("an exception occurs, skipped")
                    excs.append(e)
                    result.append(None)
                    continue

            cur.execute(
                "INSERT INTO objects(idx, pickled) VALUES (?, ?)",
                (idx, pickle.dumps(item)),
            )
            con.commit()
        result.append(item)
    if not failfast:
        con.commit()
        if excs:
            raise ExceptionGroup("There are some exceptions during rfbp() loop.", excs)
    return result
