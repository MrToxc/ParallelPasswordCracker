import hashlib
import multiprocessing
import string




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




    def worker_crack_password(self, symbols_count, start_index, end_index):
        password_index_list = [0] * symbols_count
        print(password_index_list)
        counter = 0
        password_index_list[0] = start_index
        while (password_index_list is not False and password_index_list[0] != end_index) and self.finish_flag.value == 0:
            counter += 1
            if counter >= 300000:
                counter = 0
                print(self.get_password_from_index_list(password_index_list) + "////start:" +  str(self.final_char_set[start_index]) + "/end:" + str(self.final_char_set[end_index-1]))
            current_password = self.get_password_from_index_list(password_index_list)
            if hashlib.sha384(current_password.encode('utf-8')).hexdigest() == self.hash_target:
                # Ulozeni do sdilene pameti (musime prevest na bytes)
                self.final_password.value = current_password.encode('utf-8')
                self.finish_flag.value = 1 #True
                return self.get_password_from_index_list(password_index_list)
            password_index_list = self.increment_index_list(password_index_list)
        #password not found
        return None




    def process_manager(self, max_chars, max_processes):

        password_index_list = []
        base, rem = divmod(len(self.final_char_set), max_processes)
        self.finish_flag.value = 0

        processes = []

        for symbols_count in range(1, max_chars + 1):
            if self.finish_flag.value == 1:
                break

            password_index_list.append(0)
            for process in range(0, max_processes):
                #genialni matika od chata, tohle bych fakt nevymyslel TBH
                start = process * base + min(process, rem)
                size = base + (1 if process < rem else 0)
                #konec genialni matickyy
                end = start + size
                password_index_list[0] = start

                p = multiprocessing.Process(target=self.worker_crack_password, args=(symbols_count, start, end))
                p.start()
                processes.append(p)
            for pro in processes:
                pro.join()
            processes.clear()

        if self.final_password != "":
            print(f"Ulozene heslo je: {self.final_password.value.decode('utf-8')}")
            return self.final_password.value.decode('utf-8')
        print("Password not found")
        return None


if __name__ == "__main__":
    password_hash = "aeeff5df4d122b5926acd916bea10fbc9362bd21b16fe049a2b242d4e6a2af93e7974358da58ee31bdc17e12bd68a19a"
    # heslo je "ahoj"
    print(lower_case_alphabet)
    print(upper_case_alphabet)
    print(numbers)
    print(special_characters)
    for i in range(1, 3):
        teststring = i * "a"
        print(teststring)



    Cracker = PasswordCracker(target_hash=password_hash)
    Cracker.process_manager(9, 8)