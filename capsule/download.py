import os
import six
import shutil
import wget
import traceback
import zipfile

def trim_repo_url(url):
    """Replace the .git in url"""
    return url.replace(".git", "")

def get_archive_url(url, branch=None):
    """
      get the archive url and filename
      Args:
        url: git repo url
        branch: name of the branch to be dowloaded
      Returns:
        tuple representing filename and archiveurl
    """
    git_url = trim_repo_url(url)
    fragment = None
    file = git_url.split("/")[-1]
    if not branch:
        fragment = "/archive/master.zip"
    else:
        fragment = "/archive/{}.zip".format(branch)
    return file, git_url+fragment

def _download(url, outpath=None, dirname=None, branch=None):
    """download the zip files in output directory with dirname
       
       Args:
         url: url to be downloaded
         outpath: path of the output folder
         dirname: name of the directory
       
       Returns:
         file name
    """

    outfolder = outpath or os.getcwd()
    file, archive_url = get_archive_url(url)
    if dirname:
        outfolder = "{}/{}.zip".format(outfolder, dirname)
    return file, wget.download(archive_url, out=outfolder)

def _unzip(filename, branch=None):
    """unzip the archive file"""
    try:
        file = zipfile.ZipFile(filename)
        basename = os.path.dirname(filename)
        basename = basename.replace(".zip", "")
        file.extractall(path=basename)
        return basename, filename
    except Exception as e:
        six.print_(e)

def _delete(filename):
    """deletes the archive file"""
    return os.remove(filename)


def rupture(url, outpath=None, branch='master', dirname=None):
    """
      Downloads the archive, unzips it and deletes the archive
      file

      Args:
         url: url to be downloaded
         outpath: path of the output folder
         dirname: name of the directory
         branch: branch to be downloaded

      Returns:
        None
    """
    try:
        file, filename = _download(url, outpath=outpath, dirname=dirname, branch=branch)
        base, cs= _unzip(filename)
        _delete(filename)
        to_find = "{}/{}-{}".format(base, file, branch)
        _newname = dirname or file
        shutil.move(to_find, base+"/"+_newname)
    except Exception as e:
        six.print_(traceback.format_exc())
        six.print_("Cannot download the repo. Could you check the repo url ?")