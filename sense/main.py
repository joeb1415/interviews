from instacart import Instacart


def main():
    instacart = Instacart()
    instacart.load_data(train_only=True)
    print(instacart.report_1())
    # print(instacart.report_2(20))

if __name__ == '__main__':
    main()
