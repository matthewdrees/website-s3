import argparse
import logging
import json
import os
import sys
import shutil
import subprocess
from PIL import Image

def createImagesAndImageHtml(inputpath, inputjson, outputpath):
    '''Creates copies of properly sized images and returns image html.

    :param inputpath: path/to/content
    :param inputjson: input json from a.json file
    :param outputpath: path/to/output
    :return: html of images section

    Need to copy 3 types of images from the original:
     - Big: 1600x1200
     - Med: 1024x768
     - Small: 240x180

    If portrait, the inverse.

    If panormaic, cap the y axis to the same as landscape.

    So we only have to touch images once, create the html blob and return it
    as a string.

    Create the index.jpg file as well.
    '''

    imageshtml = ''
    for image in inputjson['images']:
        logging.debug(f'processing image {image}')

        def cap_dimensions_by_height(dimensions, y_cap):
            if dimensions[1] > y_cap:
                return (int(dimensions[0]/dimensions[1]*y_cap), y_cap)
            return dimensions

        im = Image.open(os.path.join(inputpath, 'images', image['image']))
        width, height = im.size
        if width >= height:

            # Landscape. Cap each image to a given height, keep the aspect ratio.
            photo_dimensions_big = cap_dimensions_by_height(im.size, 1200)
            photo_dimensions_med = cap_dimensions_by_height(im.size, 768)
            photo_dimensions_low = cap_dimensions_by_height(im.size, 180)

        else:
            # Portait.
            photo_dimensions_big = cap_dimensions_by_height(im.size, 1600)
            photo_dimensions_med = cap_dimensions_by_height(im.size, 1024)
            photo_dimensions_low = cap_dimensions_by_height(im.size, 240)

        image_basename = os.path.basename(image['image'])
        bigname = image_basename + '_b.jpg'
        medname = image_basename + '_m.jpg'
        lowname = image_basename + '_l.jpg'
        im.resize(photo_dimensions_big,Image.BICUBIC).save(os.path.join(outputpath, bigname))
        im.resize(photo_dimensions_med,Image.BICUBIC).save(os.path.join(outputpath, medname))
        im.resize(photo_dimensions_low,Image.BICUBIC).save(os.path.join(outputpath, lowname))

        imageshtml += '''<a href="{}" data-size="{}x{}" data-med="{}" data-med-size="{}x{}" class="demo-gallery__img--main">
         <img src="{}" alt=""/>
         <figure>{}</figure>
        </a>'''.format(bigname,
                photo_dimensions_big[0],
                photo_dimensions_big[1],
                medname,
                photo_dimensions_med[0],
                photo_dimensions_med[1],
                lowname,
                image['caption'])

        # Create the index.jpg file for the overall posting.
        if image['image'] == inputjson['index image']:
            assert(width*3 == height*4), "index image must be 4/3 landscape"
            im.resize((400,300),Image.BICUBIC).save(os.path.join(outputpath, 'index.jpg'))

    return imageshtml

def doFolderIndex(inputjson, imageshtml, outputpath):
    '''Create posting index.html in outputpath.'''

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>%s</title>
  <link href="../../site-assets/site.css?v=4.1.1-1.0.4" rel="stylesheet" />
  <link href="../../photoswipe/photoswipe.css?v=4.1.1-1.0.4" rel="stylesheet" />
  <link href="../../photoswipe/default-skin/default-skin.css?v=4.1.1-1.0.4" rel="stylesheet" />
  <script src="../../photoswipe/photoswipe.min.js?v=4.1.1-1.0.4"></script>
  <script src="../../photoswipe/photoswipe-ui-default.min.js?v=4.1.1-1.0.4"></script>
  <!--    <script src="//use.typekit.net/snf1yod.js"></script> -->
  <!--    <script>try{Typekit.load();}catch(e){}</script> -->
      <!--[if lt IE 9]>
       <script>
          document.createElement('figure');
       </script>
      <![endif]-->
