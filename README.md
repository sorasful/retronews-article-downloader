# Retonews Image Downloader

A CLI tool using `asyncio` to convert the URL of an retronews.fr article to one or multiple JPG images.
You can specify to get only one

![docker](https://img.shields.io/badge/docker-supported-brightgreen)
![python-3.7](https://img.shields.io/badge/python-3.7-blue)
![python-3.8](https://img.shields.io/badge/python-3.8-blue)


## Install (Using Docker)

Clone the repository :  
`git clone https://github.com/sorasful/retronews-article-downloader.git`  

`cd retronews-article-downloader/`

Build the docker image :  
`docker build -t retronews-downloader .`  

## Usage

See available commands :  
`docker run  retronews-downloader --help`  

Example : Download the page 4 of article https://www.retronews.fr/journal/le-petit-marseillais/24-mars-1938/437/1806613/  
`docker run  retronews-downloader download_page https://www.retronews.fr/journal/le-petit-marseillais/24-mars-1938/437/1806613/ 4`


**Note** : By default images will be created in the `/app/results` folder in the container with the name corresponding to IDs of URL.
For example, the command :  
`docker run  retronews-downloader download_page https://www.retronews.fr/journal/le-petit-marseillais/24-mars-1938/437/1806613/ 4`
will produce `4437-11806613-4.jpg`  so you can use `docker cp` to get the image you seek.

Or you can mount a volume like this :  
`docker run -v $(pwd)/result:/app/results bnf download_page https://www.retronews.fr/journal/le-petit-marseillais/24-mars-1938/437/1806613/ 4`


## Disclaimer

This tool has been built to train my skills on async libraries with Python. Do not use this project to start a business.  
If you want to get more data or use it for commercial use, please contact https://retronews.fr to check if that's possible.  

I will not be responsible for the use, malfunctioning of this tool.
