import subprocess

from politeauthority import environmental


def send(color, msg):
    cmd = """curl -X POST -H 'Content-type: application/json' --data '{"text":"%s"}' """
    cmd += environmental.slack_url()
    cmd = cmd % msg
    try:
        subprocess.call(cmd, shell=True)
        return True
    except Exception, e:
        print 'Error: %s' % e
        return False

# End File politeauthority/politeauthority/slacky.py
