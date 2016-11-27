import getopt
import logging
import json
import os
import sys

def readJson(jsonRelPath):

    with open(jsonRelPath) as f:
        strJson = f.read()

    return json.JSONDecoder().decode(strJson)


def doMovieHtml(jsonRelPath, movieRelPath):

    json = readJson(jsonRelPath)
    movieName = os.path.basename(movieRelPath)[0:-4]
    title = json['title']
    html = """
<html>
<head>
<title>%s</title>
</head>
<body>

<!-- first try HTML5 playback: if serving as XML, expand `controls` to `controls="controls"` and autoplay likewise -->
<!-- warning: playback does not work on iOS3 if you include the poster attribute! fixed in iOS4.0 -->
<video width="480" height="270" controls autoplay>
	<!-- MP4 must be first for iPad! -->
	<source src="%s.mp4" type="video/mp4" /><!-- Safari / iOS video    -->
	<source src="%s.ogv" type="video/ogg" /><!-- Firefox / Opera / Chrome10 -->
	<!-- fallback to Flash: -->
	<object width="480" height="270" type="application/x-shockwave-flash" data="player.swf">
		<!-- Firefox uses the `data` attribute above, IE/Safari uses the param below -->
		<param name="movie" value="player.swf" />
		<param name="flashvars" value="autoplay=true&amp;controlbar=over&amp;file=%s.mp4" />
		<!-- fallback image. note the title field below, put the title of the video there -->
		<img src="images/IMG_0349.jpg" width="480" height="270" alt=""
		     title="No video playback capabilities, please download the video below" />
	</object>
</video>
<!-- you *must* offer a download link as they may be able to play the file locally. customise this bit all you want -->
<p>	<strong>Download link:</strong>
		<a href="%s.mp4">%s.mp4</a>
</p>

</body>
</html>
""" % (title, movieName, movieName,movieName,movieName,movieName)
       
    movieHtmlRelPath = os.path.join(os.path.dirname(movieRelPath), "movie.html")
    with open(os.path.join(movieHtmlRelPath), 'w') as f:
        f.write(html)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try: 
        optlist, args = getopt.getopt(sys.argv[1:], 'j:m:')
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)
    
    jsonRelPath = ""
    mp4RelPath = ""

    for opt, a in optlist:
        if opt == '-j':
            jsonRelPath = os.path.join(os.path.dirname(a), "a.json")

        if opt == '-m':
            mp4RelPath = a

    doMovieHtml(jsonRelPath, mp4RelPath)

