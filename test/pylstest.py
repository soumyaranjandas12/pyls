import unittest
from subprocess import check_output


class MyTestCase(unittest.TestCase):
    def test_ls_cmd(self):
        output = check_output(["python", "-m", "pyls"], text=True).strip()
        self.assertTrue(output == "LICENSE README.md ast go.mod lexer main.go parser token")

    def test_ls_cmd_A(self):
        output = check_output(["python", "-m", "pyls", "-A"], text=True).strip()
        self.assertTrue(output == ".gitignore LICENSE README.md ast go.mod lexer main.go parser token")

    def test_l_cmd_path(self):
        output = check_output(["python", "-m", "pyls", "-l", "parser"], text=True).strip()
        self.assertTrue(output == "drwxr-xr-x 533 Nov 14 16:03 go.mod\n"
                                  "-rw-r--r-- 1.6K Nov 17 12:05 parser.go\n"
                                  "drwxr-xr-x 1.3K Nov 17 12:51 parser_test.go")

    def test_l_cmd_path_file(self):
        output = check_output(["python", "-m", "pyls", "-l", "parser/parser.go"], text=True).strip()
        self.assertTrue(output == "-rw-r--r-- 1.6K Nov 17 12:05 ./parser/parser.go")

    def test_l_r(self):
        output = check_output(["python", "-m", "pyls", "-l", "-r"], text=True).strip()
        self.assertTrue(output == "-rw-r--r-- 4.0K Nov 14 14:57 token\n"
                                  "drwxr-xr-x 4.0K Nov 17 12:51 parser\n"
                                  "-rw-r--r-- 74 Nov 14 13:57 main.go\n"
                                  "drwxr-xr-x 4.0K Nov 14 15:21 lexer\n"
                                  "drwxr-xr-x 60 Nov 14 13:51 go.mod\n"
                                  "-rw-r--r-- 4.0K Nov 14 15:58 ast\n"
                                  "drwxr-xr-x 83 Nov 14 11:27 README.md\n"
                                  "drwxr-xr-x 1.0K Nov 14 11:27 LICENSE")

    def test_l_r_t(self):
        output = check_output(["python", "-m", "pyls", "-l", "-r", "-t"], text=True).strip()
        self.assertTrue(output == "drwxr-xr-x 4.0K Nov 17 12:51 parser\n"
                                  "-rw-r--r-- 4.0K Nov 14 15:58 ast\n"
                                  "drwxr-xr-x 4.0K Nov 14 15:21 lexer\n"
                                  "-rw-r--r-- 4.0K Nov 14 14:57 token\n"
                                  "-rw-r--r-- 74 Nov 14 13:57 main.go\n"
                                  "drwxr-xr-x 60 Nov 14 13:51 go.mod\n"
                                  "drwxr-xr-x 83 Nov 14 11:27 README.md\n"
                                  "drwxr-xr-x 1.0K Nov 14 11:27 LICENSE")

    def test_filter_dir(self):
        output = check_output(["python", "-m", "pyls", "-l", "--filter=dir"], text=True).strip()
        self.assertTrue(output == "-rw-r--r-- 4.0K Nov 14 15:58 ast\n"
                                  "drwxr-xr-x 4.0K Nov 14 15:21 lexer\n"
                                  "drwxr-xr-x 4.0K Nov 17 12:51 parser\n"
                                  "-rw-r--r-- 4.0K Nov 14 14:57 token")

    def test_filter_file(self):
        output = check_output(["python", "-m", "pyls", "-l", "--filter=file"], text=True).strip()
        self.assertTrue(output == "drwxr-xr-x 1.0K Nov 14 11:27 LICENSE\n"
                                  "drwxr-xr-x 83 Nov 14 11:27 README.md\n"
                                  "drwxr-xr-x 60 Nov 14 13:51 go.mod\n"
                                  "-rw-r--r-- 74 Nov 14 13:57 main.go")

