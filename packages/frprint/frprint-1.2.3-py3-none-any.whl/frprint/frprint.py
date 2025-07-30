def is_variable(variable) :
    try :
        eval(variable)
        return 1
    except NameError :
        return 0


def frprint(String,Int = 1,Boolean = True) :
    try :
        verification = int(Int) / 1
    except Exception as e:
        raise ValueError("Please put a number in the Int entry")
    if Boolean != True and Boolean != False :
        raise Exception("Please add a True or False value to the Boolean entry")
    try :
        isitvariable = is_variable(str(String))
    except TypeError :
        isitvariable = 0
    if isitvariable == 1 :
        if isinstance(String, str) == False :
            if Boolean == True :
                for i in range(1,int(Int) + 1) :
                    print(String + i)
                return
            if Boolean == False :
                for i in range(1, int(Int) + 1) :
                    print(String + i, end=" ")
                return
        else :
            if Boolean == True :
                for i in range(int(Int)) :
                    print(String)
                return
            if Boolean == False :
                for i in range(int(Int)) :
                    print(String, end=" ")
                return
    elif isitvariable == 0 :
        if Boolean == True :
            for i in range(int(Int)) :
                print(String)
            return
        if Boolean == False :
            for i in range(int(Int)) :
                print(String, end=" ")
            return