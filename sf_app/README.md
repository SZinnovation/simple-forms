Simple forms web app
====================

Demonstrate SQLAlchemy integration with Morepath through more.transaction.

See the [more.transaction documentation][1] to learn more about what is going
on.

[1]: https://github.com/morepath/more.transaction

Installation
------------

I recommend using pip in a virtual env:

    $ virtualenv sf_env
    $ source sf_env/bin/activate
    $ sf_env/bin/pip install -e .

Then to run the web server:

    $ sf_env/bin/sf_app

You can now access the application through http://localhost:5000
The `-e` option for pip means we don't have to rebuild / re-install after changes if we're running locally
