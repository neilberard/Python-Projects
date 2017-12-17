import pymel.core as pm
import os
import subprocess


p4_path = pm.util.getEnv('AVATARS_V3_PERFORCE_DEPOT')
norm_p4_path = '/'.join(p4_path.split('\\'))
act_path = "/ACT/Assets/SubmissionContent"

models_path = "Models"
textures_path = "Textures"
substance_file = ".sbsar"

female = "_F"
male = "_M"
shared = "_S"
gendered = "_G"
maya_file = ".ma"
fbx_file = ".fbx"


class GetFilePaths(object):

    path = pm.system.sceneName()

    def get_source(self):
        out_paths = []
        if self.path.find(gendered + maya_file):
            out_paths.append(self.path.replace(gendered + maya_file, female + fbx_file))
            out_paths.append(self.path.replace(gendered + maya_file, male + fbx_file))
            out_paths.append(self.find_substance())
            return out_paths
        if self.path.find(shared + maya_file):
            return self.path.replace(maya_file, fbx_file)

    def find_substance(self):
        txt_src = self.path.replace(models_path, textures_path)
        a = txt_src.replace(maya_file, substance_file)
        substance_path = a.replace(gendered, "")
        if os.path.isfile(substance_path):
            return substance_path
        else:
            print "substance file not found:", substance_path
            return None


class FStat(GetFilePaths):

    def perform_perforce_command(self, command):
        sub = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        return sub.read()


    def fstat(self):
        command = "p4 fstat " + str(self.path)
        return self.perform_perforce_command(command)

    def get_fstat(self):
        my_fstat = self.fstat().split('...')
        print my_fstat
        return my_fstat

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

    def revert_file(self):
        if self.is_checked_out():
            print 'ready'
            command = "p4 revert " + str(self.path)
            self.perform_perforce_command(command)
            print 'REVERTED'

    def check_out_file(self):
        if self.is_checked_out():
            return
        command = "p4 edit -c default " + str(self.path)
        print command
        self.perform_perforce_command(command)

        print self.path, "CHECKED OUT"

    def get_latest(self):
        if self.is_latest_revision():
            print 'Already have latest'
            return

        command = "p4 sync --parallel=0 " + str(self.path) + "#head"
        sub = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        if len(sub.stdout.read()) == 0:
            print "Have latest"
        return


class FileFuncs(GetFilePaths):

    def copy_to_act(self):
        if len(self.get_source()) == 0:
            print 'could not find files'
            return

        for i in self.get_source():
            if os.path.isfile(i):
                source = i
                dest = i.replace(norm_p4_path, norm_p4_path + act_path)
            print source, " copy to ", dest
            if os.path.isfile(dest):
                print "dest path is good"

            pm.system.sysFile(source, copy=dest)








