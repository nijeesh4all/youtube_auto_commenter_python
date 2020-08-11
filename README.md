# Youtube Auto Comment Shitposter

This script allows you to make comments on youtube which doesnt contribute towards anything on that channel or to anyone who reads it. 

This make a comment on youtube which says 

> This comment has { x } likes which is { y } less/more than the video.

where x is the number of likes the comment has
and y is the differance of likes for the video and the comment 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar. and i recommend using `virtalenv` as well or you can just  run the code in docker if you dont want to screw up your local env for something so useless.

### if you want to use `virtualenv` 
```bash
pip install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install -r reqirements.text
```

### Else
```bash
pip install -r reqirements.text
```

Also you need to create an `credentials.json` file from the google-APIs to make requests to youtube

https://developers.google.com/youtube/registering_an_application

>Its important that you get credentails for a desktop app

## Usage

### running directly
```bash
python3 handler.py
```

### runing on docker

```bash
docker build . spam_youtube
docker run spam_youtube
```

## Configs

You can change the congifs in `config.init ` to customise the behaviour to some extend

<b>video_url</b> : <b> youtube video url </b>

<b>delete_comment_after</b>: <b> If you want to delete the comment on exit </b> 

<b>comment_thread_id </b> : <b> If you you wnat to reuse another comment  </b>

<b>polling_interval</b> : <b> Poling intervel in seconds</b>

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)