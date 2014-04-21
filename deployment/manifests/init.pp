Exec { path => '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin' }

# Global variables
$inc_file_path = '/vagrant/manifests/files' # Absolute path to the files directory (If you're using vagrant, you can leave it alone.)
$tz = 'Pacific/Honolulu' # Timezone
$project = 'kala' # Used in nginx and uwsgi
$domain_name = 'kala.localhost' # Used in nginx, uwsgi and virtualenv directory
$db_name = 'kala' # Postgres database name to create
$db_user = 'kala' # Postgres username to create
$db_password = 'kala' # Postgres password for $db_user
$secret_key = '68d3b82e-08eb-4585-b8d4-2b77d73f2a89' # Change if you want

include timezone
include apt
include nginx
include uwsgi
include postgres
include python
include virtualenv
include pildeps
include software
include syncdb
include user_config

class timezone {
  package { "tzdata":
    ensure => latest,
    require => Class['apt'],
  }

  file { "/etc/localtime":
    require => Package["tzdata"],
    source => "file:///usr/share/zoneinfo/${tz}",
  }
  }

  class apt {
  exec { 'apt-get update':
    timeout => 0
  }

  package { 'python-software-properties':
    ensure => latest,
    require => Exec['apt-get update'],
  }
}

class nginx {
  package { 'nginx':
    ensure => latest,
    require => Class['apt'],
  }

  service { 'nginx':
    ensure => running,
    enable => true,
    require => Package['nginx'],
  }

  file { '/etc/nginx/sites-enabled/default':
    ensure => absent,
    require => Package['nginx'],
  }

  file { 'sites-available config':
    path => "/etc/nginx/sites-available/${domain_name}",
    ensure => file,
    content => template("${inc_file_path}/nginx/nginx.conf.erb"),
    require => Package['nginx'],
  }

  file { "/etc/nginx/sites-enabled/${domain_name}":
    ensure => link,
    target => "/etc/nginx/sites-available/${domain_name}",
    require => File['sites-available config'],
    notify => Service['nginx'],
  }
}

class uwsgi {
  package { 'uwsgi':
    ensure => latest,
    require => [Class['apt'], Class['python'], Class['virtualenv']],
  }

  package { 'uwsgi-plugin-python3':
    ensure => latest,
    require => Package['uwsgi'],
  }

  service { 'uwsgi':
    ensure => running,
    enable => true,
    require => Package['uwsgi'],
  }

  file { '/etc/uwsgi/apps-enabled/README':
    ensure => absent,
    require => Package['uwsgi'],
  }

  file { 'apps-available config':
    path => "/etc/uwsgi/apps-available/${domain_name}.ini",
    ensure => file,
    content => template("${inc_file_path}/uwsgi/uwsgi.ini.erb"),
    require => Package['uwsgi'],
  }

  file { "/etc/uwsgi/apps-enabled/${domain_name}.ini":
    ensure => link,
    target => "/etc/uwsgi/apps-available/${domain_name}.ini",
    require => File['apps-available config'],
    notify => Service['uwsgi'],
  }
}

class postgres {
  package { 'postgresql':
    ensure => latest,
    require => Class['apt'],
  }

  package { 'postgresql-client':
    ensure => latest,
    require => Class['apt'],
  }

  package { 'postgresql-contrib':
    ensure => latest,
    require => Class['apt'],
  }

  package { 'postgresql-server-dev-all':
    ensure => latest,
    require => Class['apt'],
  }

  service { 'postgresql':
    ensure => running,
    enable => true,
    require => Package['postgresql'],
  }


  exec { 'create role':
    command => "sudo -u postgres -- psql -c \"CREATE ROLE \\\"${db_user}\\\" WITH LOGIN PASSWORD '${db_password}';\"",
    unless => "sudo -u postgres -- psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname='${db_user}'\" | grep -q 1",
    require => Service['postgresql'],
  }

  exec { 'create database':
    command => "sudo -u postgres -- psql -c \"CREATE DATABASE \\\"${db_name}\\\" WITH OWNER \\\"${db_user}\\\";\"",
    unless => "sudo -u postgres -- psql -tAc \"SELECT 1 from pg_database WHERE datname='${db_name}'\" | grep -q 1",
    require => Exec['create role'],
  }
}

