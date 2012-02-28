import fudge
from fudge.patcher import patch_object
from nose.plugins.attrib import attr
from tests import fixture_path
from virtstrap import constants
from virtstrap.testing import *
from virtstrap_local.commands.install import InstallCommand

PACKAGES_DIR = fixture_path('packages')

def test_initialize_command():
    command = InstallCommand()

class TestInstallCommand(object):
    def setup(self):
        self.command = InstallCommand()
        self.pip_index_ctx = ContextUser(temp_pip_index(PACKAGES_DIR))
        self.index_url = self.pip_index_ctx.enter()
        self.temp_proj_ctx = ContextUser(temp_project())
        self.project, self.options, self.temp_dir = self.temp_proj_ctx.enter()

    def teardown(self):
        self.temp_proj_ctx.exit()
        self.pip_index_ctx.exit()
    
    @attr('slow')
    @hide_subprocess_stdout
    @fudge.test
    def test_run_install(self):
        # Install should process the requirements 
        # and create a requirement_set
        # The requirement_set is then turned into a 
        # string and written to a requirements file to be
        # used by pip and install the requirements
        project = self.project
        options = self.options
        temp_dir = self.temp_dir
        fake_req_set = (project.__patch_method__('process_config_section')
                .returns_fake())
        fake_req_set.expects('to_pip_str').returns("test1")
        self.command.run(project, options)
        requirements_file = open(constants.VE_LOCK_FILENAME)
        requirements_data = requirements_file.read()
        assert 'test1==0.1' in requirements_data

    @attr('slow')
    @hide_subprocess_stdout
    @fudge.test
    def test_run_install_multiple_packages(self):
        project = self.project
        options = self.options
        temp_dir = self.temp_dir
        fake_req_set = (project.__patch_method__('process_config_section')
                .returns_fake())
        fake_req_set.expects('to_pip_str').returns("test1\ntest5")
        self.command.run(project, options)
        requirements_file = open(constants.VE_LOCK_FILENAME)
        requirements_data = requirements_file.read()
        expected_packages = ['test1==0.1', 'test2==1.3', 
                'test3==0.10.1', 'test5==1.4.3']
        for package in expected_packages:
            assert package in requirements_data


