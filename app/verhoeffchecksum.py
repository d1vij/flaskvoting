from random import randint

def random_number() -> int: return randint(10**10,10**11-1) #random 11 digit number

class VerhoeffChecksum:
    """
    Implementation of the Verhoeff checksum algorithm, a digit-based checksum used for error detection
    in numerical data such as identification numbers. Modification of this algorithm is used to generate aadhar numbers (infact this can verify aadhar numbers).
        d : The permutation table (d) used to calculate intermediate checksum values.
        p : The permutation table (p) used to map digits based on their position in the number.
        inv : The inverse table (inv) used to calculate the final checksum digit or validate the checksum.

    Algorithm Description:
        1. The Verhoeff algorithm uses three main components:
            - The d table for mapping intermediate checksum states.
            - The p table for permuting digits based on their position in the number (cyclically modulo 8).
            - The inv table to compute the inverse of the final checksum state.
        2. To calculate the checksum for a number:
            - Start with an initial checksum value of 0.
            - For each digit in the number (processed right-to-left):
                - Select the appropriate row in the p table based on the digit's position (mod 8).
                - Use the p table to map the current digit to a new value.
                - Update the checksum state using the d table and the mapped value.
            - Compute the final checksum digit using the `inv` table.
                - final checksum digit = inv[checksum digit obtained in the end]

        3. To verify a number containing a checksum:
            - Repeat the steps above but start with a checksum value of 0 and include the checksum digit in the computation.
            - A valid number will result in a final checksum value of 0.


    Sources:
        1. Inspiration  : https://medium.com/@krs.sharath03/how-aadhar-number-is-generated-and-validated-3c3e7172e606
        2. Explaination of algorithm : https://www.youtube.com/watch?v=yaoSdFAL4UY

    """


    #permutation table
    d =  [
    #   (x,y) ≈ (c,m)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
        [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
        [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
        [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
        [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
        [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ]


    # Permutation table (p)
    p = [
    #   (x,y)≈( (i+1)%8, n)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
        [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
        [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
        [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
        [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
    ]

    #inverse table
    inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]

    @classmethod
    def add_checksum_to(cls, number: int) -> int:
        """
        :param number: Number to add checksum to
        :return: Number with last digit as the checksum value
        """
        number = str(number)
        c = 0
        for i, n in enumerate(reversed(number)):

            c = cls.d[c][ cls.p[(i + 1) % 8][int(n)] ] # m = p[ (i+1) %8 ][n] |-> Where i is the index of digit n from right
        c_final = cls.inv[c]
        return int(number + str(c_final))

    @classmethod
    def validate_number(cls, number: int) -> bool:
        """
        :param number: Number to validate
        :return: True if valid else false
        """
        number = str(number)
        c = 0
        for i, n in enumerate(reversed(number)):
            c = cls.d[c][ cls.p[i % 8][int(n) ]]
        return c == 0




if __name__ == '__main__':
    number = random_number()
    checked_number = VerhoeffChecksum.add_checksum_to(number)
    validity_of_original = VerhoeffChecksum.validate_number(number)
    validity_of_checked = VerhoeffChecksum.validate_number(checked_number)
    print(f"number {number}\nChecked number {checked_number}\nOriginal number valid? {validity_of_original}\nChecked number valid? {validity_of_checked}")
