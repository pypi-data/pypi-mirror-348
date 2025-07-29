import os
import re
from kabaret import flow
from kabaret.flow.object import _Manager
from kabaret.flow_contextual_dict import get_contextual_dict
from libreflow.utils.os import remove_folder_content
from libreflow.baseflow.file import GenericRunAction, TrackedFile, TrackedFolder, MarkImageSequence
from libreflow.baseflow.runners import FILE_EXTENSION_ICONS


class RevisionNameChoiceValue(flow.values.SessionValue):

    DEFAULT_EDITOR = 'choice'
    STRICT_CHOICES = False

    _file = flow.Parent(2)

    def __init__(self, parent, name):
        super(RevisionNameChoiceValue, self).__init__(parent, name)
        self._revision_names = None

    def choices(self):
        if self._revision_names is None:
            self._revision_names = self._file.get_revision_names(sync_status='Available', published_only=True)
        
        return self._revision_names
    
    def revert_to_default(self):
        names = self.choices()
        if names:
            self.set(names[-1])
    
    def touch(self):
        self._revision_names = None
        super(RevisionNameChoiceValue, self).touch()


class ExportFormatChoiceValue(flow.values.ChoiceValue):

    CHOICES = ('png', 'psd')


class ExportKrita(GenericRunAction):
    MANAGER_TYPE = _Manager
    ICON = ('icons.gui', 'picture')

    revision = flow.SessionParam(None, RevisionNameChoiceValue)
    export_format = flow.Param('png', ExportFormatChoiceValue).ui(label='Format', choice_icons=FILE_EXTENSION_ICONS)

    _file = flow.Parent()
    _files = flow.Parent(2)
    _task = flow.Parent(3)

    def runner_name_and_tags(self):
        return 'Krita', []
    
    def get_version(self, button):
        return None
    
    def get_run_label(self):
        return 'Krita - Export image'
    
    def allow_context(self, context):
        return (
            context
            and self._file.format.get() == 'kra'
            and self.revision.choices()
        )
    
    def needs_dialog(self):
        self.message.set('<h2>Export image</h2>')
        self.revision.touch()
        self.revision.revert_to_default()
        return True
    
    def get_buttons(self):
        return ['Export', 'Cancel']
    
    def extra_argv(self):
        argv = super(ExportKrita, self).extra_argv()
        
        basename = self._file.name()[:-(len(self._file.format.get()) + 1)]
        scene_path = self._file.get_revision(self.revision.get()).get_path().replace('\\', '/')
        export_path = self._ensure_revision(f'{basename}_export.{self.export_format.get()}', self.revision.get())
        argv += [
            f'{scene_path}',
            '--export',
            '--export-filename',
            f'{export_path}',
        ]
        
        return argv
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        return super(ExportKrita, self).run(button)
    
    def _ensure_revision(self, file_name, revision_name):
        '''
        Returns the path of the revision `revision_name` in
        the `file_name` file history.
        It creates the revision in the project and in the current
        site's file system if it does not exist yet.
        '''
        name, ext = file_name.split('.')
        file_mapped_name = file_name.replace('.', '_')

        default_files = self.root().project().get_task_manager().get_task_files(self._task.name())
        default_file = default_files.get(file_mapped_name)
        
        if not self._files.has_mapped_name(file_mapped_name):
            _file = self._files.add_file(name, ext, tracked=True, default_path_format=(default_file[1] if default_file else None))
        else:
            _file = self._files[file_mapped_name]
        
        _file.file_type.set('Outputs')
        source_revision = self._file.get_revision(self.revision.get())
        revision = _file.get_revision(revision_name)
        
        if revision is None:
            revision = _file.add_revision(revision_name)
        
        revision.comment.set(source_revision.comment.get())
        path = revision.get_path().replace('\\', '/')
        os.makedirs(os.path.dirname(path), exist_ok=True)

        return path


class ImageExportFormat(flow.values.SessionValue):

    DEFAULT_EDITOR = 'choice'

    def choices(self):
        return [
            'jpg', 'png', 'tif'
        ]


class KritaRenderImageSequence(GenericRunAction):

    ICON = ('icons.libreflow', 'krita')

    revision = flow.SessionParam(None, RevisionNameChoiceValue)

    with flow.group('Advanced settings'):
        export_format = flow.SessionParam('png', ImageExportFormat)

    _file = flow.Parent()
    _files = flow.Parent(2)
    _task = flow.Parent(3)

    def runner_name_and_tags(self):
        return 'Krita', []
    
    def get_version(self, button):
        return None
    
    def get_run_label(self):
        return 'Render image sequence'
    
    def allow_context(self, context):
        return False
    
    def needs_dialog(self):
        self.message.set('<h2>Render image sequence</h2>')
        self.revision.touch()
        self.revision.revert_to_default()
        return True
    
    def get_buttons(self):
        return ['Render', 'Cancel']
    
    def extra_argv(self):
        argv = super(KritaRenderImageSequence, self).extra_argv()
        
        basename = self._file.name()[:-(len(self._file.format.get()) + 1)]
        scene_path = self._file.get_revision(self.revision.get()).get_path().replace('\\', '/')
        export_path = self._ensure_render_folder(f'{basename}_render', self.revision.get())

        # Prefix
        settings = get_contextual_dict(self._file, 'settings')
        prefix = f"{settings.get('sequence')}_{settings.get('shot')}."
        
        argv += [
            f'{scene_path}',
            '--export-sequence',
            '--export-filename',
            f'{export_path}/{prefix}.{self.export_format.get()}',
        ]
        
        return argv
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        return super(KritaRenderImageSequence, self).run(button)
    
    def _ensure_render_folder(self, folder_name, revision_name):
        '''
        Returns the path of the revision `revision_name` in
        the `folder_name` folder history.
        It creates the revision in the project and in the current
        site's file system if it does not exist yet.
        '''
        default_files = self.root().project().get_task_manager().get_task_files(self._task.name())
        default_file = default_files.get(folder_name)
        
        if not self._files.has_mapped_name(folder_name):
            folder = self._files.add_folder(folder_name, tracked=True, default_path_format=(default_file[1] if default_file else None))
        else:
            folder = self._files[folder_name]
        
        folder.file_type.set('Outputs')
        
        source_revision = self._file.get_revision(self.revision.get())
        revision = folder.get_revision(revision_name)
        
        if revision is None:
            revision = folder.add_revision(revision_name)
        
        revision.comment.set(source_revision.comment.get())
        path = revision.get_path().replace('\\', '/')

        if os.path.isdir(path):
            remove_folder_content(path)
        else:
            os.makedirs(path)

        return path


