from text import Stemmer

if __name__ == "__main__":
    g = Stemmer()
    # print(g.get_base("снующий"))
    file = input("Введите название файла:")
    result = []
    with open(file, "r", encoding="utf8") as text_file:
        read_content = text_file.read().split(" ")    
        for content in read_content:
            result.append((content, g.get_base(content)))
    
    with open("result.txt", "w", encoding="utf8") as writer:
        result.sort(key=lambda x: x[0])
        for i in result:
            writer.write(i[0] + "\t\t" + i[1] + "\n")