</head>
<body>
 <div class="section section--head">
  <div class="row row--heading">
   <h1>%s</h1>
   <p>%s</p>
  </div>
  <div class="row">
   <div id="demo-test-gallery" class="demo-gallery">
%s
   </div>
  </div>
 </div>
 <div id="gallery" class="pswp" tabindex="-1" role="dialog" aria-hidden="true">
  <div class="pswp__bg"></div>
  <div class="pswp__scroll-wrap">
   <div class="pswp__container">
    <div class="pswp__item"></div>
    <div class="pswp__item"></div>
    <div class="pswp__item"></div>
   </div>
   <div class="pswp__ui pswp__ui--hidden">
    <div class="pswp__top-bar">
     <div class="pswp__counter"></div>
     <button class="pswp__button pswp__button--close" title="Close (Esc)"></button>
     <button class="pswp__button pswp__button--share" title="Share"></button>
     <button class="pswp__button pswp__button--fs" title="Toggle fullscreen"></button>
     <button class="pswp__button pswp__button--zoom" title="Zoom in/out"></button>
     <div class="pswp__preloader">
      <div class="pswp__preloader__icn">
       <div class="pswp__preloader__cut">
        <div class="pswp__preloader__donut"></div>
       </div>
      </div>
     </div>
    </div>
    <div class="pswp__share-modal pswp__share-modal--hidden pswp__single-tap">
     <div class="pswp__share-tooltip">
      <!-- <a href="#" class="pswp__share--facebook"></a>
          <a href="#" class="pswp__share--twitter"></a>
          <a href="#" class="pswp__share--pinterest"></a>
          <a href="#" download class="pswp__share--download"></a> -->
     </div>
    </div>
    <button class="pswp__button pswp__button--arrow--left" title="Previous (arrow left)"></button>
    <button class="pswp__button pswp__button--arrow--right" title="Next (arrow right)"></button>
    <div class="pswp__caption">
     <div class="pswp__caption__center">
     </div>
    </div>
   </div>
  </div>
 </div>
    
  
 <script type="text/javascript">
  (function() {

  var initPhotoSwipeFromDOM = function(gallerySelector) {

    var parseThumbnailElements = function(el) {
      var thumbElements = el.childNodes,
              numNodes = thumbElements.length,
              items = [],
              el,
              childElements,
              thumbnailEl,
              size,
              item;

          for(var i = 0; i < numNodes; i++) {
              el = thumbElements[i];

              // include only element nodes 
              if(el.nodeType !== 1) {
                continue;
              }

              childElements = el.children;

              size = el.getAttribute('data-size').split('x');

              // create slide object
              item = {
            src: el.getAttribute('href'),
            w: parseInt(size[0], 10),
            h: parseInt(size[1], 10),
            author: el.getAttribute('data-author')
              };

              item.el = el; // save link to element for getThumbBoundsFn

              if(childElements.length > 0) {
                item.msrc = childElements[0].getAttribute('src'); // thumbnail url
                if(childElements.length > 1) {
                    item.title = childElements[1].innerHTML; // caption (contents of figure)
                }
              }


          var mediumSrc = el.getAttribute('data-med');
                if(mediumSrc) {
                  size = el.getAttribute('data-med-size').split('x');
                  // "medium-sized" image
                  item.m = {
                      src: mediumSrc,
                      w: parseInt(size[0], 10),
                      h: parseInt(size[1], 10)
                  };
                }
                // original image
                item.o = {
                  src: item.src,
                  w: item.w,
                  h: item.h
                };

              items.push(item);
          }

          return items;
      };

      // find nearest parent element
      var closest = function closest(el, fn) {
          return el && ( fn(el) ? el : closest(el.parentNode, fn) );
      };

      var onThumbnailsClick = function(e) {
          e = e || window.event;
          e.preventDefault ? e.preventDefault() : e.returnValue = false;

          var eTarget = e.target || e.srcElement;

          var clickedListItem = closest(eTarget, function(el) {
              return el.tagName === 'A';
          });

          if(!clickedListItem) {
              return;
          }

          var clickedGallery = clickedListItem.parentNode;

          var childNodes = clickedListItem.parentNode.childNodes,
              numChildNodes = childNodes.length,
              nodeIndex = 0,
              index;

          for (var i = 0; i < numChildNodes; i++) {
              if(childNodes[i].nodeType !== 1) { 
                  continue; 
              }

              if(childNodes[i] === clickedListItem) {
                  index = nodeIndex;
                  break;
              }
              nodeIndex++;
          }

          if(index >= 0) {
              openPhotoSwipe( index, clickedGallery );
          }
          return false;
      };

      var photoswipeParseHash = function() {
        var hash = window.location.hash.substring(1),
          params = {};

          if(hash.length < 5) { // pid=1
              return params;
          }

          var vars = hash.split('&');
          for (var i = 0; i < vars.length; i++) {
              if(!vars[i]) {
                  continue;
              }
              var pair = vars[i].split('=');  
              if(pair.length < 2) {
                  continue;
              }           
              params[pair[0]] = pair[1];
          }

          if(params.gid) {
            params.gid = parseInt(params.gid, 10);
          }

          return params;
      };

      var openPhotoSwipe = function(index, galleryElement, disableAnimation, fromURL) {
          var pswpElement = document.querySelectorAll('.pswp')[0],
              gallery,
              options,
              items;

        items = parseThumbnailElements(galleryElement);

          // define options (if needed)
          options = {

              galleryUID: galleryElement.getAttribute('data-pswp-uid'),

              getThumbBoundsFn: function(index) {
                  // See Options->getThumbBoundsFn section of docs for more info
                  var thumbnail = items[index].el.children[0],
                      pageYScroll = window.pageYOffset || document.documentElement.scrollTop,
                      rect = thumbnail.getBoundingClientRect(); 

                  return {x:rect.left, y:rect.top + pageYScroll, w:rect.width};
              },

              addCaptionHTMLFn: function(item, captionEl, isFake) {
            if(!item.title) {
              captionEl.children[0].innerText = '';
              return false;
            }
            captionEl.children[0].innerHTML = item.title;
            return true;
              },
          
          };


          if(fromURL) {
            if(options.galleryPIDs) {
              // parse real index when custom PIDs are used 
              // http://photoswipe.com/documentation/faq.html#custom-pid-in-url
              for(var j = 0; j < items.length; j++) {
                if(items[j].pid == index) {
                  options.index = j;
                  break;
                }
              }
            } else {
              options.index = parseInt(index, 10) - 1;
            }
          } else {
            options.index = parseInt(index, 10);
          }

          // exit if index not found
          if( isNaN(options.index) ) {
            return;
          }



        var radios = document.getElementsByName('gallery-style');
        for (var i = 0, length = radios.length; i < length; i++) {
            if (radios[i].checked) {
                if(radios[i].id == 'radio-all-controls') {

                } else if(radios[i].id == 'radio-minimal-black') {
                  options.mainClass = 'pswp--minimal--dark';
                  options.barsSize = {top:0,bottom:0};
              options.captionEl = false;
              options.fullscreenEl = false;
              options.shareEl = false;
              options.bgOpacity = 0.85;
              options.tapToClose = true;
              options.tapToToggleControls = false;
                }
                break;
            }
        }

          if(disableAnimation) {
              options.showAnimationDuration = 0;
          }

          // Pass data to PhotoSwipe and initialize it
          gallery = new PhotoSwipe( pswpElement, PhotoSwipeUI_Default, items, options);

          // see: http://photoswipe.com/documentation/responsive-images.html
        var realViewportWidth,
            useLargeImages = false,
            firstResize = true,
            imageSrcWillChange;

        gallery.listen('beforeResize', function() {

          var dpiRatio = window.devicePixelRatio ? window.devicePixelRatio : 1;
          dpiRatio = Math.min(dpiRatio, 2.5);
            realViewportWidth = gallery.viewportSize.x * dpiRatio;


            if(realViewportWidth >= 1200 || (!gallery.likelyTouchDevice && realViewportWidth > 800) || screen.width > 1200 ) {
              if(!useLargeImages) {
                useLargeImages = true;
                  imageSrcWillChange = true;
              }

            } else {
              if(useLargeImages) {
                useLargeImages = false;
                  imageSrcWillChange = true;
              }
            }

            if(imageSrcWillChange && !firstResize) {
                gallery.invalidateCurrItems();
            }

            if(firstResize) {
                firstResize = false;
            }

            imageSrcWillChange = false;

        });

        gallery.listen('gettingData', function(index, item) {
            if( useLargeImages ) {
                item.src = item.o.src;
                item.w = item.o.w;
                item.h = item.o.h;
            } else {
                item.src = item.m.src;
                item.w = item.m.w;
                item.h = item.m.h;
            }
        });

          gallery.init();
      };

      // select all gallery elements
      var galleryElements = document.querySelectorAll( gallerySelector );
      for(var i = 0, l = galleryElements.length; i < l; i++) {
        galleryElements[i].setAttribute('data-pswp-uid', i+1);
        galleryElements[i].onclick = onThumbnailsClick;
      }

      // Parse URL and open gallery if it contains #&pid=3&gid=1
      var hashData = photoswipeParseHash();
      if(hashData.pid && hashData.gid) {
        openPhotoSwipe( hashData.pid,  galleryElements[ hashData.gid - 1 ], true, true );
      }
    };

    initPhotoSwipeFromDOM('.demo-gallery');

  })();
  </script>
