To compile the C code do `$ gcc -shared -o example.so -fPIC test.c`

It's interesting to note that even if a vacancy does not reach the surface, it will still be trapped in layers 3 and 4 indefinitely, maybe this would not produce a GR1 signal, making it effectively destroyed?
### TODO:
* Make it so that the final image of the last neb is the initial image of the next neb, this will also fix any indexing issues.
* Write a quick function that just makes a vacancy in a given layer so that you could start the run from any height, 
will probably just have to start from the centre and then just recursively work your way up to the top.
* Currently there are fluctuations between layers that shouldn't be there, finite size effects?
