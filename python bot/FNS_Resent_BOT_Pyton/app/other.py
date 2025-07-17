from aiogram.types import ContentType, BufferedInputFile
import requests
separator1 = '\x1F'
separator2 = '\x1E'
separator3 = '\x1D'


def already_inited(i, chat_id):
    file = open('../indexing.env', 'r')
    matrix = uncapsule_matrix(file)
    file.close()
    if chat_id in matrix[i]:
        return True
    else:
        return False


def incapsulate_changed_matrix(file, matrix):
    matrix_text = ''
    for row in matrix:
        if (row != matrix[0]):
            matrix_text += f"\n"
        for element in row:
            if (element != row[0]):
                matrix_text += f";{element}"
            else:
                matrix_text += f"{element}"
    file.write(f"{matrix_text}")


def uncapsule_matrix(file):
    content = file.read()
    rows = content.strip().split('\n')
    matr = [row.split(';') for row in rows]
    return matr


def creator_exists(operator_id):
    file = open('../indexing.env', 'r')
    matrix = uncapsule_matrix(file)
    file.close()
    matr0 = [row[0] for row in matrix if row]
    connected = [matr0.index(elem) for elem in matr0 if str(operator_id) == elem]
    if connected:
        return connected[0]
    else:
        return -1
