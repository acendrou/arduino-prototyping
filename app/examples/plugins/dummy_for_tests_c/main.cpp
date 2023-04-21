#include <iostream>


void show_values(int *tab, size_t size) {
    std::cout << "DUMMY PLUGIN C START" << std::endl;
    std::cout << "Values: " << std::endl;

    for(int i = 0; i < size; i++) {
        std::cout << tab[i] << ";";
    }
    std::cout << std::endl;

    std::cout << "DUMMY PLUGIN C END" << std::endl;
}

int* parse_command_line(int argc, char  *argv[]) {
    int *tab = new int[argc];

    for(int i = 0; i <= argc; i++) {
        tab[i] = std::atoi(argv[i+1]);
    }
    return tab;
}

int main(int argc, char *argv[]) {
    std::cout << "DUMMY PLUGIN C CALLED" << std::endl;
    if (argc == 1) {
        std::cout << "No values" << std::endl;
        return 0;
    }

    int *values = parse_command_line(argc, argv);
    show_values(values, argc);
    return 0;
}



