# Using * allows you to unpack lists. (theoretically, this function could take an unlimited amount of arguments)
# Using ** allows you to unpack named arguments into a dictionary.
def unlimted_arguments(*args, **kwargs):
    for argument in args:
        print(argument)

# call unlimited arguments with  
unlimited_arguments(1,2,3,4)
