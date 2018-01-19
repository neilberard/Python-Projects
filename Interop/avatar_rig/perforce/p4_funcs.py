import pymel.core as pymel
import os
import subprocess
import logging
import re

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)




models_path = "Models"
textures_path = "Textures"
substance_file = ".sbsar"

female = "_F"
male = "_M"
shared = "_S"
gendered = "_G"
maya_file = ".ma"
fbx_file = ".fbx"


class FilePaths(object):

    def __init__(self):

        self._avatars_depot_path = '/'.join(os.environ['AVATARS_V3_PERFORCE_DEPOT'].split('\\'))
        self._ACT_path = "/ACT/Assets/SubmissionContent"
        self._file_path = []

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, str_path):
        self._file_path = str_path

    @property
    def ACT_path(self):
        return self._ACT_path

    @ACT_path.setter
    def ACT_path(self, str_path):
        self._ACT_path = str_path

    @property
    def avatars_depot_path(self):
        return self._avatars_depot_path

    @avatars_depot_path.setter
    def avatars_depot_path(self, str_path):
        self._avatars_depot_path = str_path

    def get_source(self):
        out_paths = []
        if self._file_path.find(gendered + maya_file):
            out_paths.append(self._file_path.replace(gendered + maya_file, female + fbx_file))
            out_paths.append(self._file_path.replace(gendered + maya_file, male + fbx_file))
            out_paths.append(self.find_substance())
            return out_paths
        if self._file_path.find(shared + maya_file):
            return self._file_path.replace(maya_file, fbx_file)

    def find_substance(self):
        txt_src = self._file_path.replace(models_path, textures_path)
        a = txt_src.replace(maya_file, substance_file)
        substance_path = a.replace(gendered, "")
        if os.path.isfile(substance_path):
            return substance_path
        else:
            print "substance file not found:", substance_path
            return None


class FStat(FilePaths):
    """
    Issues P4 Commands via subprocess and Returns OutPut
    """

    def perform_perforce_command(self, command):
        sub = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        return sub.communicate()

    def get_fstat(self):
        command = "p4 fstat " + str(self._file_path)
        return self.perform_perforce_command(command)


    def is_checked_out(self):
        message = self.get_fstat()
        for i in message:
            if i.find("action edit") != -1:
                print "file is CHECKED OUT"
                return True

        print "file is NOT CHECKED OUT"
        return False

    def is_latest_revision(self):

        message = self.get_fstat()

        if len(message) == 0:
            print "file not in Perforce"
            return None

        for i in message:
            if i.find('headRev') == 1:
                head_value = int(i.split(' ')[2])

        for i in message:
            if i.find('haveRev') == 1:
                have_value = int(i.split(' ')[2])

        if head_value == have_value:
            print '>>>File is up to date: REVISION#', have_value
            return True
        else:
            print '>>>File is NOT to up date, please get latest Revision#', head_value
            return False


class P4Funcs(FStat):
    def __init__(self):
        super(P4Funcs, self).__init__()

    def get_info(self):
        command = 'p4 info'

        # p4 info returns a multi-line str, parsing this str into a dict. Example key['User name'] : value['name']
        environment_info = {}
        file_info = str(self.perform_perforce_command(command)[0]).splitlines()

        for str_line in file_info:
            info = str_line.split(': ')
            environment_info[info[0]] = info[1]
        return environment_info

    def get_workspaces(self, user):
        command = 'p4 workspaces -u {}'.format(user)

        # parsing output
        p4_output = self.perform_perforce_command(command)
        p4_output_split = str(p4_output[0]).split(' ')

        # gathering workspaces
        workspaces = []
        for num, obj in enumerate(p4_output_split):

            if obj.find('Client') != -1:
                workspaces.append(p4_output_split[num + 1])

        return workspaces

    def set_client(self, client):
        command = 'p4 set P4CLIENT={}'.format(client)
        return self.perform_perforce_command(command)

    def revert_file(self):
        if self.is_checked_out():
            print 'ready'
            command = "p4 revert " + str(self._file_path)
            self.perform_perforce_command(command)
            log.info('REVERTED')

    def check_out_file(self):
        if self.is_checked_out():
            return
        command = "p4 edit -c default " + str(self._file_path)
        print command
        self.perform_perforce_command(command)

        print self._file_path, "CHECKED OUT"

    def get_latest(self):
        if self.is_latest_revision():
            print 'Already have latest'
            return

        command = "p4 sync --parallel=0 " + str(self._file_path) + "#head"
        sub = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        if len(sub.stdout.read()) == 0:
            print "Have latest"
        return


class FileFuncs(FilePaths):
    def __init__(self):
        super(FileFuncs, self).__init__()

    def copy_to_act(self):
        if len(self.get_source()) == 0:
            print 'could not find files'
            return

        for i in self.get_source():
            if os.path.isfile(i):
                source = i
                dest = i.replace(self._avatars_depot_path, self._avatars_depot_path + self._ACT_path)
            print source, " copy to ", dest
            if os.path.isfile(dest):
                print "dest path is good"

            pymel.system.sysFile(source, copy=dest)


p4_file = P4Funcs()


if __name__ == '__main__':
    p4_file.file_path = (''.join([p4_file.avatars_depot_path, '/items/Skinnable/Top/Models/MilitaryJacket_G.ma']))
    fstat = p4_file.get_fstat()
#
#
env = p4_file.get_info()

print env

#
# workspaces = p4_file.get_workspaces(env['User name'])
#
#
# print workspaces
#
#
