#include <stdio.h>

#define to ,
#define from ,
#define repeat(x) for (int i = 0; i < x; i++) {
#define when int
#define flag main()
#define clicked {
#define end }
#define stop ;
#define all return 0;
#define this_block break;
#define say(x) puts(x)
#define think(x) puts(x)
#define broadcast goto
#define repeat_until while
#define then ){
#define not !
#define and &&
#define or ||
#define if if(
#define function void
#define does (){
#define broadcasts __label__
#define else }else{

function ohno does
    repeat(10)
        say("Math doesnt work!!!");
    end
end

function ohgood does
    repeat(10)
        say("Math works!!!");
    end
end

when flag clicked
    broadcasts math_works, math_doesnt_work;
    
    repeat(10)
        say("Hello World!");
    end

    if 1 == 1 and 2 == 2 then
        broadcast math_works;
    else
        broadcast math_doesnt_work;
    end

    math_doesnt_work:
        ohno();
        stop all;

    math_works:
        ohgood();
        stop all;
end
