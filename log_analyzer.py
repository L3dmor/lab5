import gzip, io, os, re

config = {
    "DIRECTORY": "./log"
}


def main():
    #получение списка файлов в директории "log"
    log_file = os.listdir(config.get('DIRECTORY'))
    #если файлов нет, возвращаем сообщение
    if not log_file:
        return print(f'No Logs')
    #переменная, содержащая путь к файлам
    file = f'{config.get("DIRECTORY")}./{log_file[-1]}'
    #компилирование файла для последующего использования
    regex = re.compile(r'\"[A-Z]+ (\S+) .* (\d+\.\d+)\n')
    log = {}
    k = 0

    def read(object):
        nonlocal k
        for line in object:
            result = regex.findall(line)
            k += 1
            if not len(result):
                continue
            url, time = result[0]
            if url not in log:
                log[url] = []
            log[url].append(float(time))

    if os.path.splitext(file)[1] != '.gz':
        with open(file, 'r') as file:
            read(file)
    else:
        with gzip.open(file, 'r') as fileGZ:
            with io.TextIOWrapper(fileGZ, encoding='utf-8') as file:
                read(file)

    for number in log:
        count = len(log[number])
        fi = len(number)
        st = fi-20
        report = (number[st:fi], count, round(count / k * 100, 10), max(log[number]), log[number][count // 2])
        print(report)


if __name__ == "__main__":
    main()
