# Twitter things to OPML file

Since twitter is kind of dying, i wanted to grab as much of the magic as i could. I use twitter lists a lot and i wanted to grab my friends, and my list members feeds into a bunch of nice OMPL files for import into a feed reader. 

This barely works! 

## Usage

1. Clone this repo
2. install the dependencies `pip install -r requirements.txt`
3. copy `example.env` to `.env`
4. edit the `.env` file with your twitter api keys, and `screen_name`
5. 
6. run `python twitter-friends-to-feeds.py` to get your friends feeds in an nice OPML file
7. run `python twitter-lists-to-feeds.py` to get your lists feeds in an nice OPML file

It will cache the request and twitter calls for 3 days. You can clear the cache by updating the `CLEAR_CACHE` env var to `true`.

### Output

This will output a BUNCH of opml files. I suggest importing them into your feed reader and checking them out. 

## Bugs

- It will sometimes find duplicate feeds. I dont do anything about this.
- It will find a billion comment feeds. I dont do anything about this either. 
- It will sometimes crash cuz i am bad at python. I haven't done anything about this in about 20 years.
- It will sometimes run into a site that doesn't exist, or is down. I try and catch it, but it may crash and put you into a weird cache state. 

## TODO

- [ ] Make this work
- [ ] Make this work better
- [ ] Make this work betterer
- [ ] Make this work bettererer
- [ ] Make this work betterererer
- [ ] Make this work bettererererer

*^ this todo list was writter by copilot. lol*


## License

MIT

## Inspiration

- https://github.com/bslatkin/tweeps2opml - i am so bad at go. Brett is awesome and i am a bad person
- https://twitter.com/luca/status/1029354370620694530?s=20 - this is probably WAY WAY less work than this




