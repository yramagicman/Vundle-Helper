import os, vim, datetime, time, Self_update
from subprocess import call, check_output
home = os.path.expanduser('~')

def VundleHelper_sanity_check():
    # Make sure variables exist. The script only requires
    # g:VundleHelper_Setup_Folders.
    dir_tree_defined = int(vim.eval('exists("g:VundleHelper_Setup_Folders")'))
    plugin_file_defined = int(vim.eval('exists("g:VundleHelper_Plugin_File")'))
    # Check for .vim/bundle. The script breaks without it.
    if not os.path.exists(home + '/.vim/bundle'):
        cmd= ['mkdir', '-p']
        cmd = cmd + ['bundle']
        os.chdir(home + '/.vim/')
        call(cmd)
    # If both config variables are defined, return their values.
    if dir_tree_defined and  plugin_file_defined:
        dir_tree = vim.eval("g:VundleHelper_Setup_Folders")
        plugin_file = vim.eval("g:VundleHelper_Plugin_File")
        return dir_tree, plugin_file
    # If g:VundleHelper_Setup_Folders is defined, return its value and the location
    # of the .vimrc file
    elif dir_tree_defined and not plugin_file_defined:
        plugin_file= vim.eval('$MYVIMRC')
        dir_tree = vim.eval("g:VundleHelper_Setup_Folders")
        return dir_tree, plugin_file
    # When all else fails print an error message.
    else:
        print 'You must at least define g:VundleHelper_Setup_Folders for this to work.'

# Set variables globally
setup_folders, plugin_file = VundleHelper_sanity_check()

def VundleHelper_pkg_manager_install():
    os.chdir(home + '/.vim/bundle')
    call(['git', 'clone', 'https://github.com/gmarik/Vundle.vim.git'])

def VundleHelper_check_dir():
    installed_packages = check_output(['ls', home + '/.vim/bundle'])
    installed_packages = installed_packages.split('\n')
    return installed_packages

def VundleHelper_read_bundle(file):
    bundles = open(file, 'r')
    lines = bundles.read().split('\n')
    ret_val = []
    for line in lines:
        if ('Plugin' in line or 'plugin' in line) and ('"' not in line):
            ret_val.append(line[line.index('/') + 1: -1])
    bundles.close()
    return ret_val

def VundleHelper_check_installation():
    to_install = VundleHelper_read_bundle(home + plugin_file)
    installed = VundleHelper_check_dir()
    not_installed = []
    for i in to_install:
        if i not in installed:
            not_installed.append(i)
    return not_installed

def VundleHelper_clean_up():
    listed = VundleHelper_read_bundle(home + plugin_file)
    remove = VundleHelper_check_dir()
    to_remove = []
    for i in remove:
        if i not in listed:
            to_remove.append(i)
    return to_remove

def VundleHelper_run_install():
    if len(VundleHelper_check_installation()) > 0:
        os.chdir(home + '/.vim/')
        call(['mkdir', '-p'] + setup_folders)
        if 'Vundle.vim' in VundleHelper_check_installation():
            VundleHelper_pkg_manager_install()
            # Source .vimrc to make sure the package manager is loaded
            vim.command('source $MYVIMRC')
        # Run the package manger
        vim.command('PluginInstall')
        # Load everything.
        vim.command('source $MYVIMRC')
    # clean_up() always returns an empty string, so check for length greater
    # than 1 to account for this.
    if len(VundleHelper_clean_up()) > 1:
        vim.command('PluginClean')

def VundleHelper_update_how_often():
    often_set = int(vim.eval('exists("g:VundleHelper_Update_Frequency")'))
    if often_set:
        return vim.eval('g:VundleHelper_Update_Frequency')
    else:
        return False

def VundleHelper_read_update_cache():
    try:
        f = open(home + '/.vim/lastupdate', 'r')
        dates = f.read()
        f.close()
        return dates
    except:
        print "File not found. Running updates and writing new file."
        time.sleep(2)
        vim.command('PluginUpdate')
        return VundleHelper_write_last_update()

def VundleHelper_get_last_update(dates):
    date = dates.split('\n')
    date= float(date[0])
    return date

def VundleHelper_get_next_update(dates):
    date = dates.split('\n')
    date= float(date[1])
    return date

def VundleHelper_write_last_update(days=30):
    next = days * 24 * 60 * 60
    f = open(home + '/.vim/lastupdate', 'w')
    f.write(str(time.time()) + '\n')
    f.write(str(time.time() + next))
    f.close()
    return str(time.time()) + '\n' + str(time.time() + next)

def VundleHelper_run_updates():
    dates = VundleHelper_read_update_cache()
    next = VundleHelper_get_next_update(dates)
    freq = VundleHelper_update_how_often()
    if next < time.time():
        vim.command('PluginUpdate')
        if freq:
            VundleHelper_write_last_update(freq)
        else:
            VundleHelper_write_last_update()

def VundleHelper_self_update():
    one_day = 1 * 24 * 60 * 60
    dates = VundleHelper_read_update_cache()
    next = VundleHelper_get_next_update(dates)
    freq = VundleHelper_update_how_often()
    if next < time.time() + one_day:
        s = Self_update.Self_update()
        s.run()

# Copyright Jonathan Gilson 2014
