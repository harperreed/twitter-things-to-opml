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