</body>
</html>''' % (inputjson['title'], inputjson['title'], inputjson['blurb'], imageshtml)

    indexHtmlRelPath = os.path.join(outputpath, 'index.html')
    logging.info("Creating file %s" % indexHtmlRelPath)
    with open(indexHtmlRelPath, 'w') as f:
        f.write(html)

def createMovieHtml(inputjson, outputpath):
    '''Create movie.html for posting.

    Assumes movie name is the same as the outputpath basename, e.g. if outputpath
    is "out/2020/may" then the movie name will be may.mp4/webm.

    :param inputjson: input a.json
    :type inputjson: dict
    :param outputpath: path to output files
    :type outputpath: str
    :return None
    '''
    movieName = os.path.basename(outputpath)
    logging.debug(f'movie name is "{movieName}"')
    title = inputjson['title']
    html = f"""
<html>
<head>
<title>{title}</title>
</head>
<body>
<video controls>
  <source src="{movieName}.webm" type="video/webm">
  <source src="{movieName}.mp4" type="video/mp4">
  I'm sorry; your browser doesn't support HTML5 video in WebM with VP8 or MP4 with H.264.
</video>
</body>
</html>
"""

    with open(os.path.join(outputpath, "movie.html"), 'w') as f:
        f.write(html)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Create part of mattandcress.com.')
    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        help='verbose')
    parser.add_argument('--inputpath', metavar='input/path', dest='inputpath',
                        help='Path to input folder containing a.json.')
    parser.add_argument('--outputpath', metavar='output/path', dest='outputpath',
                        help='Path to output index.html and images.')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    os.makedirs(args.outputpath, exist_ok=True)

    with open(os.path.join(args.inputpath, 'a.json'), 'r') as f:
        inputjson = json.JSONDecoder().decode(f.read())

    imageshtml = createImagesAndImageHtml(args.inputpath, inputjson, args.outputpath)
    doFolderIndex(inputjson, imageshtml, args.outputpath)
    createMovieHtml(inputjson, args.outputpath)
