from multiprocessing import Process, Pipe
import time as t
import os
import argparse
import numpy as np
import pandas as pd
import optimize_J



def f(i):
    print('id :',i,'\n','process: ',os.getpid())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=int, default=3,
        help='Number of islands, i.e. number of Genetic Algorithm excuted in parallel')
    parser.add_argument('-m', type=int, default=5,
                        help='Interval between each migration')
    parser.add_argument('-e', type=int, default=5,
                        help='Pourcentage of emigrants in each migration')
    args = parser.parse_args()

    N_islands = args.i
    N_migrations = args.m
    N_emigrants = args.e


    # Creates an array which contain a Pipe for every connexion between islands    
    Pipes = pd.DataFrame(columns=[str(i) for i in range(N_islands)])
    for i in range(N_islands):
        Pipes.loc[i] = [ Pipe() for _ in range(N_islands)]
        # Set the diagonal to 0: Migration is not possible from an island to itself
        np.fill_diagonal(Pipes.values,0)

    pool = []
    for i in range(N_islands):
        p = Process(target=optimize_J.main, args=(Pipes, i, N_islands,))
        p.start()
        pool.append(p)
    
    #for i,p in enumerate(pool):
        #p.join()




if __name__ == '__main__':
    main()

    # def g(conn,id):
    #     print('Bonjour depuis ',id,conn)
    #     #a = pd.DataFrame([[0,0,0,0,0,0],[1,1,1,1,1,1]])
    #     conn.send('Hello from %s'%str(id))
    #     rep = conn.recv()
    #     print(rep,conn)

    # a , b = Pipe()
    # pipes = [a,b]
    # for i in range(2):
    #     p = Process(target=g, args=(pipes[i],i))
    #     p.start()
    