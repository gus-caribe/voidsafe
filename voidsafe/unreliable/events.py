"""
        \
This module contains the constants that represent unreliable events that `might`
or `might not` happens and that were being relied on for further operations, resulting
on `Potentially Unsafe Instances []` and `Potentially Unsafe Resources []`.
"""

from typing import Final

class _Event:
    __slots__ = ()

    happens: Final[bool] = True
    doesNotHappen: Final[bool] = False


TAKEN_FOR_GRANTED: _Event = _Event()
"""
        \
This constant can invoke `happens` and `doesNotHappen` in order to emulate a 
condition where `Potentially Unsafe Instances [2.1]` and `Potentially Unsafe 
Resources [2.2]` are assigned with a value that's expected to be used on further
operations.
        \
You can take it as an analogy to certain `unpredictable`, `unreliable` resources 
that `usually` provide you with what you expected at runtime, but `might` not work 
as expected sometimes. Your application should be able to deal with these situations.

...

----
### 1. Case:

        \
Say you're getting a JSON as a response from an HTTP request. You were counting          \
on the value of one of its fields to assign it to a variable of which your application   \
depends on, and you expected it to be a `string`. \n
        \
Your application is running smoothly for 2 weeks straight when, suddenly, your REST API  \
provider returns a JSON response body containing the same field, but with the value      \
`null` (which translates to `None` in Python). Your application crashes. Your services   \
are shut down and your customers get furious, all of that because you've `taken for      \
granted` that an external resource would give you exactly what you needed, 100% of the   \
time.

...
### 2. Example:

        \
In the following example, you're providing an application that depends on a third-party  \
service offered by `catfact.ninja`, which serves an API with a GET method that delivers  \
a JSON containing one random fact about cats.
        \
You're supposed to serve a WEB back-end containing one single route supporting GET       \
method: `/upper_fact`. Its purpose is to provide your client with the same response it   \
would have gotten from `catfact.ninja`'s `/fact` route, but with the `'fact'` content    \
formatted in UPPERCASE.

...

```python
from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/upper_fact")
async def upperCatFact():
    # You were smart enough to initialize 'catFact' as a string,
    # because you knew you would need to call 'upper()' later on.
    catFact: str = ""

    # You've obtained the response from 'catfact.ninja/fact'
    response = requests.get("https://catfact.ninja/fact")

    # You were smart enough to check if the response body contained 
    # the field 'fact', which should hold the value you needed.
    if response.status_code == 200 and 'fact' in response.json():
        responseJson = response.json()

        # Now, suppose that, one day, `catfact.ninja`'s service failed
        # and the `responseJson['fact']` returned 'None'. Remember
        # Python doesn't assert types at runtime.
        catFact = responseJson['fact']
    
    # Here, when your app tried to call the 'upper()' method on an
    # instance that was holding the value 'None', Python raised an 
    # 'AttributeError' and you application crashed.
    return {'fact': catFact.upper()}
```
...
        \
In the example given above, the `implicit` condition that could be represented by
`TAKEN_FOR_GRANTED` would be `isinstance(response.json()["fact"], str)`. 

...
"""
