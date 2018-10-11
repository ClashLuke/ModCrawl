*This is a tiny Project you can use to scrape data, you will need to enter a regular expression and a root URL you want to scrape. It will pseudo-recursively reuse the links it has found by the previous generations*


**Dependencies**
Those scripts use Python3, to enable Python2 support, uncomment the first line in deps.py.
Using Python3, you will need to download the following libraries:
	re
	requests
You can install those dependencies using the following command `python3 -m pip install re requests`.

Using Python2, you will need to download the following libraries:
	sets
	re
	requests
You can install those dependencies using the following command `python2 -m pip install sets re requests`.


**Scripts**

*main.py*
This is the main part of the program, its simply automating the dependencies declared in deps.py while giving a nice debug.

*deps.py*
This is simply the dependency package, it contains some useful things such as a fancy input function, a file merger (which removes the original files) and a multi-platform clear function, to make sure your console is always as tidy as it should be.


**Please note, that this Project is still under development. It works perfectly fine on Ubuntu Machines**

The color coding in the print functions may not work on older machines, you can remove them without doing any harm to the program.

If you have got any issues, please open a case.
If you know how to improve parts of the code, make sure to send a pull request.


