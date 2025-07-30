from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class CustomInstallCommand(install):
    def run(self):
        install.run(self)  # Standard install steps

        # Post-install message and optional symlink creation
        local_bin = os.path.expanduser("~/.local/bin/shield")
        system_bin = "/usr/local/bin/shield"

        print("\n🎉 MinakiShield installed!")
        print("📦 Binary: ~/.local/bin/shield")

        if os.path.exists(local_bin):
            try:
                if not os.path.exists(system_bin):
                    os.symlink(local_bin, system_bin)
                    print(f"✅ Symlink created: {system_bin}")
                else:
                    print("ℹ️ Symlink already exists.")
            except PermissionError:
                print("⚠️ Could not create global symlink (Permission denied). You can do it manually:")
                print(f"   sudo ln -s {local_bin} {system_bin}")
            except Exception as e:
                print(f"❌ Unexpected error while creating symlink: {e}")
        else:
            print("⚠️ Binary not found in ~/.local/bin. Check your pip install location.")

setup(
    name='minaki-shield',
    version='1.1.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'psutil'
    ],
    entry_points={
        'console_scripts': [
            'shield=shield.cli:main',
        ],
    },
    author='Andrew Polykandriotis',
    description='Modular Linux intrusion detection CLI by MinakiLabs',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: System Administrators',
        'Topic :: Security',
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
