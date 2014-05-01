#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from xclip import Xclip
import base64

clip = Xclip()





#=============== COMMAND LINE PARSER =======================#

def cliparser():
    import argparse
    import sys

    desc = "Convert image to base64"
    parser = argparse.ArgumentParser(prog=sys.argv[0], description=desc)

    parser.add_argument("--input-clipboard","-c", action="store_true",  help="Read file from clipboard [ default]")
    parser.add_argument("--input-stdin","-i", action="store_true",  help="Read file from stdin")
    parser.add_argument("--input-file", "-f", help="<filename> Read file and return output in clipboard.")
    parser.add_argument("--input-url", "-u", action="store_true", help="<filename> Read image from url and output in clipboard.")
    parser.add_argument("--decode-image", "-d", action="store_true", help="Decode base64 image from clipboard")
    parser.add_argument("--out", action="store_true", help="Show output in terminal")
    parser.add_argument("--html", action="store_true", help="Output in html format")


    args = parser.parse_args()

    if args.input_stdin:
        data = sys.stdin.read()
        data = base64.b64encode(data)
        print "Wrote to clipboard \n", data
        clip.write(data)
        sys.exit(0)

    elif args.input_file:
        f = args.input_file
        fp = open(f, 'rb')
        data = f.read()
        data = base64.b64encode(data)
        print "Wrote to clipboard ", f
        clip.write(data)

        sys.exit(0)

    elif args.input_url:

        import tempfile
        import urllib

        url = clip.read()

        with  tempfile.NamedTemporaryFile(suffix="", delete=True) as temp:
            tname = temp.name
            print url
            print tname

            #import IPython ;  IPython.empython bed()

            os.system("wget " + url + " -o " + tname)

            fp = open(tname, "rb")
            data  = fp.read()
            data = base64.b64encode(data)
            fp.close()

            clip.write(data)

        sys.exit(0)

    elif args.decode_image:

        print "-------decode-image--------"

        imagedata = clip.readf()
        fname = clip.read()

        import tempfile



        with  tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
            img = temp.name
            print img
            fp = open(img, "wb")
            fp.write(base64.b64decode(imagedata))
            fp.close()
            os.system("xdg-open " + img)
            raw_input(">> Type Return to exit.")
            os.remove(img)

    else:
        # Read file from clipboard
        img = clip.readf()
        fname = clip.read()

        ext = fname.split('.')[1] # Get file type

        data = base64.b64encode(img)
        print "Wrote to clipboard ", clip.read()

        encoded = "data:image/%s;base64,%s" % (ext, data)

        if args.html:
            encoded = '<img src="%s"/>' % encoded


        clip.write(encoded)




def main():

    cliparser()

if __name__ == '__main__':
    main()


