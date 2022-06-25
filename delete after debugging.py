import concurrent.futures
numb =0
def foo(bar):
    print('hello {}'.format(bar))
    global numb
    numb+=1
    return numb

with concurrent.futures.ThreadPoolExecutor() as executor:
    
    
    param_list= ["fdsf","dfdfd","isabelle"] 
    futures = [executor.submit(foo, param) for param in param_list]
    print([f.result() for f in futures])
  