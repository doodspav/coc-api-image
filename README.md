# coc-api-image
This repo lets you generate a image of someone's main base profile in clash of clans using their #.

Uses the clash of clans api - get an api key at https://developer.clashofclans.com/

Tutorial
------
Use python 2.7 (and I'm 99% sure it works in python 3.x)

Using git:

    $ git clone http://github.com/doodspav/coc-api-image
 
Python packages:

    $ pip install numpy
    $ pip install pillow
    $ pip install fonttools

You will need to get an api key from https://developer.clashofclans.com/.

Bear in mind that api keys are IP specific.

Use the api_key as show in the example (usage denoted by api_key).

Use the example.py file to create an image in the same folder that everything else is in. The image will be called test.jpg.

    $ python example.py

If you are using this on a bot, please credit me in your bot's message that display's all its commands.

Errors
------
An invalid api key will generate a _404_ error.

An invalid #player_tag will return a _403_ error.

For any other error, start an issue.

Author
------

doodspav

LINE ID - doodspav

COC - #ULP92C2

Credits
------

Akkey Kami (LINE ID - akkey_god): helped with font issues
