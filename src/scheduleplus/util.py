def parse_minute(minutes: str):
    minutes_list = []
    for part in minutes.split(","):
        start, end, step = 0, 59 + 1, 1
        if part == "*":
            for num in range(start, end, step):
                if num not in minutes_list:
                    minutes_list.append(num)
        elif "/" in part:
            tmp = part.split("/")
            if tmp[0] != "*":
                if "-" in tmp[0]:
                    tmp2 = tmp[0].split("-")
                    start, end = int(tmp2[0]), int(tmp2[1]) + 1
                else:
                    start, end = int(tmp[0]), int(59) + 1
            step = int(tmp[1])
            for num in range(start, end, step):
                if num not in minutes_list:
                    minutes_list.append(num)
        elif "-" in part:
            tmp2 = part.split("-")
            start, end = int(tmp2[0]), int(tmp2[1]) + 1
            for num in range(start, end, step):
                if num not in minutes_list:
                    minutes_list.append(num)
        else:
            if int(part) not in minutes_list:
                minutes_list.append(int(part))
    minutes_list.sort()
    return minutes_list


if __name__ == "__main__":
    print(parse_minute("*"))
