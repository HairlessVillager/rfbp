# RFBP: Resume your batch From BreakPoing!

```py
from rfbp import rfbp

# This generate data.😉
def loader():
    for x in range(4):
        yield x

# This process data.😉
def transformer(x):
    if random() < 0.5:
        raise ValueError("mock exception")
    return x * 2

if __name__ == "__main__":
    # And this help you recover your batch script from a disastrous exception!🥳
    result = rfbp(loader(), transformer, failfast=False)
    print(result)
```

```
$ python example.py                                                                                                                            ─╯
idx=0
not exists, transforming...
an exception occurs, skipped
idx=1
not exists, transforming...
an exception occurs, skipped
idx=2
not exists, transforming...
an exception occurs, skipped
idx=3
not exists, transforming...
  + Exception Group Traceback (most recent call last):
  |   File "/workspace/example.py", line 18, in <module>
  |     result = rfbp(loader(), transformer, failfast=False)
  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  |   File "/workspace/rfbp.py", line 119, in rfbp
  |     raise ExceptionGroup("There are some exceptions during rfbp() loop.", excs)
  | ExceptionGroup: There are some exceptions during rfbp() loop. (3 sub-exceptions)
  +-+---------------- 1 ----------------
    | Traceback (most recent call last):
    |   File "/workspace/rfbp.py", line 99, in rfbp
    |     item = transformer(item)
    |            ^^^^^^^^^^^^^^^^^
    |   File "/workspace/example.py", line 13, in transformer
    |     raise ValueError("mock exception")
    | ValueError: mock exception
    +---------------- 2 ----------------
    | Traceback (most recent call last):
    |   File "/workspace/rfbp.py", line 99, in rfbp
    |     item = transformer(item)
    |            ^^^^^^^^^^^^^^^^^
    |   File "/workspace/example.py", line 13, in transformer
    |     raise ValueError("mock exception")
    | ValueError: mock exception
    +---------------- 3 ----------------
    | Traceback (most recent call last):
    |   File "/workspace/rfbp.py", line 99, in rfbp
    |     item = transformer(item)
    |            ^^^^^^^^^^^^^^^^^
    |   File "/workspace/example.py", line 13, in transformer
    |     raise ValueError("mock exception")
    | ValueError: mock exception
    +------------------------------------

$ python example.py                                                                                                                            ─╯
idx=0
not exists, transforming...
an exception occurs, skipped
idx=1
not exists, transforming...
idx=2
not exists, transforming...
idx=3
exists, skipped
  + Exception Group Traceback (most recent call last):
  |   File "/workspace/example.py", line 18, in <module>
  |     result = rfbp(loader(), transformer, failfast=False)
  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  |   File "/workspace/rfbp.py", line 119, in rfbp
  |     raise ExceptionGroup("There are some exceptions during rfbp() loop.", excs)
  | ExceptionGroup: There are some exceptions during rfbp() loop. (1 sub-exception)
  +-+---------------- 1 ----------------
    | Traceback (most recent call last):
    |   File "/workspace/rfbp.py", line 99, in rfbp
    |     item = transformer(item)
    |            ^^^^^^^^^^^^^^^^^
    |   File "/workspace/example.py", line 13, in transformer
    |     raise ValueError("mock exception")
    | ValueError: mock exception
    +------------------------------------

$ python example.py                                                                                                                            ─╯
idx=0
not exists, transforming...
idx=1
exists, skipped
idx=2
exists, skipped
idx=3
exists, skipped
[0, 2, 4, 6]
```

More info see the docstring of `rfbp()`.
