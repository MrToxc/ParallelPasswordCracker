import hashlib
import multiprocessing
import string

from parser import get_file_characters

THEORETICAL_MAX_PASSWORD_LENGTH = 100
CHAR_SETS = {
    "letters" : set(string.ascii_lowercase),
    "LETTERS" : set(string.ascii_uppercase),
    "numbers" : set(string.digits),
    "special" : set(string.punctuation),
}
DEFAULT_HASH = "9e0133f2a137e8eb48b7f27c25f06a7f4f9a3410b045bfe6823246608d1ee827e31e38bde7cfdfcb8702741b60449a3a"
DEFAULT_MAX_CHARS = 5
DEFAULT_MAX_PROCESSES = 2
CONFIG_FILEPATH = "config.txt"

class PasswordCracker:
    def __init__(self, max_chars = DEFAULT_MAX_CHARS, max_processes = DEFAULT_MAX_PROCESSES, target_hash = DEFAULT_HASH, character_types=None):
        self.check_arguments(max_chars, max_processes, target_hash)
        final_char_set = get_file_characters(CONFIG_FILEPATH)

        if len(final_char_set) == 0 and (character_types is None or len(character_types) == 0):
            character_types = ["letters"]

        self.max_chars = max_chars
        self.max_processes = max_processes
        self.hash_target = target_hash.strip().lower()

        for char_set_type in character_types:
            char_set = CHAR_SETS[char_set_type]
            final_char_set |= char_set
        self.final_char_set = list(final_char_set)

        self.finish_flag = multiprocessing.Value('i', 0)
        self.final_password = multiprocessing.Array('c', THEORETICAL_MAX_PASSWORD_LENGTH)



    def get_result(self):
        return self.final_password.value.decode('utf-8')

    @staticmethod
    def check_arguments(max_chars: int, max_processes: int, target_hash: str):
        if max_chars <= 0:
            raise ValueError(f"max_chars must be a positive integer (got {max_chars})")
        if max_processes <= 0:
            raise ValueError(f"max_processes must be a positive integer (got {max_processes})")
        if len(target_hash) != len(DEFAULT_HASH):
            raise ValueError("target_hash is invalid")

    def get_password_from_index_list(self, index_list):
        final_password = ''
        for index in index_list:
            if not isinstance(index, int):
                raise TypeError('Index must be an integer')
            if index < 0 or index >= len(self.final_char_set):
                raise IndexError(f"Index out of range, index = {index}, len(final_char_set) = {len(self.final_char_set)}")
            final_password += self.final_char_set[index]
        return final_password

    def increment_index_list(self, index_list):
        base = len(self.final_char_set)
        pos = len(index_list) - 1
        while pos >= 0:
            if not isinstance(index_list[pos], int):
                raise TypeError('Index must be an integer')

            if index_list[pos] + 1 < base:
                index_list[pos] += 1
                return index_list

            index_list[pos] = 0
            pos -= 1
        return False




    def worker_crack_password(self, task_queue):
        #v manageru je queue.put((symbols_count, start, end))

        while True:
            tasks = task_queue.get()
            if self.finish_flag.value == 1 or tasks is None:
                break
            password_index_list = [0] * tasks[0]

            #print(password_index_list)
            counter = 0
            password_index_list[0] = tasks[1]
            while (password_index_list is not False and password_index_list[0] != tasks[2]) and self.finish_flag.value == 0:
                counter += 1
                if counter >= 300000:
                    counter = 0
                    #print(self.get_password_from_index_list(password_index_list) + "////start:" +  str(self.final_char_set[tasks[1]]) + "/end:" + str(self.final_char_set[tasks[2]-1]))
                current_password = self.get_password_from_index_list(password_index_list)
                if hashlib.sha384(current_password.encode('utf-8')).hexdigest() == self.hash_target:
                    # Ulozeni do sdilene pameti (musime prevest na bytes)
                    self.final_password.value = current_password.encode('utf-8')
                    self.finish_flag.value = 1 #True
                    return self.get_password_from_index_list(password_index_list)
                password_index_list = self.increment_index_list(password_index_list)
        #password not found
        return None




    def process_manager(self):

        self.finish_flag.value = 0
        task_queue = multiprocessing.Queue()

        base, rem = divmod(len(self.final_char_set), self.max_processes)
        self.finish_flag.value = 0
        processes = []

        for _ in range(self.max_processes):
            p = multiprocessing.Process(target = self.worker_crack_password, args = (task_queue,))
            p.start()
            processes.append(p)

        for symbols_count in range(1, self.max_chars + 1):
            if self.finish_flag.value == 1:
                break


            for process in range(0, self.max_processes):
                #genialni matika od chata, tohle bych fakt nevymyslel TBH
                current_process_start = process * base + min(process, rem)
                size = base + (1 if process < rem else 0)
                #konec genialni matickyy
                current_process_end = current_process_start + size
                task_queue.put((symbols_count , current_process_start, current_process_end))


        for _ in range(self.max_processes):
            task_queue.put(None)  # Pekne jedovata pill

        for process in processes:
            process.join()

        if self.finish_flag.value == 1:
            return self.final_password.value.decode('utf-8')
        #print("Password not found")
        return None


