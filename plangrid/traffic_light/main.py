from intersection import Intersection
from light import Light


def main():
    intersection = Intersection([Light('1'), Light('2'), Light('3')])
    intersection.run(40)

if __name__ == '__main__':
    main()