class KritaRenderPlayblast(flow.Action):

    MANAGER_TYPE = _Manager
    ICON = ('icons.libreflow', 'krita')

    revision = flow.SessionParam(None, RevisionNameChoiceValue)

    _file = flow.Parent()
    _shot = flow.Parent(5)

    def allow_context(self, context):
        return (
            context
            and self._file.format.get() == 'kra'
            and self.revision.choices()
        )
    
    def needs_dialog(self):
        self.message.set('<h2>Render playblast</h2>')
        self.revision.touch()
        self.revision.revert_to_default()
        return True
    
    def get_buttons(self):
        return ['Render', 'Cancel']

    def get_audio_path(self):
        mng = self.root().project().get_task_manager()
        default_files = mng.default_files.get()
        for file_name, task_names in default_files.items():
            if 'animatic.wav' in file_name:
                task = default_files[file_name][0]
                file_mapped_name = file_name.replace(".", '_')
                break

        if not self._shot.tasks.has_mapped_name(task):
            return None
        self.animatic_task = self._shot.tasks[task]

        name, ext = file_mapped_name.split('_')
        
        if not self.animatic_task.files.has_file(name, ext):
            return None
        f = self.animatic_task.files[file_mapped_name]
        rev = f.get_head_revision()
        rev_path = rev.get_path()

        return rev_path
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        revision_name = self.revision.get()
        
        # Render image sequence
        ret = self._render_image_sequence(revision_name)
        render_runner = self.root().session().cmds.SubprocessManager.get_runner_info(
            ret['runner_id']
        )
        # Configure image sequence marking
        folder_name = self._file.name()[:-len(self._file.format.get())]
        folder_name += 'render'
        self._mark_image_sequence(
            folder_name,
            revision_name,
            render_runner['pid']
        )
    
    def _render_image_sequence(self, revision_name):
        render_action = self._file.render_image_sequence_krita
        render_action.revision.set(revision_name)
        ret = render_action.run('Render')

        return ret
    
    def _mark_image_sequence(self, folder_name, revision_name, render_pid):
        mark_sequence_wait = self._file.mark_image_sequence_wait
        mark_sequence_wait.folder_name.set(folder_name)
        mark_sequence_wait.revision_name.set(revision_name)
        mark_sequence_wait.wait_pid(render_pid)
        mark_sequence_wait.run(None)


class MarkImageSeqKrita(MarkImageSequence):
    
    def _get_audio_path(self):
        scene_name = re.search(r"(.+?(?=_render))", self._folder.name()).group()
        scene_name += '_kra'
            
        if not self._files.has_mapped_name(scene_name):
            print('[GET_AUDIO_PATH] Scene not found')
            return None
            
        return self._files[scene_name].render_playblast_krita.get_audio_path()

    def mark_sequence(self, revision_name):
        # Compute playblast prefix
        prefix = self._folder.name()
        if 'preview' in prefix:
            prefix = prefix.replace('_render_preview', '')
        else:
            prefix = prefix.replace('_render', '')
        
        source_revision = self._file.get_revision(revision_name)
        revision = self._ensure_file_revision(
            f'{prefix}_movie_preview' if 'preview' in self._folder.name() else f'{prefix}_movie', revision_name
        )
        revision.comment.set(source_revision.comment.get())
        
        # Get the path of the first image in folder
        img_path = self._get_first_image_path(revision_name)
        
        file_name = prefix + '.kra'
        
        self._extra_argv = {
            'image_path': img_path,
            'video_output': revision.get_path(),
            'file_name': file_name
        }

        audio_path = self._get_audio_path()
        if audio_path:
            self._extra_argv['audio_file'] = audio_path
        
        return super(MarkImageSequence, self).run('Render')


def render_playblast_krita(parent):
    if isinstance(parent, TrackedFile):
        render_img_sequence = flow.Child(KritaRenderImageSequence)
        render_img_sequence.name = 'render_image_sequence_krita'
        render_img_sequence.index = 49

        render_playblast = flow.Child(KritaRenderPlayblast).ui(label='Render playblast')
        render_playblast.name = 'render_playblast_krita'
        render_playblast.index = 50
        
        return [render_img_sequence, render_playblast]


def mark_sequence_krita(parent):
    if isinstance(parent, TrackedFolder) and any(
        file_name.endswith("_kra") is True for file_name in parent._map.mapped_names()
    ):
        r = flow.Child(MarkImageSeqKrita)
        r.name = 'mark_image_sequence'
        r.index = None
        return r


def export_png_krita(parent):
    if isinstance(parent, TrackedFile):
        r = flow.Child(ExportKrita).ui(label='Export image')
        r.name = 'export_krita'
        r.index = 51
        return r


def install_extensions(session):
    return {
        "rendering_krita": [
            render_playblast_krita,
            export_png_krita,
            mark_sequence_krita,
        ]
    }
