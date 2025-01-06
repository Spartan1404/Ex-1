import unittest

from server_logic import calc_ponderation


class ServerTest(unittest.TestCase):
    known_values = (
        (1000, 'aa'),
        (1000, 'aA'),
        (1000, 'Aa'),
        (1000, 'AA'),
        (1000, 'PHsjKb dKgOfdImDPe1hQhWQTSXtYL6AJi4o2UjOLX mDeD4dpectwAaTa0tyhCJj8SDI7DL8bpw1 25YsxrjuExBy2UTalO53JJ'),
        (1000, 'PHsjKb dKgOfdImDPe1hQhWQTSXtYL6AJaa34o2UjOLX mDeD4dpectwTa0tyhCJj8SDI7DL8bpw1 25YsxrjuExBy2UTalO53JJ'),
        (1000, 'PHsjKb dKgOfdImDPe1hQhWQTSXtYL6AJi4o2UjOLX mDeD4dpectwAaTa0tyhCJj8SDI7DLAApw1 25YsxrjuExBy2UTalO53JJ'),
        (1000, 'PHsjKb dKgOfdImDPe1hQhWQTSXtYL6AJi4o2UjOLX mDeD4dpectwAaTa0tyhCJaASDI7DL8bpw1 25YsxrjuExBy2UTalO53JJ'),
        (0, ''),
        (0, '  '),
        (0, '   '),
        (0, 'qwertyuiopasdfghjklzxcvbnm'),
        (0, 'QWERTYUIOPASDFGHJKLZXCVBNM'),
        (39, 'qwertyuiopasdfghjklzxcv bnm'),
        (39, 'QWERTYUIOPASDFGHJKLZXCV BNM'),
        (0, '123456789'),
        (18, '1234567 89'),
        (0, '123456789qwertyuiopasdfghjklzxcvbnm'),
        (0, '123456789QWERTYUIOPASDFGHJKLZXCVBNM'),
        (57, '123456789qwertyuiopasdfghjklzxcvbn m'),
        (28.5, '123456789qwertyuiopasdfghjklzxcvbn  m'),
        (19, '123456789qwertyuiopasdfghjklzxcvbn   m'),
    )

    def test_ponderation_return(self):
        for pond, chain in self.known_values:
            result = calc_ponderation(chain=chain)
            self.assertEqual(pond, result)

    def test_ponderation_custom_skip_chain(self):
        result = calc_ponderation("b1bb", skip_chain=('bb',))
        self.assertEqual(result, 1000)


if __name__ == '__main__':
    unittest.main()