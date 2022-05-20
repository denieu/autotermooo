def generate_words_file(dictionary_file, words_file, word_size=5):
    """
    Generates a file containing all the words in the dictionary.
    """
    with open(dictionary_file, "r") as dict_fp:
        words = dict_fp.read().splitlines()

    words = [word.lower() for word in words]
    words = filter(lambda word: len(word) == word_size, words)
    words = sorted(words)

    with open(words_file, "w") as words_fp:
        for word in words:
            word = word.strip()
            words_fp.write(word + '\n')


if __name__ == "__main__":
    generate_words_file("dictionaries/pt_br.txt", "words/pt_br.txt")
