import optparse
import requests

###
# This script takes in a target image that the user wants to download and a list
# of kodi servers (in the format of 192.168.1.40:8080,192.168.1.41). The script
# will then send an HTTP request that proxies through the kodi servers like so:
#
# user <-> 192.168.1.40 <-> 192.168.1.41 <-> image server
#
# In that way, the user never exposes themselves to image server.
##
def encode_all(string_to_encode):
    encoded = ''
    for c in string_to_encode:
        encoded += '%'
        encoded += c.encode("hex")
    return encoded

def create_url(target, host):
    encoded_target = encode_all(target)
    encoded_target = encode_all("image/image://" + encoded_target)
    return "http://" + host + '/' + encoded_target

if __name__=="__main__":
    parser = optparse.OptionParser("usage: %prog -k [kodi host] -t [target]")
    parser.add_option("-k", "--kodi-hosts", dest="hosts", type="string", help="A comma seperated list of Kodi hosts")
    parser.add_option("-t", "--target", dest="target", type="string", help="The target image to download")
    parser.add_option("-o", "--output", dest="output", type="string", help="Name of output file")

    (options, args) = parser.parse_args()

    if options.hosts == None or options.target == None:
        print '[-] Host and target must be provided. For example: '
        print '\tpython kodi_img_request.py -t http://attrition.org/images/squirrel-mascot-iconL.gif -k 192.168.1.40:8080'
        exit(0)

    request = options.target
    for host in options.hosts.split(','):
        request = create_url(request, host)

    print "[+] Sending HTTP GET for " + request
    image_request = requests.get(request)
    if image_request.status_code != 200:
        print "[-] Bad status code: " + str(image_request.status_code)
        exit(0)
    print "[+] 200 received!"

    if options.output != None:
        with open(options.output, "wb") as output:
            print "[+] Writing response to " + options.output
            output.write(image_request.content)

    print "[+] Done"