/******************************************************************************
                                  
                                UUID Generator

*******************************************************************************/

#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

char *generate_uuid(char* uuid, int max_size){
    
    // Get random 2 bytes each, totalling 16 bytes
    int firstTwoBytes = rand() % 65535;
    int secondTwoBytes = rand() % 65535;
    int thirdTwoBytes = rand() % 65535;
    int fourthTwoBytes = rand() % 65535;
    int fifthTwoBytes = rand() % 65535;
    int sixthTwoBytes = rand() % 65535;
    int seventhTwoBytes = rand() % 65535;
    int eightTwoBytes = rand() % 65535;
    
    // Set the four MSB of the 7th byte to 0100'byte
    fourthTwoBytes = fourthTwoBytes & 0x4FFF | 0x4000;

    // Set the two most significant bits of the 9th byte to 10'B
    fifthTwoBytes = (fifthTwoBytes & 0x3FFF) | ((0xB & 0xF) << 12 & 0xC000);
    
    // Initialize char array to hold the hex values
    char firstPart[5];
    char secondPart[5];
    char thirdPart[5];
    char fourthPart[5];
    char fifthPart[5];
    char sixthPart[5];
    char seventhPart[5];
    char eightPart[5];

    // Converting the integer to hexstring
    sprintf(firstPart, "%X", firstTwoBytes);
    sprintf(secondPart, "%X", secondTwoBytes);
    sprintf(thirdPart, "%X", thirdTwoBytes);
    sprintf(fourthPart, "%X", fourthTwoBytes);
    sprintf(fifthPart, "%X", fifthTwoBytes);
    sprintf(sixthPart, "%X", sixthTwoBytes);
    sprintf(seventhPart, "%X", seventhTwoBytes);
    sprintf(eightPart, "%X", eightTwoBytes);

    // Building the final UUID string
    memset(uuid, '\0', max_size + 1);
    strncpy(uuid, firstPart, 4);
    strncat(uuid, secondPart, 4);
    strcat(uuid, "-");
    strncat(uuid, thirdPart, 4);    
    strcat(uuid, "-");
    strncat(uuid, fourthPart, 4);    
    strcat(uuid, "-");
    strncat(uuid, fifthPart, 4);
    strcat(uuid, "-");
    strncat(uuid, sixthPart, 4);
    strncat(uuid, sixthPart, 4);
    strncat(uuid, seventhPart, 4);
    strncat(uuid, eightPart, 4);
    
    return uuid;
}

int get_uuid(char uuid[])
{

    /* To call in python
    
    from ctypes import *
    uuid_lib =cdll.LoadLibrary("uuid_gen.so")
    s = create_string_buffer(b'\x00' * 37)
    uuid_lib.get_uuid(s)
    s.value

    To compile:
    gcc uuid_generator.c -c -fPIC
    gcc -shared -fPIC -o uuid_gen.so uuid_generator.o 
    */

    srand(time(NULL));   // Initialization, should only be called once.
    generate_uuid(uuid, 37);
    return 0;
}
