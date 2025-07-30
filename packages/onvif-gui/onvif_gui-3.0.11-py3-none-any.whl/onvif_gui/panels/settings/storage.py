#/********************************************************************
# libonvif/onvif-gui/onvif_gui/panels/settings/storage.py 
#
# Copyright (c) 2024  Stephen Rhodes
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#*********************************************************************/

import os
from PyQt6.QtWidgets import QMessageBox, QSpinBox, \
    QGridLayout, QWidget, QCheckBox, QLabel, QMessageBox, QGroupBox
from PyQt6.QtCore import QStandardPaths
from loguru import logger
from onvif_gui.components import DirectorySelector
import shutil

class StorageOptions(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw

        self.archiveKey = "settings/archive"
        self.pictureKey = "settings/picture"
        self.diskLimitKey = "settings/diskLimit"
        self.mangageDiskUsagekey = "settings/manageDiskUsage"
        self.enableBulkStorageKey = "settings/enableBulkStorage"
        self.bulkArchiveKey = "settings/bulkArchive"
        self.bulkPictureKey = "settings/bulkPicture"
        self.manageBulkUsageKey = "settings/manageBulkUsage"
        self.bulkLimitKey = "settings/bulkLimit"

        video_dirs = QStandardPaths.standardLocations(QStandardPaths.StandardLocation.MoviesLocation)
        self.dirArchive = DirectorySelector(mw, self.archiveKey, "Archive Dir", video_dirs[0])
        self.dirArchive.signals.dirChanged.connect(self.dirArchiveChanged)

        picture_dirs = QStandardPaths.standardLocations(QStandardPaths.StandardLocation.PicturesLocation)
        self.dirPictures = DirectorySelector(mw, self.pictureKey, "Picture Dir", picture_dirs[0])
        self.dirPictures.signals.dirChanged.connect(self.dirPicturesChanged)

        dir_size = "{:.2f}".format(self.getDirectorySize(self.dirArchive.text()) / 1000000000)
        self.grpDiskUsage = QGroupBox(f'Disk Usage (currently {dir_size} GB)')
        self.spnDiskLimit = QSpinBox()
        max_size = int(self.getMaximumDirectorySize())
        self.spnDiskLimit.setMaximum(max_size)
        disk_limit = min(int(self.mw.settings.value(self.diskLimitKey, 100)), max_size)
        self.spnDiskLimit.setValue(disk_limit)
        self.spnDiskLimit.valueChanged.connect(self.spnDiskLimitChanged)

        lbl = f'Auto Manage (max {max_size} GB)'
        self.chkManageDiskUsage = QCheckBox(lbl)
        self.chkManageDiskUsage.setChecked(bool(int(self.mw.settings.value(self.mangageDiskUsagekey, 0))))
        self.chkManageDiskUsage.clicked.connect(self.chkManageDiskUsageChanged)

        lytDiskUsage = QGridLayout(self.grpDiskUsage)
        lytDiskUsage.addWidget(self.chkManageDiskUsage, 0, 0, 1, 1)
        lytDiskUsage.addWidget(self.spnDiskLimit,       0, 2, 1, 1)
        lytDiskUsage.addWidget(QLabel("GB"),            0, 3, 1, 1)
        lytDiskUsage.addWidget(self.dirArchive,         1, 0, 1, 4)
        lytDiskUsage.addWidget(self.dirPictures,        2, 0, 1, 4)
        lytDiskUsage.setColumnStretch(2, 10)

        '''
        self.dirBulkArchive = DirectorySelector(mw, self.bulkArchiveKey, "Archive Dir", "")
        self.dirBulkPicture = DirectorySelector(mw, self.bulkPictureKey, "Picture Dir", "") 

        self.chkManageBulkUsage = QCheckBox(lbl)
        self.spnBulkLimit = QSpinBox()
        self.spnBulkLimit.setMaximum(max_size)
        bulk_limit = min(int(self.mw.settings.value(self.bulkLimitKey, 100)), max_size)
        self.spnBulkLimit.setValue(bulk_limit)
        self.spnBulkLimit.valueChanged.connect(self.spnBulkLimitChanged)

        self.grpBulkUsage = QGroupBox(f'Bulk Storage (currently {10} GB)')
        self.grpBulkUsage.setCheckable(True)
        self.grpBulkUsage.setChecked(bool(int(self.mw.settings.value(self.enableBulkStorageKey, 0))))
        self.grpBulkUsage.clicked.connect(self.grpBulkUsageChecked)

        lytBulkUsage = QGridLayout(self.grpBulkUsage)
        lytBulkUsage.addWidget(self.chkManageBulkUsage,  0, 0, 1, 1)
        lytBulkUsage.addWidget(self.spnBulkLimit,        0, 2, 1, 1)
        lytBulkUsage.addWidget(QLabel("GB"),             0, 3, 1, 1)
        lytBulkUsage.addWidget(self.dirBulkArchive,      1, 0, 1, 4)
        lytBulkUsage.addWidget(self.dirBulkPicture,      2, 0, 1, 4)
        '''

        lytMain = QGridLayout(self)
        lytMain.addWidget(self.grpDiskUsage, 0, 0, 1, 1)
        lytMain.addWidget(QLabel(),          1, 0, 1, 1)
        #lytMain.addWidget(self.grpBulkUsage, 2, 0, 1, 1)
        lytMain.addWidget(QLabel(),          3, 0, 1, 1)
        lytMain.setRowStretch(3, 10)

    def spnDiskLimitChanged(self, value):
        self.mw.settings.setValue(self.diskLimitKey, value)

    def spnBulkLimitChanged(self, value):
        self.mw.settings.setValue(self.bulkLimitKey, value)

    def grpBulkUsageChecked(self, value):
        self.mw.settings.setValue(self.enableBulkStorageKey, int(value))

    def chkManageDiskUsageChanged(self):
        if self.chkManageDiskUsage.isChecked():
            ret = QMessageBox.warning(self, "** WARNING **",
                                        "You are giving full control of the archive directory to this program.  "
                                        "Any files contained within this directory or its sub-directories are subject to deletion.  "
                                        "You should only enable this feature if you are sure that this is ok.\n\n"
                                        "Are you sure you want to continue?",
                                        QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if ret == QMessageBox.StandardButton.Cancel:
                self.chkManageDiskUsage.setChecked(False)
        self.mw.settings.setValue(self.mangageDiskUsagekey, int(self.chkManageDiskUsage.isChecked()))

    def dirArchiveChanged(self, path):
        logger.debug(f'Video archive directory changed to {path}')
        self.mw.settings.setValue(self.archiveKey, path)
        max_size = int(self.getMaximumDirectorySize())
        self.spnDiskLimit.setMaximum(max_size)
        lbl = f'Auto Manage (max {max_size} GB)'
        self.chkManageDiskUsage.setText(lbl)
        disk_limit = min(int(self.mw.settings.value(self.diskLimitKey, 100)), max_size)
        self.spnDiskLimit.setValue(disk_limit)
        self.chkManageDiskUsageChanged()

    def dirPicturesChanged(self, path):
        logger.debug(f'Picture directory changed to {path}')
        self.mw.settings.setValue(self.pictureKey, path)

    def getMaximumDirectorySize(self):
        # compute disk space available for archive directory in GB
        d = self.dirArchive.txtDirectory.text()
        if not os.path.isdir(d):
            return 0
        d_size = 0
        max_available = 0
        try:
            for dirpath, dirnames, filenames in os.walk(d):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        if not os.path.islink(fp):
                            d_size += os.path.getsize(fp)
            total, used, free = shutil.disk_usage(d)
            max_available = (free + d_size - 10000000000) / 1000000000
        except Exception as ex:
            logger.error(f'Exception occurred during disk space calculation: {ex}')
        return max_available

    def getDirectorySize(self, d):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(d):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        
        return total_size
    
