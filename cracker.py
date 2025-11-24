import hashlib
import multiprocessing
import string
import time


lower_case_alphabet = list(string.ascii_lowercase)
upper_case_alphabet = list(string.ascii_uppercase)
numbers = list(string.digits)
special_characters = list(string.punctuation)


class PasswordCracker:
    def __init__(self, contains_lowercase=True, contains_uppercase=False, contains_numbers=False, contains_special_chars=False, target_hash = ""):
        final_char_set = []
        if contains_numbers or contains_special_chars or contains_lowercase or contains_uppercase:
            if contains_lowercase:
                final_char_set += lower_case_alphabet
            if contains_uppercase:
                final_char_set += upper_case_alphabet
            if contains_numbers:
                final_char_set += numbers
            if contains_special_chars:
                final_char_set += special_characters
            if len(final_char_set) > 0:
                self.final_char_set = final_char_set
            if target_hash != "":
                self.hash_target = target_hash.strip().lower()
            self.finish_flag = multiprocessing.Value('i', 0)
            self.final_password = multiprocessing.Array('c', 100)
        else:
            raise TypeError("contains_numbers or contains_special_chars or contains_lowercase or contains_uppercase must be True")


    def get_password_from_index_list(self, index_list):
        final_password = ''
        for index in index_list:
            if not isinstance(index, int):
                raise TypeError('Index must be an integer')
            if index < 0 or index >= len(self.final_char_set):
                print(index)
                print(index_list)
                raise IndexError('Index out of range')
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

            print(password_index_list)
            counter = 0
            password_index_list[0] = tasks[1]
            while (password_index_list is not False and password_index_list[0] != tasks[2]) and self.finish_flag.value == 0:
                counter += 1
                if counter >= 300000:
                    counter = 0
                    print(self.get_password_from_index_list(password_index_list) + "////start:" +  str(self.final_char_set[tasks[1]]) + "/end:" + str(self.final_char_set[tasks[2]-1]))
                current_password = self.get_password_from_index_list(password_index_list)
                if hashlib.sha384(current_password.encode('utf-8')).hexdigest() == self.hash_target:
                    # Ulozeni do sdilene pameti (musime prevest na bytes)
                    self.final_password.value = current_password.encode('utf-8')
                    self.finish_flag.value = 1 #True
                    return self.get_password_from_index_list(password_index_list)
                password_index_list = self.increment_index_list(password_index_list)
        #password not found
        return None




    def process_manager(self, max_chars, max_processes, task_queue):


        base, rem = divmod(len(self.final_char_set), max_processes)
        self.finish_flag.value = 0
        processes = []

        for _ in range(max_processes):
            p = multiprocessing.Process(target=self.worker_crack_password, args=(task_queue,))
            p.start()
            processes.append(p)

        for symbols_count in range(1, max_chars + 1):
            if self.finish_flag.value == 1:
                break


            for process in range(0, max_processes):
                #genialni matika od chata, tohle bych fakt nevymyslel TBH
                current_process_start = process * base + min(process, rem)
                size = base + (1 if process < rem else 0)
                #konec genialni matickyy
                current_process_end = current_process_start + size
                task_queue.put((symbols_count , current_process_start, current_process_end))


        for _ in range(max_processes):
            task_queue.put(None)  # Pekne jedovata pill

        for process in processes:
            process.join()

        if self.final_password != "":
            print(f"Ulozene heslo je: {self.final_password.value.decode('utf-8')}")
            return self.final_password.value.decode('utf-8')
        print("Password not found")
        return None


if __name__ == "__main__":

    password_hash = "9e0133f2a137e8eb48b7f27c25f06a7f4f9a3410b045bfe6823246608d1ee827e31e38bde7cfdfcb8702741b60449a3a"
    #ahojj

    queue = multiprocessing.Queue()
    start = time.time()
    Cracker = PasswordCracker(target_hash=password_hash)
    p1 = multiprocessing.Process(target=Cracker.process_manager, args=(6, 4, queue,))
    p1.start()
    p1.join()


    end = time.time()
    print("Vypocet bez trval {:.6f} sec.".format((end - start)))