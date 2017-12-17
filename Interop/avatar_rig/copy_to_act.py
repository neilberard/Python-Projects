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
prefab_file = ".prefab"
meta_file = ".meta"


def perform_p4_command(*args):
    print args
    command = pm.textField('Command', query=True, text=True)
    fstat = FStat()
    message = fstat.perform_perforce_command(command)
    pm.text("Command", edit=True, label=message)


def create_window():
    window_name = 'PerforceDialog'
    if pm.window(window_name, exists=True):
        pm.deleteUI(window_name)
    window = pm.window(window_name, t=window_name, widthHeight=(400, 100))
    pm.columnLayout(adjustableColumn=True)
    pm.text("Command")
    pm.textField("Command")
    pm.button("Enter P4 Command", command=perform_p4_command)
    pm.setParent('..')
    pm.showWindow(window)


class GetFilePaths(object):

    path = []

    def reset_path(self):
        self.path = pm.system.sceneName()

    def get_short_path(self):
        short_path = self.path.split('/')[-1:]
        return short_path[0]

    def set_alternate_path(self, new_path):
        self.path = new_path

    def set_windows_path(self):
        scene_name = self.get_short_path()
        print scene_name, 'SCENE NAME'
        win_path = str(self.path).replace(str(scene_name), '')
        return win_path.replace('/', '\\')

    def get_source(self):

        if self.path is None:
            print "Path is NONE"
            return None
        out_paths = []

        if self.path.find(shared) != -1:
            print "Shared File Found", self.path
            out_paths.append(self.path.replace(maya_file, fbx_file))
            return out_paths

        if self.path.find(female + maya_file) != -1:
            out_paths.append(self.path.replace(maya_file, fbx_file))

        if self.path.find(male + maya_file) != -1:
            out_paths.append(self.path.replace(maya_file, fbx_file))

        if self.path.find(gendered + maya_file) != -1:
            out_paths.append(self.path.replace(gendered + maya_file, female + fbx_file))
            out_paths.append(self.path.replace(gendered + maya_file, male + fbx_file))
            out_paths.append(self.find_substance())
            return out_paths

    def get_act_paths(self):
        if self.get_source() is None:
            return None

        source_paths = self.get_source()
        source_paths.append(self.path.replace(gendered + maya_file, female + prefab_file))
        source_paths.append(self.path.replace(gendered + maya_file, female + prefab_file + meta_file))
        source_paths.append(self.path.replace(gendered + maya_file, male + prefab_file))
        source_paths.append(self.path.replace(gendered + maya_file, male + prefab_file + meta_file))

        dest_paths = []
        for i in source_paths:
            if i is not None:
                dest_paths.append(i.replace(norm_p4_path, norm_p4_path + act_path))

        return dest_paths

    def find_substance(self):
        txt_src = self.path.replace(models_path, textures_path)
        a = txt_src.replace(maya_file, substance_file)
        substance_path = a.replace(gendered, "")
        if os.path.isfile(substance_path):
            return substance_path
        else:
            # print "substance file not found:", substance_path
            return None


class FStat(GetFilePaths):
    """This class gathers file information from Perforce"""

    def perform_perforce_command(self, command):
        sub = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                               shell=True)
        stdout, stderr = sub.communicate()
        if len(stderr) > 0:
            return stderr
        return stdout

    def get_fstat(self):
        command = "p4 fstat " + str(self.path)
        raw_stat = self.perform_perforce_command(command)
        my_fstat = raw_stat.split('...')
        return my_fstat

    def is_checked_out(self):
        check_out_message = self.get_fstat()
        for i in check_out_message:
            if i.find("action edit") != -1:
                return True
        return False

    def is_logged_into_perforce(self):
        message = self.get_fstat()
        for i in message:
            if i.find("please login") != -1:
                pm.confirmDialog(message="Not logged into Perforce")
                return None
        return True

    def is_in_perforce(self):
        message = self.get_fstat()

        for i in message:
            if i.find("wrong number of arguments") != -1:
                print 'found'
                return None

        return True

    def is_latest_revision(self):
        message = self.get_fstat()

        head_value = 0
        have_value = 0

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
    def enter_p4_command(self, text_command):
        return self.perform_perforce_command(text_command)

    def revert_file(self):
        if self.is_checked_out():
            command = "p4 revert " + str(self.path)
            self.perform_perforce_command(command)
            print 'REVERTED'

    def check_out_file(self, **kwargs):
        if self.is_in_perforce() is None:
            pm.confirmDialog(message="File not in Perforce: " + str(self.path))
            return None

        if not self.is_latest_revision():
            if pm.confirmDialog(message='File not up to date, would you like to get latest revision and reopen',
                                button=['Yes', 'No']) == 'Yes':
                print "getting latest"
                self.get_latest()
                pm.openFile(self.path, force=True)
            else:
                print "checking out older version"

        if self.is_checked_out():
            message = "FILE is checked out: " + str(self.path)
            if kwargs.get('dialog'):
                pm.confirmDialog(message=message)
            return None
        command = "p4 edit -c default " + str(self.path)

        if pm.confirmDialog(message='Would you like to check out the file: ' + str(self.path),
                            button=['Yes', 'No']) == 'Yes':
            print 'PERFORMING CHECKOUT'
            print self.perform_perforce_command(command)


        return

    def get_latest(self):
        if self.is_latest_revision():
            print 'Already have latest'
            return

        command = "p4 sync --parallel=0 " + str(self.path) + "#head"
        sub = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        if len(sub.stdout.read()) == 0:
            print "Have latest"
        return


class FileFuncs(P4Funcs):

    def check_out_source_files(self):
        self.reset_path()

        if not self.is_logged_into_perforce():
            return None
        self.check_out_file()
        source_files = self.get_source()
        print source_files, 'get source'

        if len(source_files) == 0:
            print "No source file could be found"
            return None

        for i in source_files:
            print i, " SOURCE PATH"
            if i is None:
                return None
            if os.path.isfile(i):
                # set the file path to check
                self.set_alternate_path(i)
                self.check_out_file()

    def check_out_act_files(self):
        self.reset_path()

        if not self.is_logged_into_perforce():
            return

        for i in self.get_act_paths():
            print i, "ACT PATH"

            if os.path.isfile(i) and self.is_in_perforce():
                self.set_alternate_path(i)
                self.check_out_file()

        self.reset_path()
                    # print self.path

    def copy_to_act(self):
        self.reset_path()

        if len(self.get_source()) == 0:
            print 'could not find files'
            return

        for i in self.get_source():
            print i

            source = ''
            dest = ''
            if i is not None:
                source = i
                dest = i.replace(norm_p4_path, norm_p4_path + act_path)
                dialog = str(source) + "<<< COPY TO DESTINATION >>>>" + str(dest) + '  PROCEED?'
                if pm.confirmDialog(message=dialog, button=['Yes', 'No']) == 'No':
                    return
                pm.system.sysFile(source, copy=dest)

    def open_current_folder(self):
        self.reset_path()
        win_path = self.set_windows_path()
        cmd = 'start %windir%\explorer.exe ' + win_path
        print cmd, "Command"

        self.perform_perforce_command(cmd)

    def open_act_folder(self):
        self.reset_path()
        self.set_alternate_path(self.get_act_paths()[0])
        win_path = self.set_windows_path()
        cmd = 'start %windir%\explorer.exe ' + win_path
        print cmd, "Command"
        self.perform_perforce_command(cmd)


