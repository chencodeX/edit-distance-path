#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@Author : zihao.chen
@File : edit_distance.py
@Create Date : 2022/04/07
@Descirption : 
"""
import numpy as np
import Levenshtein

# Below are the costs of different operations.
ins_cost = 1
del_cost = 1
sub_cost = 2


def min_cost_path(cost, operations):
    # operation at the last cell
    path = [operations[cost.shape[0] - 1][cost.shape[1] - 1]]
    # print(operations[cost.shape[0] - 1][cost.shape[1] - 1])
    # cost at the last cell
    min_cost = cost[cost.shape[0] - 1][cost.shape[1] - 1]

    row = cost.shape[0] - 1
    col = cost.shape[1] - 1
    # print(cost)
    while row > 0 or col > 0:

        if cost[row - 1][col - 1] <= cost[row - 1][col] and cost[row - 1][col - 1] <= cost[row][col - 1]:
            # print(1,row - 1,col - 1)
            # print(operations[row - 1][col - 1])
            path.append(operations[row - 1][col - 1])
            row -= 1
            col -= 1

        elif cost[row - 1][col] <= cost[row - 1][col - 1] and cost[row - 1][col] <= cost[row][col - 1]:
            # print(2,row - 1,col)
            # print(operations[row - 1][col])
            path.append(operations[row - 1][col])
            row -= 1

        else:
            # print(3,row,col - 1)
            # print([row][col - 1])
            path.append(operations[row][col - 1])
            col -= 1
    # print(path)
    return "".join(path[::-1][1:])


def edit_distance_dp(seq1, seq2):
    # create an empty 2D matrix to store cost
    cost = np.zeros((len(seq1) + 1, len(seq2) + 1))

    # fill the first row
    cost[0] = [i for i in range(len(seq2) + 1)]

    # fill the first column
    cost[:, 0] = [i for i in range(len(seq1) + 1)]

    # to store the operations made
    operations = np.asarray([['-' for j in range(len(seq2) + 1)] \
                             for i in range(len(seq1) + 1)])

    # fill the first row by insertion
    operations[0] = ['I' for i in range(len(seq2) + 1)]

    # fill the first column by insertion operation (D)
    operations[:, 0] = ['D' for i in range(len(seq1) + 1)]

    operations[0, 0] = '-'

    # now, iterate over earch row and column
    for row in range(1, len(seq1) + 1):

        for col in range(1, len(seq2) + 1):

            # if both the characters are same then the cost will be same as
            # the cost of the previous sub-sequence
            if seq1[row - 1] == seq2[col - 1]:
                cost[row][col] = cost[row - 1][col - 1]
            else:

                insertion_cost = cost[row][col - 1] + ins_cost
                deletion_cost = cost[row - 1][col] + del_cost
                substitution_cost = cost[row - 1][col - 1] + sub_cost

                # calculate the minimum cost
                cost[row][col] = min(insertion_cost, deletion_cost, substitution_cost)

                # get the operation
                if cost[row][col] == substitution_cost:
                    operations[row][col] = 'S'

                elif cost[row][col] == insertion_cost:
                    operations[row][col] = 'I'
                else:
                    operations[row][col] = 'D'

    return cost[len(seq1), len(seq2)], min_cost_path(cost, operations)


if __name__ == '__main__':

    seq1 = u"大上海市在沪过节#上海 #春节"
    seq2 = u"上海市在沪过节"

    print(len(seq1), len(seq2))
    # seq1 = """umexpr"""
    # seq2 = """numpy"""
    print(Levenshtein.distance(seq1, seq2))
    score, operations = edit_distance_dp(seq1, seq2)
    print(f"Edit Distance between `{seq1}` & `{seq2}` is: {score}")
    print("\nOperations performed are:\n")
    print('ED:%s\tDEL:%s\tADD:%s\tSUB:%s,' % (
        score, operations.count('D'), operations.count('I'), operations.count('S'),))

    print(len(operations))
    for operation in operations:
        if operation == '-':
            print('No Change.')
        elif operation == 'I':
            print('Insertion')
        elif operation == 'D':
            print('Deletion')
        else:
            print('Substitution')
