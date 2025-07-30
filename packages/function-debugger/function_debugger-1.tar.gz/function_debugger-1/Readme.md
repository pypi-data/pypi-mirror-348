# Introducing function debugger!

## form
```
logger(text(optional))
```
If you use this function in your function,<br>
It will print({your function name} + text(optional))<br>
And It will return {your function name}!<br>
Example :
```
def test() :
    logger()

test()
>>>>>>>>>>>>>
print -> test
return -> test
```
And the other example is...
```
def test2() :
    logger("is used logger function")

test2()
>>>>>>>>>>>>>
print -> test2 is used logger function
return -> test2
```