import os
import subprocess


def file_safe_date(the_date):
    ret = str(the_date).replace(':', '_').replace(' ', 'T')
    return ret


def get_percentage(partial, total, rounding=2):
    """
        @desc
            basic percentage calculator
        @param
            partial  : int() or float() 25
            total    : int() or float()  100
            rounding : int()
        @return
            float()
    """
    return round(float(partial * 100) / total, rounding)


def uncompress_file(infile, outfile=None, password=None, remove_original=True):
    """
        @desc: Method to uncompress any file you may have. Currently supports .gz, .tar, .zip

        @param:
            infile: str() file path of file to be compressed
            outfile: str() file where to store the uncompressed result. defaults to same dir of infile
            password str() password for decrypting archive
            remove_original Bool Remove the original archive, leaving only the compressed result.

        @return
            False if error
            or
            str() unzipped file or directory
    """
    if not outfile:
        outfile = os.path.dirname(infile)
    if infile[-3:] == '.gz':
        try:
            subprocess.check_call('gunzip -f %s' % infile, shell=True)
        except Exception, e:
            print 'Cannot Uncompress %s, %s' % (infile, e)
            return False
        infile = infile.replace('.gz', '')
    elif infile[-4:] == '.tar':
        try:
            subprocess.check_call('tar -xvf %s' % infile, shell=True)
        except Exception, e:
            print 'Cannot Uncompress %s, %s' % (infile, e)
            return False
        infile = infile.replace('.tar', '')
    elif infile[-4:] == '.zip':
        try:

            subprocess.check_call('unzip -d %s  %s' % (outfile, infile), shell=True)
        except Exception, e:
            print 'Cannot Uncompress %s, %s' % (infile, e)
            return False
        infile = infile.replace('.zip', '')
    else:
        print "ERROR: Unknown or no compression"
        return infile
    if outfile:
        return outfile
