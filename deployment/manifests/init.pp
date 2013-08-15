Exec { path => '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin' }

# Global variables
$inc_file_path = '/vagrant/manifests/files' # Absolute path to the files directory (If you're using vagrant, you can leave it alone.)
$tz = 'Pacific/Honolulu' # Timezone
$project = 'kala' # Used in nginx and uwsgi
$domain_name = 'kala.ndptc.manoa.hawaii.edu' # Used in nginx, uwsgi and virtualenv directory
$db_name = 'ndptc' # Mysql database name to create
$db_user = 'ndptc' # Mysql username to create
$db_password = 'ndptc' # Mysql password for $db_user
$secret_key = '68d3b82e-08eb-4585-b8d4-2b77d73f2a89'

include timezone
include apt
include nginx
include uwsgi
include postgres
include python
include virtualenv
include pildeps
include software

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
    require => Class['apt'],
  }

  package { 'uwsgi-plugin-python':
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

  package { 'postgresql-server-dev-9.1':
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

class python {
  package { 'python':
    ensure => latest,
    require => Class['apt'],
  }

  package { 'python-dev':
    ensure => latest,
    require => Class['apt'],
  }

  package { 'python-pip':
    ensure => latest,
    require => Class['apt'],
  }

}

class virtualenv {
  package { 'virtualenv':
    ensure => latest,
    provider => pip,
    require => Class['python', 'pildeps'],
  }

  exec { 'create virtualenv':
    command => "sudo -u vagrant virtualenv /home/vagrant/virtualenvs/${project}",
    unless => 'test -d /home/vagrant/virtualenvs/moi',
    require => Package['virtualenv'],
  }

  exec { 'pip install':
    command => "sudo -u vagrant pip install -E /home/vagrant/virtualenvs/${project} -r /srv/${project}/requirements.txt",
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
