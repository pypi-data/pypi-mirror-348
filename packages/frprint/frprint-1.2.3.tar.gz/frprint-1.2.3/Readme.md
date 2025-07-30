# Introducing "frprint"!

If we want to repeat using "print()" before,<br>
We should use "for()" or spam "print()".<br>
But now! we can use "frprint()"!
## form
```
frprint(string type or variable,repeat times(optional,int type),Do not line break(True or False,Optional,Default = True))
```
## how to use

It is very easy to use.<br>
Just type frprint(), and put two variables in the "frprint()".<br>
There's a 2 Type of frprint must need.<br>
frprint() needs "text" and "int".<br>
for an example,<br>
&nbsp; frprint("Hello python!",4)<br>
&nbsp; It is same with...<br>
```
for i in range(4) :
    print("Hello python!")
```
Is same with,<br>
```
frprint("Hello python!")
```
Yup. It goes like frprint(text,int,boolean(optional,Default value is True) )
If you write frprint like this...
```
frprint("Hello python!",4,False)
```
It goes like...
```
for i in range(4) :
    print("Hello word!", end=" ")
```

And this is all to use frprint()!<br>
Ps.<br>
you can also print variables.()


# update log

## 1.2.3
If variable in frprint(), it will be work like this<br>
example :
```
x = 10
frprint(x,5)
```
is same with...
```
for i in range(1,5 + 1) :
    print(x += i)
```