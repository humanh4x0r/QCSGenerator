import numpy as np
import string
import time

class QCSGenerator:
    def __init__(self, seed=None):
        if seed is None:
            seed = int(time.time() * 1000) % 2**32
        self.state = np.zeros(len(string.digits) + len(string.ascii_letters), dtype=np.complex128)
        self.state[seed % len(self.state)] = 1

    def generate_number(self):
        h_matrix = np.array([
            [1 / np.sqrt(2), 1 / np.sqrt(2)],
            [1 / np.sqrt(2), -1 / np.sqrt(2)]
        ], dtype=np.complex128)
        for i in range(0, len(self.state), 2):
            if i == len(self.state) // 2:
                continue
            self.state[i:i+2] = np.dot(h_matrix, self.state[i:i+2])

        measurement_probs = np.abs(self.state) ** 2
        rand_value = np.argmax(np.random.multinomial(1, measurement_probs, 1))

        for i in range(0, len(self.state), 2):
            if i == len(self.state) // 2:
                continue
            self.state[i:i+2] = np.dot(np.conjugate(h_matrix), self.state[i:i+2])

        return rand_value

    def write_string_to_file(self, string):
        with open('strings.txt', 'a') as file:
            file.write(string + '\n')

    def generate_string(self, length=30):
        if length < 20:
            length = 20

        all_characters = string.digits + string.ascii_letters
        random_characters = np.random.randint(0, high=len(all_characters), size=length)

        random_strings = []
        for index in random_characters:
            while index >= len(all_characters):
                index -= len(all_characters)

            random_character = all_characters[index]
            random_strings.append(random_character)

        return ''.join(random_strings)

    def generate_strings(self, count=5000):
        string_count = 0
        while string_count < count:
            generated_string = self.generate_string()
            self.write_string_to_file(generated_string)
            string_count += 1

qcs_generator = QCSGenerator()
qcs_generator.generate_strings()