class syncdb {
  exec { 'syncdb':
    command => "bash -c \"export KALA_DEPLOYMENT_ENVIRONMENT=development &&\
      export KALA_DATABASE_NAME=kala &&\
      export KALA_DATABASE_USER=kala &&\
      export KALA_DATABASE_PASSWORD=kala &&\
      export KALA_SECRET_KEY=68d3b82e-08eb-4585-b8d4-2b77d73f2a89 &&\
      /home/vagrant/virtualenvs/${project}/bin/python manage.py syncdb --noinput &&\
      touch /srv/${project}/reload\"",
    cwd         => "/srv/${project}",
    user        => vagrant,
    require     => [Class['virtualenv'], Class['postgres']]
  }
}

class python {
  package { 'python3':
    ensure => latest,
    require => Class['apt'],
  }

  package { 'python3-dev':
    ensure => latest,
    require => Class['apt'],
  }

  package { 'python3-pip':
    ensure => latest,
    require => Class['apt'],
  }
}

class virtualenv {
  exec { 'virtualenv':
    command => "sudo pip3 install virtualenv",
    require => Class['python', 'pildeps'],
  }

  exec { 'create virtualenv':
    command => "sudo -u vagrant virtualenv /home/vagrant/virtualenvs/${project}",
    unless => 'test -d /home/vagrant/virtualenvs/${project}',
    require => Exec['virtualenv'],
  }

  exec { 'pip install':
    command => "sudo -u vagrant /home/vagrant/virtualenvs/${project}/bin/pip install -r /srv/${project}/requirements.txt",
    require => Exec['create virtualenv'],
  }
}

class pildeps {
  package { 'libjpeg-dev':
    ensure => latest,
    require => Class['apt'],
  }

  package { 'libfreetype6-dev':
    ensure => latest,
    require => Class['apt'],
  }

  package { 'liblcms1-dev':
    ensure => latest,
    require => Class['apt'],
  }

  package { 'libtiff4-dev':
    ensure => latest,
    require => Class['apt'],
  }

  package { 'libwebp-dev':
    ensure => latest,
    require => Class['apt'],
  }
}

class software {
  package { 'git':
    ensure => latest,
    require => Class['apt'],
  }

  package { 'zsh':
    ensure => latest,
    require => Class['apt'],
  }

  package { 'libxslt-dev':
    ensure => latest,
    require => Class['apt'],
  }
}

class user_config {
  # Clone oh-my-zsh
  exec { 'clone oh-my-zsh':
    cwd     => "/home/vagrant",
    user    => "vagrant",
    command => "git clone https://github.com/robbyrussell/oh-my-zsh.git /home/vagrant/.oh-my-zsh",
    creates => "/home/vagrant/.oh-my-zsh",
    require => [Package['git'], Package['zsh']]
  }

  exec { 'copy-config':
    cwd     => "/home/vagrant",
    user    => "vagrant",
    command => "sudo -u vagrant cp /home/vagrant/.oh-my-zsh/templates/zshrc.zsh-template /home/vagrant/.zshrc",
    require => Exec['clone oh-my-zsh']
  }

  exec { 'activate cd':
    cwd     => "/home/vagrant",
    user    => "vagrant",
    command => "echo 'source /home/vagrant/virtualenvs/kala/bin/activate' >> /home/vagrant/.zshrc && echo 'cd /srv/kala' >> /home/vagrant/.zshrc",
    require => Exec['copy-config']
  }

  # Set the shell
  exec { "chsh -s /usr/bin/zsh vagrant":
    unless  => "grep -E '^vagrant.+:/usr/bin/zsh$' /etc/passwd",
    require => Package['zsh']
  }

  file { "/etc/environment":
    content => "export KALA_DEPLOYMENT_ENVIRONMENT=development
      export KALA_DATABASE_NAME=${db_name}
      export KALA_DATABASE_USER=${db_user}
      export KALA_DATABASE_PASSWORD=${db_password}
      export KALA_SECRET_KEY=${secret_key}",
    mode => 644,
  }
}
