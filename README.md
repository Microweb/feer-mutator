# Mutator

Get user activity from hubstaff application and save summary in file.

# How to install 

Go into the project and run command:
```bash
pip install -e .
```
> Required Python: 3.10

## Usage

Setup env
```bash
$ cp .env.default .env
$ export $(cat .env | xargs)
```

Render summary for yesterday (default)
```bash
mutator
```

If you want generate summary for other day, you can just add relative day param.
```bash
mutator --day -2
```

### TODO
* Better handling http errors
* Setup from cmd line where to save a file
