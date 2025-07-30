def frprint(String,Int = 1,Boolean = True) :
    try :
        verification = int(Int) / 1
    except Exception as e:
        raise ValueError("Please put a number in the Int entry")
    if Boolean != True and Boolean != False :
        raise Exception("Please add a True or False value to the Boolean entry")


    if Boolean == True :
        for i in range(int(Int)) :
            print(String, end=" ")
        return
    if Boolean == False :
        for i in range(int(Int)) :
            print(String)
        return