# sec_filings

To get started with the project create a virtual environment using the command:

```
python -m venv venv
```

Then install all the dependencies in the requirement.txt file using the following command:
```
pip install -r requirements.txt
```

To get started with the API, source your virtual enviroment then and start the server using:
```
uvicorn main:app --reload
```

The server will start on http://localhost:8000

To get the filing of a certain company fora certain year all you do is placing the variables in the url, see the example:
```
http://localhost:8000/<ticker>/<year>/<filing>
```
Example: 
```
http://localhost:8000/tsla/2023/10-k
```

I have also made an endpoint that shows the latest 10-K's for big 5 US companies: Apple, Amazon, Alphabet, Netflix, and Meta. You can access it using:
```
http://localhost:8000/example
```

the '/' endpoint is reserved to serve an HTML page in future to make a simple interface that let you do filing retrieval manually and easily.

