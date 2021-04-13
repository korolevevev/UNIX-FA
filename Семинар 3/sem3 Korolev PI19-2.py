import multiprocessing as mp
import yaml
import random
from typing import List

m1file = "./data/matrix1.yml"
m2file = "./data/matrix2.yml"
resFile = "./data/result.yml"

def wToFile(matrix: List[List[int]], file_name: str) -> None:
    with open(file_name, "w") as file:
        yaml.safe_dump(matrix, file)


def mGen(n: int, m: int) -> List[List[int]]:
    matrix = []
    for i in range(n):
        matrix.append([])
        for j in range(m):
            matrix[i].append(random.randint(1, 100))
    return matrix


def mMultiply(i: int, j: int, A: list, B: list, que: mp.Queue) -> None:
    buffer_list = []
    for k in range(len(A[0]) or len(B)):
        buffer_list.append(A[i][k] * B[k][j])
    resDict = {}
    resDict["result"] = sum(buffer_list)
    resDict["i"] = i
    resDict["j"] = j
    que.put(resDict)


def newMGen():
    n = int(input("Количество строк = "))
    m = int(input("Количество столбцов = "))
    matrix1 = mGen(n, m)
    matrix2 = mGen(m, n)
    wToFile(matrix1, m1file)
    wToFile(matrix2, m2file)
    return matrix1, matrix2

def oldMGen():
    return mRead(m1file), mRead(m2file)

def mPrint(matrix: List[List[int]]) -> None:
    r = "\n" + "\n".join(["\t".join([str(cell) for cell in row]) for row in matrix])
    print(r)


def mRead(file_name: str) -> List[List[int]]:
    with open(file_name, "r") as file:
        return yaml.safe_load(file)    


if __name__ == "__main__":

    manager = mp.Manager()
    commands_dict = {
        "1": oldMGen,
        "2": newMGen,
    }

    matrix1 = None
    matrix2 = None

    while True:
        command_input = input(
            "Ввести матрицу вручную или загрузить из файла?"
        )
        if command_input in commands_dict:
            matrix1, matrix2 = commands_dict[command_input]()
            break
        else:
            print("Команда не найдена")

    matrix_result = [
        [0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix2[0]))
    ]
    mPrint(matrix1)
    mPrint(matrix2)
    processes_list = []
    que = manager.Queue()

    for i in range(len(matrix_result)):
        for j in range(len(matrix_result[i])):
            p = mp.Process(
                target=mMultiply,
                args=(
                    i,
                    j,
                    matrix1,
                    matrix2,
                    que,
                ),
            )
            processes_list.append(p)

    for p in processes_list:
        p.start()
    for p in processes_list:
        p.join()

    for i in range(len(matrix_result)):
        for j in range(len(matrix_result[i])):
            r = que.get()
            matrix_result[r["i"]][r["j"]] = r["result"]

    mPrint(matrix_result)
    wToFile(matrix_result, resFile)