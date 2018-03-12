from fabric.api import *

prod_server = 'emiamar@emiamar.webfactional.com'


def prod():
    env.hosts = [prod_server]
    env.remote_app_dir = '/home/emiamar/webapps/rajdeep/pyfactory_cnc/pyfactory_cnc'
    env.remote_app_source_dir = '/home/emiamar/webapps/rajdeep/pyfactory_cnc/project_directory'
    env.remote_apache_dir = '/home/emiamar/webapps/rajdeep/apache2'
    env.remote_server_dir = '/home/emiamar/webapps/rajdeep'


def commit():
    message = raw_input("Enter a mercurial commit message:  ")
    local("hg commit -m \"%s\"" % message)
    local("hg push")
    print "Changes have been pushed to remote repository..."


def add_commit():
    message = raw_input("Enter a mercurial commit message:  ")
    local("hg add")
    local("hg commit -m \"%s\"" % message)
    local("hg push")
    print "Changes have been pushed to remote repository..."


def collectstatic():
    require('hosts', provided_by=[prod])
    run("cd %s; source bin/activate" % env.remote_server_dir)
    run("cd %s; python manage.py collectstatic --noinput" % env.remote_app_dir)
    run("%s/bin/restart;" % (env.remote_apache_dir))


def restart():
    """Restart apache on the server."""
    require('hosts', provided_by=[prod])
    require('remote_apache_dir', provided_by=[prod])

    run("%s/bin/restart;" % (env.remote_apache_dir))


def fastdeploy():
    require('hosts', provided_by=[prod])
    require('remote_app_dir', provided_by=[prod])
    message = raw_input("Enter a mercurial commit message:  ")
    local("hg commit -m \"%s\"" % message)
    local("hg push")
    print "Changes have been pushed to remote repository..."
    run("cd %s; hg pull ssh://hg@bitbucket.org/asavalagi/pyfactory_cnc" % env.remote_app_dir)
    run("cd %s; hg update" % env.remote_app_dir)
    restart()
    # collectstatic()


def deploy():
    require('hosts', provided_by=[prod])
    require('remote_app_dir', provided_by=[prod])
    run("cd %s; hg pull ssh://hg@bitbucket.org/asavalagi/pyfactory_cnc" % env.remote_app_dir)
    run("cd %s; hg update" % env.remote_app_dir)
    restart()

def deploy_source():
    require('hosts', provided_by=[prod])
    require('remote_app_source_dir', provided_by=[prod])
    run("cd %s; hg pull ssh://hg@bitbucket.org/anandpujari/rajdeep_source" % env.remote_app_dir)
    run("cd %s; hg update" % env.remote_app_dir)
    restart()


def migrate_deploy():
    require('hosts', provided_by=[prod])
    require('remote_app_dir', provided_by=[prod])
    app_name = raw_input("Enter the app name to migrate:  ")
    run("cd %s; hg pull" % env.remote_app_dir)
    run("cd %s; hg update" % env.remote_app_dir)
    run("cd %s; source bin/activate" % env.remote_server_dir)
    run("cd %s; python manage.py migrate %s" % (env.remote_app_dir,app_name ))
    restart()

def migrate():
    require('hosts', provided_by=[prod])
    require('remote_app_dir', provided_by=[prod])
    app_name = raw_input("Enter the app name to migrate:  ")
    run("cd %s; source bin/activate" % env.remote_server_dir)
    run("cd %s; python manage.py migrate %s" % (env.remote_app_dir,app_name ))


def list_migration():
    activate()
    require('hosts', provided_by=[prod])
    require('remote_app_dir', provided_by=[prod])
    app_name = raw_input("Enter the app name to migrate:  ")
    run("cd %s; python manage.py migrate --list %s" % (env.remote_app_dir,app_name ))


def install_pip():
    package = raw_input("Enter the pip package you want to install:  ")
    require('hosts', provided_by=[prod])
    require('remote_app_dir', provided_by=[prod])
    run(" pip2.7 install --user %s" % package )
    restart()


def activate():
    require('hosts', provided_by=[prod])
    run("cd %s; source bin/activate" % env.remote_server_dir)
