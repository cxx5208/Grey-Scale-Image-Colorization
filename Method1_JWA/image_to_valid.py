import os
image_folder = 'F:/mtech/partial_test_set/'
def f():
    names = [f for f in os.listdir(image_folder)]


    # with open('names.txt', 'w') as file:
    #     file.write('\n'.join(names))

    with open('valid_names.txt', 'w') as file:
        file.write('\n'.join(names))

    
if __name__ == '__main__':
    f()
