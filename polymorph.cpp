#include <iostream>

struct Animal {
    void (*do_it)(void);
};

struct Dog : Animal {
    static void bark() {
        std::cout << "Woof!" << std::endl;
    }

    Dog () {
        do_it = bark;
    }
};

struct Cat : Animal{
    static void meow() {
        std::cout << "Bark!" << std::endl;
    }

    Cat () {
        do_it = meow;
    }
};

void poke(const Animal& a) {
    a.do_it();
}

int main() {
    Dog dog {};
    Cat cat {};

    poke(dog);
    poke(cat);
}