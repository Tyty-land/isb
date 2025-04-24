from math import erfc
from scipy.special import gammaincc


def freq_bit_test(data: str) -> float:
    """
    A frequency bitwise test of a pseudorandom sequence of zeros and ones. The first of three NIST tests
    :param data: a sequence of zeros and ones
    :return erfc(abs(x)): the result of calculating the additional error function
    """
    s_n = 0
    for i in data:
        if i == '1':
            s_n += 1
        elif i == '0':
            s_n -= 1
    s_n *= (1 / (len(data) ** 0.5))
    x = s_n / (2 ** 0.5)
    return erfc(abs(x))

def similar_run_test(data: str) -> float:
    """
    A test for identical consecutive bits in a sequence of zeros and ones. The second NIST test
    :param data: a sequence of zeros and ones
    :return erfc(x): the result of calculating the additional error function
    """
    s = 0
    for i in data:
        s += int(i)
    s /= len(data)
    if abs(s - 0.5) < (2 / (len(data)**0.5)):
        v = 0
        for i in range(0, len(data)-1):
            v += 0 if data[i] == data[i+1] else 1
        x = abs(v - 2*len(data)*s*(1 - s)) / (((8*len(data))**0.5) * s * (1 - s))
        return erfc(x)
    else:
        return 0

def long_bit_test(data: str) -> float:
    """
    The test is for the longest sequence in the sequence of zeros and ones block. The third NIST test
    :param data: a sequence of zeros and ones
    :return gammaincc(1.5, x_2/2): incomplete gamma function
    """
    m = 8
    v_all = [0, 0, 0, 0]
    p_all = [0.2148, 0.3672, 0.2305, 0.1875]
    for i in range(0, len(data), m):
        max_sequence_bit = 0
        for j in range(i, i+m):
            tmp_max = 0
            while data[j] == '1' and j < i+m:
                tmp_max += 1
                if j < i + m - 1:
                    j = j+1
                else:
                    break
            if max_sequence_bit <= tmp_max:
                max_sequence_bit = tmp_max
        v_all[0] = v_all[0] + 1 if max_sequence_bit <= 1 else v_all[0]
        v_all[1] = v_all[1] + 1 if max_sequence_bit == 2 else v_all[1]
        v_all[2] = v_all[2] + 1 if max_sequence_bit == 3 else v_all[2]
        v_all[3] = v_all[3] + 1 if max_sequence_bit >= 4 else v_all[3]
    x_2 = 0
    for i in range(0, 4):
        x_2 += ((v_all[i] - 16*p_all[i])**2) / 16*p_all[i]

    return gammaincc(1.5, x_2/2)


def main() -> None:
    """
    The main function that simply writes the results of the test functions to a file
    :return None:
    """
    try:
        with open("c_rand.txt", "r", encoding='utf-8') as file:
            c_rand_str = file.read()
        with open("j_rand.txt", "r", encoding='utf-8') as file:
            j_rand_str = file.read()

        with open("result.txt", "w", encoding='utf-8') as r_file:
            r_file.write("Результаты 3-х тестов NIST для двух ГПСЧ:\n\n")
            r_file.write("ГПСЧ в C++:\n")
            r_file.write(f"Частотный побитовый тест: {freq_bit_test(c_rand_str)}\n")
            r_file.write(f"Тест на одинаковые подряд идущие биты: {similar_run_test(c_rand_str)}\n")
            r_file.write(f"Тест на самую длинную последовательность единиц в блоке: {long_bit_test(c_rand_str)}\n\n")
            r_file.write("ГПСЧ в Java:\n")
            r_file.write(f"Частотный побитовый тест: {freq_bit_test(j_rand_str)}\n")
            r_file.write(f"Тест на одинаковые подряд идущие биты: {similar_run_test(j_rand_str)}\n")
            r_file.write(f"Тест на самую длинную последовательность единиц в блоке: {long_bit_test(j_rand_str)}\n\n")
    except FileNotFoundError:
        print("Что-то не так с открытием файлов!")


if __name__ == '__main__':
    main()
