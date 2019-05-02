# RIRI 
### ralsei image retrieval interface


RIRI is a tool for retrieving pictures of Ralsei from the internet en masse. This tool can very well be used to retrieve any image, as the finders are flexible in what URLs may be supplied, but why would you ever need any other pictures?


# NOTE
This tool is still very much in development, and may or may not be fully realized as an extensible program due to its nature as something that started entirely as a joke. Current plans are to add more finders and improve code quality overall, nothing more (at the moment).

# USAGE

RIRI may be operated from the command line by simply invoking the module. For now, you'll have to clone this repository itself and call it with `py -m riri`

Commands include:
* list - lists all available finders
* find - executes the given finder with the given arguments

Current available finders are:
* tumblr - retrieves images from Tumblr without an API key via scraping