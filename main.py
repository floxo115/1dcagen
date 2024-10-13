import numpy as np
import argparse
from PIL import Image


def apply_rule(inp: np.ndarray, rule:int)->np.ndarray:
    new_row = np.zeros_like(inp)

    for i in range(len(inp)):
        pos_2 = inp[(i-1)%len(inp)]
        pos_1 = inp[i%len(inp)]
        pos_0 = inp[(i+1)%len(inp)]

        num = pos_2*2**2 + pos_1*2**1 + pos_0*2**0
        alive = (2**num & rule) != 0
        new_row[i] = int(alive)

    return new_row


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--length_row", "-lr", help="length of the rows", type=int, required=True)
    parser.add_argument("--length_cols", "-lc", help="length of the result", type=int, required=True)
    parser.add_argument("--rule_number", "-r", help="rule to use for transformations", type=int, required=True)
    parser.add_argument("--save_image", type=str, help="save image")
    parser.add_argument("--save_array", type=str, help="save array")
    args = parser.parse_args()

    current_line = np.random.randint( 0,2, size=(args.length_row,))
    current_line = np.zeros_like(current_line)
    for i in range(10):
        current_line[np.random.randint(0, args.length_row)] = 1

    result = np.zeros((args.length_cols, args.length_row),dtype=int)
    result[0, :] = current_line

    for i in range(1, result.shape[0]):
        result[i, :] = apply_rule(current_line, args.rule_number)
        current_line = result[i,:]

    if args.save_image:
        result8 = np.kron(result, np.ones((1,1), dtype=float))
        result8 = (((result8 - result8.min()) / (result8.max() - result8.min())) * 255.9).astype(np.uint8)
        Image.fromarray(result8).save("./"+args.save_image)

    if args.save_array:
        result = np.vstack((np.arange(0, result.shape[1]).reshape(1,-1), result))
        np.savetxt(args.save_array, result, delimiter=",", fmt="%i")



