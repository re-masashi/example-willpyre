# An Example using Willpyre

A simple Book Store app.

This app uses:
- willpyre (the core of the app).
- SQLAlchemy (may move to Gino in the future) for DB queries.
- ItsDangerous for signing cookies.
- Jinja2 for templating.


**Note:** This app has uvicorn as a dependency but there are some [problems](https://github.com/encode/uvicorn/discussions/1876).
    If your app seems to behave wierd, kindly use [Hypercorn](https://gitub.com/pgjones/hypercorn).

### Run

```bash
git clone https://github.com/re-masashi/example-willpyre.git
cd example-willpyre
pip install -r requirements.txt
python -m uvicorn main:app
```

Using Hypercorn:
```bash
git clone https://github.com/re-masashi/example-willpyre.git
cd example-willpyre
pip install -r requirements.txt 
pip install hypercorn
python -m hypercorn main:app
```

Now you can visit the pages in your browser at http://127.0.0.1.

There is no issue template right now. Feel free to raise one for any query (however, [discussions](https://github.com/re-masashi/example-willpyre/discussions) are preffered).

