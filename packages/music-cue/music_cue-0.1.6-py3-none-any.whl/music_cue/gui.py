import os
import queue
import tkinter
import inspect
from tkinter.filedialog import askopenfilename

import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox

from openpyxl.utils.exceptions import InvalidFileException

from music_cue.base_logger import logger
from music_cue.data_handler import DataHandler, SheetExistsException
from music_cue.utils import PropagateExceptionThread


class MusicCueGui(ttk.Frame):
    """
    Provides GUI for the Music Cue APP using two tabs
    """
    def __init__(self, master, **kwargs):        
        super().__init__(master, padding=10, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        label = ttk.Label(self, text="Hello, this is the MusicCue App!")
        label.pack()
        
        self.widgets = {}

        self.data_handler = DataHandler()

        self.my_notebook = ttk.Notebook(self, width=1400, height=750)
        self.my_notebook.pack()
        self.my_notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

        self.create_general_tab()
        self.create_episode_tab()

    def on_tab_change(self, event: tkinter.Event) -> None:
        """
        Populates list of Episode names for 'Episode' combobox when tab button is pressed.
        """

        tab = event.widget.tab('current')['text']
        if tab == 'Episode':
            try:
                self.widgets['episode_cb']['values'] = self.data_handler.get_episode_names()
            except TypeError:
                Messagebox.show_warning('Warning: First select Excel file', alert=True)

    def create_general_tab(self) -> None:
        """
        Create frames within this tab. The main purpose of this tab is to provide
        general functionalities.
        """

        tab = ttk.Frame(self.my_notebook)
        self.my_notebook.add(tab, text='General')

        # Label frame
        self.widgets['excel_select_lf_header'] = self.create_label_frame_header(tab, frame_text='File select')
        browse_btn = ttk.Button(
            master=self.widgets['excel_select_lf_header'],
            text="Browse",
            command=self.select_excel_file,
            width=10,
        )
        browse_btn.pack(side=LEFT, padx=5)
        hdr_txt = 'Please select Excel file'
        hdr = ttk.Label(master=self.widgets['excel_select_lf_header'], text=hdr_txt, width=50)
        hdr.pack(side=LEFT, pady=5, padx=10)

        # Label frame
        lf_header = self.create_label_frame_header(tab, frame_text='Additional sheets')
        create_sheets_btn = ttk.Button(
            master=lf_header,
            text="Create",
            command=self.create_additional_sheets,
            width=10,
        )
        create_sheets_btn.pack(side=LEFT, padx=5)
        hdr_txt = 'Create additional sheets'
        hdr = ttk.Label(master=lf_header, text=hdr_txt, width=50)
        hdr.pack(side=LEFT, pady=5, padx=10)

        update_sheets_btn = ttk.Button(
            master=lf_header,
            text="Update",
            command=self.update_additional_sheets,
            width=10,
        )
        update_sheets_btn.pack(side=LEFT, padx=5)
        hdr_txt = 'Update additional sheets'
        hdr = ttk.Label(master=lf_header, text=hdr_txt, width=50)
        hdr.pack(side=LEFT, pady=5, padx=10)

        # Label frame
        lf_header = self.create_label_frame_header(tab, frame_text='Directory structure')
        dir_btn_create = ttk.Button(
            master=lf_header,
            text="Create or Update",
            command=self.create_or_update_directory_structure,
            width=20,
        )
        dir_btn_create.pack(side=LEFT, padx=5)
        hdr_txt = 'Create or Update directory structure'
        hdr = ttk.Label(master=lf_header, text=hdr_txt, width=50)
        hdr.pack(side=LEFT, pady=5, padx=10)

    def create_episode_tab(self) -> None:
        """
        This tab provides functionalities to update information and to split Episode music files.
        """

        tab = ttk.Frame(self.my_notebook)
        self.my_notebook.add(tab, text='Episode')

        # Label frame
        lf_header = self.create_label_frame_header(tab, frame_text='Select Episode')
        self.widgets['episode_cb'] = ttk.Combobox(
            master=lf_header,
            values=[],
            width=25,
        )
        self.widgets['episode_cb'].pack(side=LEFT, padx=5)
        hdr_txt = 'Please select the episode'
        hdr = ttk.Label(master=lf_header, text=hdr_txt, width=50)
        hdr.pack(side=LEFT, pady=5, padx=10)

        # Label frame
        lf_header = self.create_label_frame_header(tab, frame_text='Get Episode data')
        episode_data_btn = ttk.Button(
            master=lf_header,
            text="Get",
            command=self.get_episode_data,
            width=10,
        )
        episode_data_btn.pack(side=LEFT, padx=5)
        hdr_txt = 'Get episode data'
        hdr = ttk.Label(master=lf_header, text=hdr_txt, width=50)
        hdr.pack(side=LEFT, pady=5, padx=10)

        # Label frame
        lf_header = self.create_label_frame_header(tab, frame_text='Episode data')
        columns = [0, 1, 2, 3, 4, 5]
        self.widgets['episode_result_view'] = ttk.Treeview(
            master=lf_header,
            columns=columns,
            show=HEADINGS
        )
        self.widgets['episode_result_view'].pack(fill=BOTH, expand=YES, pady=10)

        # setup columns
        self.widgets['episode_result_view'].heading(0, text='Event', anchor=W)
        self.widgets['episode_result_view'].heading(1, text='Clip name', anchor=W)
        self.widgets['episode_result_view'].heading(2, text='Start time', anchor=W)
        self.widgets['episode_result_view'].heading(3, text='End time', anchor=W)
        self.widgets['episode_result_view'].heading(4, text='Artist', anchor=W)
        self.widgets['episode_result_view'].heading(5, text='Title', anchor=W)
        for column in columns:
            self.widgets['episode_result_view'].column(
                column=column,
                anchor=W,
                width=utility.scale_size(self, 30),
                stretch=True
            )

        # Label frame
        lf_header = self.create_label_frame_header(tab, frame_text='Select Event')
        self.widgets['event_cb'] = ttk.Combobox(
            master=lf_header,
            values=[],
            width=25,
        )
        self.widgets['event_cb'].pack(side=LEFT, padx=5)
        hdr_txt = 'Please select the Event'
        hdr = ttk.Label(master=lf_header, text=hdr_txt, width=50)
        hdr.pack(side=LEFT, pady=5, padx=10)

        # Label frame
        lf_header = self.create_label_frame_header(tab, frame_text='Event management')
        edit_btn = ttk.Button(
            master=lf_header,
            text="Edit",
            command=self.get_artist_title_with_popup,
            width=10,
        )
        edit_btn.pack(side=LEFT, padx=5)
        hdr_txt = 'Edit Event data'
        hdr = ttk.Label(master=lf_header, text=hdr_txt, width=20)
        hdr.pack(side=LEFT, pady=5, padx=10)

        split_btn = ttk.Button(
            master=lf_header,
            text="Split",
            command=self.split_audio_file,
            width=10,
        )
        split_btn.pack(side=LEFT, padx=5)
        hdr_txt = 'Split audio file'
        hdr = ttk.Label(master=lf_header, text=hdr_txt, width=20)
        hdr.pack(side=LEFT, pady=5, padx=10)

    def get_episode_data(self) -> None:
        """
        Get Episode data from dB sheet and present in Tree view format.
        """
        try:
            self.clear_treeview(self.widgets['episode_result_view'])
            episode_name = self.widgets['episode_cb'].get()
            if not episode_name:
                Messagebox.show_warning('Warning: First select the episode', alert=True)
            # Populate event combobox list.
            self.widgets['event_cb']['values'] = self.data_handler.get_events_per_episode_name(episode_name)
            for row in self.data_handler.read_db_sheet():
                if row.episode_name != episode_name:
                    continue
                artist = row.artist if row.artist else ''
                title = row.title if row.title else ''
                iid = self.widgets['episode_result_view'].insert(
                    parent='',
                    index=END,
                    values=(row.event, row.clip_name, row.start, row.end, artist, title,),
                )
                self.widgets['episode_result_view'].selection_set(iid)
                self.widgets['episode_result_view'].see(iid)
        except Exception as e:
            self.log_error(e)

    def create_or_update_directory_structure(self) -> None:
        """
        Generates subdirectories to store music files
        """
        try:
            os.chdir(self.data_handler.project_root_dir)
            for episode_name in self.data_handler.get_episode_names():
                os.makedirs(episode_name, exist_ok=True)
            Messagebox.ok('Folders have been successfully created or updated')
        except TypeError:
            Messagebox.show_warning('Warning: First select Excel file', alert=True)
        except Exception as e:
            self.log_error(e)
        finally:
            os.chdir(self.data_handler.ROOT_DIR)

    def split_audio_file(self):
        """
        Split music files. A Thread is used to prevent the GUI from getting frozen.
        Exception from the thread are propagated using a queue
        """
        exception_queue = queue.Queue()

        episode_name = self.widgets['episode_cb'].get()
        th = PropagateExceptionThread(
            target=self.data_handler.split_mp4_file,
            args=(episode_name,),
            daemon=True,
            exception_queue=exception_queue,
        )
        th.start()
        th.join()
        try:
            exception = exception_queue.get_nowait()
            if isinstance(exception, ModuleNotFoundError):
                Messagebox.show_warning('Warning: pydub library has not been installed', alert=True)
            elif not self.widgets['episode_cb'].get():
                Messagebox.show_warning('Warning: Please select the Episode', alert=True)
            elif isinstance(exception, FileNotFoundError):
                Messagebox.show_warning('Warning: No music file present in folder', alert=True)
            else:
                self.log_error(exception)
        except queue.Empty:
            Messagebox.ok('Episode music file has been successfully split into event fragments')

    def get_artist_title_with_popup(self) -> None:
        """
        Input entry widget to store artist and title information.
        """
        try:
            if not self.widgets['event_cb'].get():
                Messagebox.show_warning('Warning: First select the Event', alert=True)
                return
            self.widgets['artist_title_popup'] = ttk.Toplevel(size=(300, 200),)
            self.widgets['artist_title_popup'].title("Enter Artist and Title info")

            label = ttk.Label(self.widgets['artist_title_popup'], text="Enter Artist:")
            label.pack(pady=5)
            self.widgets['artist_entry'] = ttk.Entry(self.widgets['artist_title_popup'], width=50)
            self.widgets['artist_entry'].pack(pady=5)
            label = ttk.Label(self.widgets['artist_title_popup'], text="Enter Title:")
            label.pack(pady=5)
            self.widgets['title_entry'] = ttk.Entry(self.widgets['artist_title_popup'], width=50)
            self.widgets['title_entry'].pack(pady=5)

            submit_button = ttk.Button(
                self.widgets['artist_title_popup'], text="Submit", command=self.update_artist_title_info
            )
            submit_button.pack(pady=10, padx=10)
        except Exception as e:
            self.log_error(e)

    def update_artist_title_info(self) -> None:
        """
        Updates dB sheet with information entered via input widget
        """
        try:
            clip_name = self.data_handler.get_clip_name_from_event(self.widgets['event_cb'].get())
            self.data_handler.update_artist_title_info(
                clip_name, self.widgets['artist_entry'].get(), self.widgets['title_entry'].get()
            )
            self.widgets['artist_title_popup'].destroy()
        except PermissionError:
            Messagebox.show_warning('Warning: Close the sheet first', alert=True)
        except Exception as e:
            self.log_error(e)

    def select_excel_file(self) -> None:
        """
        Callback after opening Excel file.
        """
        self.data_handler.excel_filename = askopenfilename(title="Select Excel file")
        try:
            self.data_handler.open_excel_document(self.data_handler.excel_filename)
            self.data_handler.project_root_dir = self.data_handler.excel_filename.rsplit('/', 1)[0]
            # Test if sheets can be read without problems
            self.data_handler.read_source_sheet()
            # self.data_handler.read_db_sheet()
            Messagebox.ok('File has been successfully selected')
            hdr_txt = f'Excel file {self.data_handler.excel_filename} has been selected'
            hdr = ttk.Label(master=self.widgets['excel_select_lf_header'], text=hdr_txt, width=150)
            hdr.pack(side=LEFT, pady=5, padx=10)
        except InvalidFileException:
            Messagebox.show_warning('Warning: Invalid File type or None selected!', alert=True)
        except TypeError:
            Messagebox.show_warning('Warning: First select Excel file', alert=True)
        except Exception as e:
            self.log_error(e)

    def create_additional_sheets(self) -> None:
        """
        Additional sheets are created when project is initialized.
        """
        try:
            self.data_handler.create_or_update_db_sheet()
            self.data_handler.create_clip_usage_per_episode_sheet()
            self.data_handler.create_episode_tabs()
            Messagebox.ok('Additional sheets have been successfully created')
        except TypeError:
            Messagebox.show_warning('Warning: First Select Excel file', alert=True)
        except SheetExistsException:
            Messagebox.show_warning(
                'Warning: Sheet already exists. Remove current dB sheet if you want to create a new one',
                alert=True
            )
        except Exception as e:
            print(e)
            self.log_error(e)

    def update_additional_sheets(self) -> None:
        """
        dB sheet is updated when new Episodes have been added to the source sheet
        """
        try:
            self.data_handler.create_or_update_db_sheet(update=True)
            self.data_handler.create_clip_usage_per_episode_sheet()
            self.data_handler.create_episode_tabs()
            Messagebox.ok('Sheets have been successfully updated')
        except TypeError:
            Messagebox.show_warning('Warning: First Select Excel file', alert=True)
        except PermissionError:
            Messagebox.show_warning('Warning: Close the sheet first', alert=True)
        except Exception as e:
            self.log_error(e)

    def create_label_frame_header(self, root: ttk.Frame, frame_text: str) -> ttk.Frame:
        """
        Helper function to create a ttk Frame
        """
        try:
            lf = ttk.Labelframe(root, text=frame_text, padding=5)
            lf.pack(fill=X, pady=15, padx=10)

            lf_header = ttk.Frame(lf, padding=10)
            lf_header.pack(fill=X)

            return lf_header
        except Exception as e:
            self.log_error(e)

    def clear_treeview(self, tree: ttk.Treeview) -> None:
        """
        Clears Tree view data
        """
        try:
            for i in tree.get_children():
                tree.delete(i)
        except Exception as e:
            self.log_error(e)

    @staticmethod
    def log_error(exception: Exception) -> None:
        """
        Logs application errors
        """
        method_name = inspect.currentframe().f_back.f_code.co_name
        logger.error(f"Unexpected FATAL Error occurred in method {method_name}: {exception}", exc_info=True)
        Messagebox.show_error(
            f'Error: An unexpected FATAL error occurred in method {method_name}', alert=True
        )
