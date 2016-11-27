import getopt
import logging
import json
import os
import sys
import shutil
import subprocess
#import Image

def readJson(jsonRelPath):

    with open(jsonRelPath) as f:
        strJson = f.read()

    return json.JSONDecoder().decode(strJson)

def getThumbColumnsRows(numImages):
    if numImages <= 8: return (2,4)
    if numImages == 9: return (3,3)
    if numImages == 10: return (2,5)
    if numImages == 11: return (3,4)
    if numImages == 12: return (3,4)
    if numImages == 13: return (3,5)
    if numImages == 14: return (3,5)
    if numImages == 15: return (3,5)
    if numImages == 16: return (4,4)
    if numImages >= 17: return (4,5)
    
def genGalleryXml(aJsonPath, galleryXmlRelPath):

    jsonRoot = readJson(aJsonPath)
    
    xmlLines = ['<?xml version="1.0" encoding="UTF-8"?>',
                '',
                '<simpleviewergallery',
                '',
                'galleryStyle="MODERN"']
    xmlLines.append('title="%s"' % jsonRoot['title'])
    xmlLines.append('textColor="0000000"')
    xmlLines.append('frameColor="222222"')
    xmlLines.append('frameWidth="20"')
    xmlLines.append('thumbPosition="LEFT"')

    numImages = len(jsonRoot["images"])
    thumbColumns, thumbRows = getThumbColumnsRows(numImages)
    xmlLines.append('thumbColumns="%s"' % thumbColumns)
    xmlLines.append('thumbRows="%s"' % thumbRows)

    xmlLines.append('showOpenButton="TRUE"')
    xmlLines.append('showFullscreenButton="TRUE"')
    xmlLines.append('maxImageWidth="1000"')
    xmlLines.append('maxImageHeight="1000"')
    xmlLines.append('useFlickr="false"')
    xmlLines.append('flickrUserName=""')
    xmlLines.append('flickrTags=""')
    xmlLines.append('languageCode="AUTO"')
    xmlLines.append('languageList=""')
    xmlLines.append('imagePath="images/"')
    xmlLines.append('thumbPath="thumbs/"')
    xmlLines.append('>')
	
    for image in jsonRoot['images']:
        xmlLines.append('<image imageURL="images/%s" thumbURL="thumbs/%s" linkURL="" linkTarget="" >' % (image['image'], image['image']))
        xmlLines.append('  <caption>%s</caption>' % image['caption'])
        xmlLines.append('</image>')

    xmlLines.append('</simpleviewergallery>')

    logging.info("Creating file %s" % galleryXmlRelPath)
    with open(galleryXmlRelPath, 'w') as f:
        f.write("\n".join(xmlLines))

def doFolderIndex(jsonRelPath, indexHtmlRelPath):

    json = readJson(jsonRelPath)

    htmlLines = ['<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">',
        '<html>',
        '<head>',
        '  <meta http-equiv="content-type" content="text/html; charset=utf-8">'
        '  <title>%s</title>' % json['title'],
        '</head>',
        '<body',
        '',
        '    <!--START SIMPLEVIEWER EMBED.-->',
        '    <script type="text/javascript" src="../../svcore/js/simpleviewer.js"></script>',
        '    <script type="text/javascript">',
        '    simpleviewer.ready(function () {',
        "        simpleviewer.load('sv-container', '100%', '100%', 'ffffff', true);",
        '    });',
        '    </script>',
        '    <div id="sv-container"></div>',
        '    <!-- END SIMPLEVIEWER EMBED -->',
        '',
        '</body>',
        '</html>']

    logging.info("Creating file %s" % indexHtmlRelPath)

    with open(indexHtmlRelPath, 'w') as f:
        f.write('\n'.join(htmlLines))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try: 
        optlist, args = getopt.getopt(sys.argv[1:], 'j:l:')
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)
    
    jsonRelPath = ""
    indexHtmlRelPath = ""

    for opt, a in optlist:
        if opt == '-j':
            jsonRelPath = a

        if opt == '-l':
            indexHtmlRelPath = a

    doFolderIndex(jsonRelPath, indexHtmlRelPath)
    galleryXmlRelPath = os.path.join(os.path.dirname(indexHtmlRelPath), "gallery.xml")
    genGalleryXml(jsonRelPath, galleryXmlRelPath)
