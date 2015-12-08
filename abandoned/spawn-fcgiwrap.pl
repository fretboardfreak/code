#!/usr/bin/perl

use strict;
use warnings FATAL => qw( all );

use IO::Socket::UNIX;

my  = '/usr/sbin/fcgiwrap';
my  = [0] || '/var/run/fcgiwrap.socket';
my  = [1] || 1;

close STDIN;

unlink ;
my  = IO::Socket::UNIX->new(
    Local => ,
    Listen => 100,
);

die "Cannot create socket at : \n" unless ;

for (1 .. ) {
    my  = fork;
    die "Cannot fork: " unless defined ;
    next if ;

    exec ;
    die "Failed to exec : \n";
}
